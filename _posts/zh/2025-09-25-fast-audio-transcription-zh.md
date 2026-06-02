---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: 加速长音频转录处理
translated: true
type: note
---

### 为什么30分钟或1小时的音频处理时间这么长？

Google Cloud Speech-to-Text 批量 API (v2) 专为异步长时间运行的操作而设计，特别是使用 `"long"` 模型处理长音频文件（每个文件最多约1小时）。以下是它可能感觉"太慢"的原因：

- **处理时间随音频长度增加**：转录不是瞬时的。对于30分钟的音频文件，可能需要5-20分钟；对于1小时的音频，可能需要10-40分钟或更长时间。这包括：
  - 排队时间（如果你的项目/区域繁忙）。
  - 实际转录时间（AI模型推理，对长音频计算密集）。
  - 后处理时间（例如，词级时间戳、置信度分数）。
- **批量处理性质**：与实时流式处理不同，批量作业在 Google 服务器上后台运行。你的脚本调用 `operation.result()` 会阻塞等待，但实际工作是异步进行的。
- **其他因素**：
  - 音频格式/质量：OGG/Opus 或 M4A/AAC 需要解码，如果采样率/声道不匹配会增加开销。
  - 模型选择：`"long"` 针对会议/播客优化，但比 `"default"` 或 `"short"` 等短音频模型慢。
  - 网络/配额：上传到 GCS、API 调用和下载结果会增加延迟。免费层配额或高需求可能延迟作业。
  - 无内置并行：脚本按顺序一次处理一个文件。

如果你的音频持续超过30分钟，当前设置不适合快速周转——它更适合离线/批量处理。

### 如何修复：减少处理时间

要更快处理长音频，关键是**将文件分割成更小的块**（例如，每块5-15分钟）。这样可以：

- 并行处理（同时运行多个批量作业）。
- 使用更快的模型（例如，每块使用 `"short"` 或 `"default"`）。
- 每作业等待时间更短（例如，每块1-5分钟 vs 整个文件30+分钟）。

#### 步骤1：分割音频文件

使用 **FFmpeg**（免费命令行工具）分割文件而无需重新编码（快速且无损）。如果需要请安装 FFmpeg（例如，macOS 上 `brew install ffmpeg`，Linux 上 `apt install ffmpeg`）。

在你的脚本中添加一个函数来分割输入文件。以下是集成了分割功能的脚本更新版本：

```python
import os
import argparse
import subprocess
import tempfile
from google.cloud import storage
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import sys
import time  # 用于轮询

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.llm.openrouter_client import call_openrouter_api  # noqa: F401

MAX_AUDIO_LENGTH_SECS = 20 * 60 * 60
OUTPUT_DIRECTORY = "assets/transcriptions"
CHUNK_DURATION_SECS = 600  # 每块10分钟；根据需要调整（例如，900为15分钟）


def split_audio_file(input_file, chunk_duration_secs=CHUNK_DURATION_SECS):
    """
    使用 FFmpeg 将音频文件分割成更小的块。

    参数：
        input_file: 输入音频路径。
        chunk_duration_secs: 每块的持续时间（秒）。

    返回：
        块文件路径列表。
    """
    filename = os.path.basename(input_file)
    name_without_ext = os.path.splitext(filename)[0]
    dir_name = os.path.dirname(input_file)

    # 为块创建临时目录
    temp_dir = tempfile.mkdtemp()
    chunk_files = []

    # FFmpeg 命令（无需重新编码以提高速度）
    cmd = [
        "ffmpeg", "-i", input_file,
        "-f", "segment",  # 输出格式
        "-segment_time", str(chunk_duration_secs),
        "-c", "copy",  # 无需重新编码直接复制流
        "-map", "0",  # 映射所有流
        f"{temp_dir}/{name_without_ext}_chunk_%03d.{os.path.splitext(filename)[1][1:]}",  # 输出模式
        "-y"  # 覆盖
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        # 查找生成的块
        for file in os.listdir(temp_dir):
            if file.startswith(f"{name_without_ext}_chunk_") and file.endswith(os.path.splitext(filename)[1]):
                chunk_files.append(os.path.join(temp_dir, file))
        chunk_files.sort()  # 按名称排序（例如，chunk_001, chunk_002）
        print(f"已将 {filename} 分割为 {len(chunk_files)} 个块。")
        return chunk_files
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 分割 {filename} 时出错：{e}")
        return []


def run_batch_recognize(audio_gcs_uri, output_gcs_folder, language_code="en-US"):
    """
    使用 Google Cloud Speech-to-Text 批量 API 转录音频文件。
    更新为在音频可能较短时（例如，分割后）使用更短的模型。
    """
    client = SpeechClient()

    filename = audio_gcs_uri.split('/')[-1]
    file_extension = filename.split('.')[-1].lower()

    # 对于块，使用 "short" 或 "default" 模型以提高速度（如果 <15 分钟）
    model = "short" if CHUNK_DURATION_SECS < 900 else "long"  # 根据块大小调整

    if file_extension == "ogg":
        decoding = cloud_speech.ExplicitDecodingConfig(
            encoding=cloud_speech.ExplicitDecodingConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,
            audio_channel_count=1
        )
        config = cloud_speech.RecognitionConfig(
            explicit_decoding_config=decoding,
            features=cloud_speech.RecognitionFeatures(
                enable_word_confidence=True,
                enable_word_time_offsets=True,
            ),
            model=model,
            language_codes=[language_code],
        )
    else:
        config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            features=cloud_speech.RecognitionFeatures(
                enable_word_confidence=True,
                enable_word_time_offsets=True,
            ),
            model=model,
            language_codes=[language_code],
        )

    output_config = cloud_speech.RecognitionOutputConfig(
        gcs_output_config=cloud_speech.GcsOutputConfig(uri=output_gcs_folder),
    )

    files = [cloud_speech.BatchRecognizeFileMetadata(uri=audio_gcs_uri)]

    request = cloud_speech.BatchRecognizeRequest(
        recognizer="projects/graphite-ally-445108-k3/locations/global/recognizers/_",
        config=config,
        files=files,
        recognition_output_config=output_config,
    )

    print(f"开始为 {filename} 进行批量识别...")
    operation = client.batch_recognize(request=request)

    # 轮询进度（详见下文）
    poll_operation_with_progress(operation, filename)

    response = operation.result(timeout=3 * CHUNK_DURATION_SECS)  # 每块更短的超时时间
    print(f"完成 {filename} 的转录。响应：{response}")
    return response


def poll_operation_with_progress(operation, filename):
    """
    轮询长时间运行的操作并显示进度。
    """
    while not operation.done():
        # 获取操作元数据（如果可用；Speech API 提供基本状态）
        try:
            metadata = operation.metadata
            print(f"{filename} 的进度：状态={getattr(metadata, 'state', 'Unknown')}, "
                  f"已处理={getattr(metadata, 'progress_bytes', 'N/A')} 字节")
        except Exception:
            print(f"等待 {filename}...（每30秒检查一次）")

        time.sleep(30)  # 每30秒轮询一次
    if operation.exception():
        raise operation.exception()


def process_audio_file(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.basename(input_file)
    if not (filename.endswith(".m4a") or filename.endswith(".ogg")):
        print(f"错误：{filename} 不是支持的音频文件（.m4a 或 .ogg）。")
        return

    output_filename = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
    if os.path.exists(output_filename):
        print(f"跳过 {filename}：{output_filename} 已存在。")
        return

    print(f"处理中：{filename}")

    # 确定语言
    if filename.endswith("-zh.m4a") or filename.endswith("-zh.ogg"):
        language_code = "cmn-CN"
    else:
        language_code = "en-US"

    # 如果文件较长则分割（启发式：>15 分钟，但你可以使用 ffprobe 探测持续时间）
    chunk_files = []
    if os.path.getsize(input_file) > 100 * 1024 * 1024:  # 粗略检查：>100MB 可能较长
        print(f"文件较大；分割为 {CHUNK_DURATION_SECS//60} 分钟的块。")
        chunk_files = split_audio_file(input_file)
        if not chunk_files:
            print("分割失败；作为单个文件处理。")
            chunk_files = [input_file]
    else:
        chunk_files = [input_file]

    storage_client = storage.Client()
    bucket = storage_client.bucket("test2x")

    all_transcripts = []  # 用于后续合并

    for chunk_idx, chunk_file in enumerate(chunk_files):
        chunk_filename = os.path.basename(chunk_file)
        base_name = os.path.splitext(filename)[0]
        chunk_name = f"{base_name}_chunk_{chunk_idx+1:03d}"

        # 构建 GCS 路径
        gcs_audio_uri = f"gs://test2x/audio-files/{chunk_filename}"
        gcs_output_uri = f"gs://test2x/transcripts/{chunk_name}"

        # 如果需要则上传块
        blob = bucket.blob(f"audio-files/{chunk_filename}")
        if not blob.exists():
            blob.upload_from_filename(chunk_file)
            print(f"已将块 {chunk_filename} 上传到 GCS。")
        else:
            print(f"块 {chunk_filename} 已在 GCS 中。")

        # 转录
        try:
            run_batch_recognize(
                audio_gcs_uri=gcs_audio_uri,
                output_gcs_folder=gcs_output_uri,
                language_code=language_code,
            )

            # 下载并收集转录稿
            blobs = storage_client.list_blobs("test2x", prefix=f"transcripts/{chunk_name}")
            chunk_transcript = ""
            for b in blobs:
                if b.name.endswith(".json"):
                    local_path = os.path.join(output_dir, f"{os.path.basename(b.name)}")
                    b.download_to_filename(local_path)
                    # 解析 JSON 提取文本（简化版；使用 json 模块进行完整解析）
                    import json
                    with open(local_path, 'r') as f:
                        data = json.load(f)
                        if 'results' in data:
                            chunk_text = ' '.join([result.get('alternatives', [{}])[0].get('transcript', '') for result in data['results']])
                            chunk_transcript += chunk_text + "\n"
                    print(f"已下载并解析 {b.name}")

            all_transcripts.append(chunk_transcript)

            # 如果分割了则清理临时块
            if chunk_file != input_file and os.path.exists(chunk_file):
                os.remove(chunk_file)

        except Exception as e:
            print(f"处理块 {chunk_filename} 失败：{e}")

    # 将所有转录稿合并到一个文件中
    combined_text = "\n\n--- 块边界 ---\n\n".join(all_transcripts)
    with open(output_filename, 'w') as f:
        f.write(combined_text)
    print(f"合并的转录稿已保存到 {output_filename}")

    # 如果进行了分割则清理临时目录
    if chunk_files != [input_file]:
        import shutil
        shutil.rmtree(os.path.dirname(chunk_files[0]) if chunk_files else None)

    print(f"完成 {filename} 的处理。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="处理单个语音备忘录 (.m4a/.ogg) 文件以生成转录稿。"
    )
    parser.add_argument(
        "--input_file",
        type=str,
        required=True,
        help="语音备忘录文件的输入路径。",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="assets/transcriptions",
        help="转录稿的输出目录。",
    )
    parser.add_argument(
        "--chunk_secs",
        type=int,
        default=CHUNK_DURATION_SECS,
        help="块持续时间（秒）（用于分割长文件）。",
    )

    args = parser.parse_args()
    global CHUNK_DURATION_SECS  # 允许覆盖
    CHUNK_DURATION_SECS = args.chunk_secs

    process_audio_file(
        input_file=args.input_file,
        output_dir=args.output,
    )
```

#### 关键更改和好处

- **分割**：使用 FFmpeg 创建非重叠块（例如，每块10分钟）。对于1小时的文件，约6个作业，如果修改为使用线程/多进程（例如，通过 `concurrent.futures`）可以并行运行。
- **更快模型**：对于 <15 分钟的块切换到 `"short"`——处理速度快2-3倍。
- **合并转录稿**：解析 JSON 输出并将它们合并到单个 `.txt` 文件中，带有边界以便阅读。
- **清理**：删除临时块和旧的 GCS blob（如果需要，在循环中添加 `blob.delete()`）。
- **用法**：像以前一样运行，例如，`python script.py --input_file long_audio.m4a --chunk_secs 600`。对于不分割的情况，使用较大的 `--chunk_secs`（例如，3600）。

#### 其他优化

- **并行处理**：如果你有许多块/文件，使用 Python 的 `ThreadPoolExecutor` 并发提交 `run_batch_recognize` 作业（限制在5-10个以避免配额超限）。
- **探测音频持续时间**：使用 `ffprobe`（FFmpeg）动态决定是否需要分割：`ffprobe -v quiet -show_entries format=duration -of csv=p=0 input.m4a`。
- **切换到流式 API**：对于交互式使用，使用同步 `recognize`（限制约1分钟/文件）或流式处理用于实时，但不适合批量长文件。
- **成本/配额**：检查你的 Google Cloud 配额（Speech-to-Text 允许约1000 请求/分钟）。长作业消耗更多积分（标准模型约 $0.036/分钟）。
- **先测试较短文件**：从 `--chunk_secs 300`（5分钟）开始查看加速效果。

### 显示进度：轮询操作

更新的 `poll_operation_with_progress()` 函数替换了阻塞的 `operation.result()`。它：

- 每30秒检查一次。
- 从 `operation.metadata` 打印状态（例如，状态如 "RUNNING" 或 "DONE"，以及已处理的字节数如果可用——Speech API 元数据是基本的，但比没有好）。
- 如果失败则引发错误。

对于更详细的进度（例如，完成百分比），Speech API 不提供细粒度指标，但你可以：

- 通过 Google Cloud Console 监控（你的项目操作页面）。
- 使用 `gcloud` CLI：`gcloud alpha speech operations describe OPERATION_ID --project=graphite-ally-445108-k3`。
- 完成后，JSON 结果通过时间戳间接包括每个话语的进度。

如果进行分割，你会看到来自多个块的交错进度，使其感觉不那么"卡住"。

如果这不能解决你的问题（例如，特定错误），请分享日志/输出以进行更多调整！
