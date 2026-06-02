---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复适用于谷歌语音API的AAC M4A文件
translated: true
type: note
---

是的——你的文件是 **M4A 容器中的 AAC 编码**（iPhone 语音备忘录）。Google Speech-to-Text v2 批量识别经常无法自动解码 AAC/M4A 并返回该错误。请先转换为支持的编解码器/容器——然后可以保留 `AutoDetectDecodingConfig()` 或（更推荐）显式指定解码配置。

这是最快捷的解决方案。

## 方案 A — 使用 `ffmpeg 一键修复（推荐：Ogg/Opus）

文件小，准确率高，官方支持。

```bash
# 48 kHz，单声道，OGG 容器中的 Opus 编码
ffmpeg -i ~/Downloads/haifeng_and_zhiwei.m4a -vn -ac 1 -ar 48000 -c:a libopus -b:a 48k ~/Downloads/haifeng_and_zhiwei.ogg
```

然后对新文件运行脚本：

```bash
python scripts/agent/speech_to_text_agent.py --input_file ~/Downloads/haifeng_and_zhiwei.ogg
```

## 方案 B — 无损 FLAC（同样支持）

比 WAV 小；无损。

```bash
ffmpeg -i ~/Downloads/haifeng_and_zhiwei.m4a -vn -ac 1 -ar 48000 -sample_fmt s16 -c:a flac ~/Downloads/haifeng_and_zhiwei.flac
```

## 方案 C — Linear16 WAV（文件最大）

```bash
ffmpeg -i ~/Downloads/haifeng_and_zhiwei.m4a -vn -ac 1 -ar 16000 -sample_fmt s16 -c:a pcm_s16le ~/Downloads/haifeng_and_zhiwei.wav
```

---

## 代码调整（避免再次遇到此问题）

1. **允许更多扩展名**并保持相同的语言检测逻辑
2. **自动转码**为支持的格式（我使用 Ogg/Opus）
3. **明确告知 API 发送的格式**（显式解码配置）

将以下代码加入你的脚本（最小化聚焦修改）：

```python
import subprocess
import tempfile
from pathlib import Path
from google.cloud.speech_v2.types import cloud_speech

SUPPORTED_EXTS = {".ogg", ".flac", ".wav", ".mp3"}  # mp3 也支持

def _transcode_to_ogg_opus(src_path: str) -> str:
    src = Path(src_path)
    dst = src.with_suffix(".ogg")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(src),
        "-vn",
        "-ac", "1",
        "-ar", "48000",
        "-c:a", "libopus",
        "-b:a", "48k",
        str(dst),
    ]
    subprocess.run(cmd, check=True)
    return str(dst)

def run_batch_recognize(audio_gcs_uri, output_gcs_folder, language_code="en-US", decoding="ogg_opus"):
    client = SpeechClient()

    # 优先使用显式解码——避免“不支持的编码”问题
    if decoding == "ogg_opus":
        decoding_cfg = cloud_speech.ExplicitDecodingConfig(
            ogg_opus=cloud_speech.OggOpusDecodingConfig()
        )
    elif decoding == "flac":
        decoding_cfg = cloud_speech.ExplicitDecodingConfig(
            flac=cloud_speech.FlacDecodingConfig()
        )
    elif decoding == "linear16":
        decoding_cfg = cloud_speech.ExplicitDecodingConfig(
            linear16=cloud_speech.Linear16DecodingConfig()
        )
    else:
        decoding_cfg = cloud_speech.AutoDetectDecodingConfig()  # 回退方案

    config = cloud_speech.RecognitionConfig(
        explicit_decoding_config=decoding_cfg,
        features=cloud_speech.RecognitionFeatures(
            enable_word_confidence=True,
            enable_word_time_offsets=True,
        ),
        model="long",
        language_codes=[language_code],
        # 可选：说话人分离、标点等
        # speech_adaptation=...
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
    print("Waiting for operation to complete...")
    response = client.batch_recognize(request=request).result(timeout=3 * MAX_AUDIO_LENGTH_SECS)
    print(response)

def process_audio_file(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    src = Path(input_file)
    if not src.exists():
        print(f"Error: {src} does not exist.")
        return

    # 通过后缀决定语言
    language_code = "cmn-CN" if src.name.endswith("-zh" + src.suffix) else "en-US"

    # 确保编码/容器支持
    if src.suffix.lower() not in SUPPORTED_EXTS:
        print(f"Transcoding {src.name} to Ogg/Opus...")
        input_file = _transcode_to_ogg_opus(str(src))
        src = Path(input_file)

    # 本地 .txt 输出的门控逻辑（可保持原样或基于 stem 判断）
    output_filename = os.path.join(output_dir, f"{src.stem}.txt")
    if os.path.exists(output_filename):
        print(f"Skipping {src.name}: {output_filename} already exists.")
        return

    print(f"Processing: {src.name}")

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket("test2x")
        # 保持 "audio-files/" 文件夹，保留真实文件名（含新扩展名）
        blob = bucket.blob(f"audio-files/{src.name}")
        if not blob.exists():
            blob.upload_from_filename(str(src))
            print(f"Uploaded {src.name} to GCS.")
        else:
            print(f"{src.name} already exists in GCS.")

        gcs_audio_uri = f"gs://test2x/audio-files/{src.name}"
        gcs_output_uri = f"gs://test2x/transcripts/{src.stem}"

        # 根据扩展名选择解码方式
        ext = src.suffix.lower()
        if ext == ".ogg":
            decoding = "ogg_opus"
        elif ext == ".flac":
            decoding = "flac"
        elif ext == ".wav":
            decoding = "linear16"
        else:
            decoding = None  # 回退到自动检测

        run_batch_recognize(
            audio_gcs_uri=gcs_audio_uri,
            output_gcs_folder=gcs_output_uri,
            language_code=language_code,
            decoding=decoding,
        )

        print(f"File {src.name} processed.\n")

        # 下载转录 JSON 文件
        blobs = storage_client.list_blobs("test2x", prefix=f"transcripts/{src.stem}")
        for b in blobs:
            if b.name.endswith(".json"):
                local_output_path = os.path.join(output_dir, os.path.basename(b.name))
                b.download_to_filename(local_output_path)
                print(f"Downloaded {b.name} to {local_output_path}")

    except Exception as e:
        print(f"Failed to process {src.name}: {e}")

    print(f"Processing complete for {src.name}.")
```

### 为什么这个方案有效

* iOS 语音备忘录 → **AAC/M4A**。批量 STT v2 无法可靠地自动检测/解码该格式
* 通过转码为 **OGG/Opus**（或 **FLAC/WAV**）并**明确告知 API 编解码格式**，你可以完全避免“不支持的编码”错误

### 实用建议

* 对于像你 **1 小时 21 分钟单声道语音备忘录**这样的长录音，**OGG/Opus 48k** 能在保持质量的同时减小文件大小和 GCS 出口流量
* 保持单声道（`-ac 1`）。立体声只会使成本翻倍而无助于识别
* 如果对话是普通话，你的 `"cmn-CN"` 代码是正确的；按你现有的做法使用 `"-zh.m4a"` 命名约定
* 如果需要说话人分离，稍后启用该功能；先修复解码路径

如果需要，我还可以添加可选的**自动本地 → GCS 上传 + 重命名**功能，这样你的 `m4a` 输入文件会被接受，但在后台始终以内部 `.ogg` 格式处理。
