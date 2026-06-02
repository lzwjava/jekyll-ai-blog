---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 轻松修复OGG Opus解码错误
translated: true
type: note
---

简短回答：不要在 `ExplicitDecodingConfig` 中为 OGG/Opus 文件设置 `audio_channel_count`（或 `sample_rate_hertz`）。这就是导致 v2 报错的原因：

```
explicit_decoding_config.audio_channel_count: audio_channel_count 超出范围
```

## 需要修改的内容（代码）

在你的 `.ogg` 分支中，构建配置时**不要**指定声道数/采样率，让服务自动推断：

```python
if file_extension == "ogg":
    # 只保留编码格式；让 STT 推断采样率/声道数。
    decoding = cloud_speech.ExplicitDecodingConfig(
        encoding=cloud_speech.ExplicitDecodingConfig.AudioEncoding.OGG_OPUS
    )
    config = cloud_speech.RecognitionConfig(
        explicit_decoding_config=decoding,
        features=cloud_speech.RecognitionFeatures(
            enable_word_confidence=True,
            enable_word_time_offsets=True,
        ),
        model="long",
        language_codes=[language_code],
    )
else:
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        features=cloud_speech.RecognitionFeatures(
            enable_word_confidence=True,
            enable_word_time_offsets=True,
        ),
        model="long",
        language_codes=[language_code],
    )
```

> 如果你**确定**文件是立体声/48 kHz 的 Opus 格式，可以设置 `sample_rate_hertz=48000` 和 `audio_channel_count=2`。否则，请省略这两个参数——不要猜测。

---

## 是否需要使用 ffmpeg 进行预处理？

如果上述修改有效，就不需要。但如果仍然出现解码问题（混合流、异常容器、可变声道数），将其转码为"简单"格式会让批处理 API 更稳定。以下两种方式都是安全的：

### 选项 A：FLAC（无损，推荐）

```bash
ffmpeg -y -i haifeng_and_zhiwei.ogg -ac 1 -ar 16000 -c:a flac haifeng_and_zhiwei.flac
```

### 选项 B：Linear16 WAV（无损）

```bash
ffmpeg -y -i haifeng_and_zhiwei.ogg -ac 1 -ar 16000 -c:a pcm_s16le haifeng_and_zhiwei.wav
```

然后将文件上传到同一个 GCS 存储桶，并使用 **`auto_decoding_config`**（FLAC/WAV 不需要显式解码配置）：

```python
# 适用于 .flac 或 .wav 文件
config = cloud_speech.RecognitionConfig(
    auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
    features=cloud_speech.RecognitionFeatures(
        enable_word_confidence=True,
        enable_word_time_offsets=True,
    ),
    model="long",
    language_codes=[language_code],
)
```

---

## 快速检查项

* 确保语言标签是有效的 BCP-47 格式。对于普通话，可以使用 `"cmn-CN"` 或 `"cmn-Hans-CN"`。
* 保持文件名简单（使用 ASCII 字符），避免容器元数据异常。
* 如果需要在决策前确认声道数/采样率，可以使用以下命令检查：

  ```bash
  ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,channels,sample_rate -of default=nw=1 haifeng_and_zhiwei.ogg
  ```

**总结：** 首先尝试移除 `audio_channel_count`（和 `sample_rate_hertz`）。如果仍然失败，请转码为 FLAC/WAV 格式并切换到 `auto_decoding_config`。
