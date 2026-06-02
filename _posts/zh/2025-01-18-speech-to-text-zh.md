---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 谷歌云转录
translated: true
type: post
---

我最近尝试了Google Cloud的语音转文字API。以下是我用来执行转录的Python函数。

```python
import os
import argparse
from google.cloud import storage

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

MAX_AUDIO_LENGTH_SECS = 8 * 60 * 60
OUTPUT_DIRECTORY = "assets/transcriptions"


def run_batch_recognize(audio_gcs_uri, output_gcs_folder, language_code="en-US"):
    """
    使用Google Cloud语音转文字批量API转录音频文件。

    参数:
        audio_gcs_uri: 音频文件的GCS URI。
        output_gcs_folder: 存储转录结果的GCS文件夹URI。
        language_code: 转录的语言代码（例如，"en-US", "cmn-CN"）。
    """
    client = SpeechClient()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config={},
        features=cloud_speech.RecognitionFeatures(
            enable_word_confidence=True,
            enable_word_time_offsets=True,
        ),
        model="long",
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
    operation = client.batch_recognize(request=request)

    print("等待操作完成...")
    response = operation.result(timeout=3 * MAX_AUDIO_LENGTH_SECS)
    print(response)


def process_audio_files(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    all_audio_files = [f for f in os.listdir(input_dir) if f.endswith(('.mp3', '.wav', '.m4a'))]
    total_files = len(all_audio_files)
    print(f"待处理的音频文件总数: {total_files}")

    if total_files == 0:
        print(f"在'{input_dir}'目录中未找到音频文件。")
        return

    files_processed = 0

    for filename in all_audio_files:
        audio_file_path = os.path.join(input_dir, filename)
        output_filename = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
        if os.path.exists(output_filename):
            print(f"跳过 {filename}: {output_filename} 已存在。")
            continue
        print(f"\n处理 {files_processed + 1}/{total_files}: {filename}")
        try:
            # 根据文件名后缀确定语言
            if filename.endswith('-zh.mp3') or filename.endswith('-zh.wav') or filename.endswith('-zh.m4a'):
                language_code = "cmn-CN"
            else:
                language_code = "en-US"

            # 构建GCS URI
            gcs_audio_uri = f"gs://test2x/audio-files/{filename}"  # 替换为你的存储桶和文件夹
            gcs_output_uri = f"gs://test2x/transcripts/{os.path.splitext(filename)[0]}" # 替换为你的存储桶和文件夹

            # 如果文件不存在，则上传到GCS
            # 这部分未实现，你需要添加代码将文件上传到GCS
            # 例如，使用google-cloud-storage库

            storage_client = storage.Client()
            bucket = storage_client.bucket("test2x")
            blob = bucket.blob(f"audio-files/{filename}")
            if not blob.exists():
                blob.upload_from_filename(audio_file_path)
                print(f"已上传 {filename} 到GCS。")
            else:
                print(f"{filename} 已存在于GCS中。")


            run_batch_recognize(
                audio_gcs_uri=gcs_audio_uri,
                output_gcs_folder=gcs_output_uri,
                language_code=language_code
            )
            files_processed += 1
            print(f"文件 {files_processed}/{total_files} 已处理。\n")

            # 下载转录结果
            output_gcs_uri_json = f"{gcs_output_uri}/{os.path.splitext(filename)[0]}_transcript_*.json"

            blobs = storage_client.list_blobs("test2x", prefix=f"transcripts/{os.path.splitext(filename)[0]}")

            for blob in blobs:
                if blob.name.endswith(".json"):
                    local_output_path = os.path.join(output_dir, os.path.basename(blob.name))
                    blob.download_to_filename(local_output_path)
                    print(f"已下载 {blob.name} 到 {local_output_path}")


        except Exception as e:
            print(f"处理 {filename} 失败: {e}")
            continue

    print(f"处理完成！{files_processed}/{total_files} 文件已处理。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="处理音频文件以生成转录。")
    parser.add_argument('--input_dir', type=str, default="assets/audios", help="音频文件的输入目录。")

    args = parser.parse_args()

    process_audio_files(
        input_dir=args.input_dir,
        output_dir=OUTPUT_DIRECTORY,
    )

```

结果。修改为显示JSON输出的示例，部分值已省略以保持简洁。完整的JSON将包含更详细的信息。

```json
{
    "results": [
        {
            "alternatives": [
                {
                    "transcript": "Here's To The Crazy Ones The Misfits the Rebels the troublemakers the round pegs in the square holes the ones who see things differently they're not fond of rules and they have no respect for the status quo",
                    "confidence": 0.95684826,
                    "words": [
                        {
                            "startOffset": "1s",
                            "endOffset": "4.200s",
                            "word": "Here's",
                            "confidence": 0.8265989
                        },
                        {
                            "startOffset": "4.200s",
                            "endOffset": "4.400s",
                            "word": "To",
                            "confidence": 0.9994259
                        },
                        {
                            "startOffset": "4.400s",
                            "endOffset": "4.400s",
                            "word": "The",
                            "confidence": 0.9994259
                        },
                        {
                            "startOffset": "4.400s",
                            "endOffset": "4.900s",
                            "word": "Crazy",
                            "confidence": 0.9975712
                        },
                        {
                            "startOffset": "4.900s",
                            "endOffset": "5.100s",
                            "word": "Ones",
                            "confidence": 0.9904002
                        },
                        {
                            "startOffset": "5.100s",
                            "endOffset": "6.700s",
                            "word": "The",
                            "confidence": 0.9994307
                        },
                        {
                            "startOffset": "6.700s",
                            "endOffset": "7.200s",
                            "word": "Misfits",
                            "confidence": 0.9352707
                        },
                        {
                            "startOffset": "7.200s",
                            "endOffset": "8.400s",
                            "word": "the",
                            "confidence": 0.99881697
                        },
                        {
                            "startOffset": "8.400s",
                            "endOffset": "8.800s",
                            "word": "Rebels",
                            "confidence": 0.9900544
                        },
                        {
                            "startOffset": "8.800s",
                            "endOffset": "10.300s",
                            "word": "the",
                            "confidence": 0.99904335
                        }
                    ]
                }
            ],
            "resultEndOffset": "23.780s",
            "languageCode": "en-us"
        }
    ]
}
```
