---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google TTS 中的中文语音选项
translated: true
type: note
---

**问题**：对于中文，在 Google Cloud Text-to-Speech 中，我们可以使用哪些类似于 en-US-Journey 语音的语音选项？

**回答**：

Google Cloud Text-to-Speech 支持 **普通话中文**（中国大陆，代码：`cmn-CN` 或 `zh-CN`）和 **香港中文**（粤语，代码：`yue-HK` 或 `zh-HK`）。

与英语不同，目前中文没有 **Journey** 语音（Journey 系列似乎仅限于某些语言，如 en-US、en-GB 等）。

以下是 **普通话中文 (cmn-CN / zh-CN)** 的主要语音选项，您可以在 `VoiceSelectionParams(name=...)` 中使用：

- 标准语音（成本较低，质量良好）：
  - `cmn-CN-Standard-A`（男声）
  - `cmn-CN-Standard-B`（男声）
  - `cmn-CN-Standard-C`（女声）
  - `cmn-CN-Standard-D`（女声）

- 更高质量语音（更自然）：
  - `cmn-CN-Wavenet-A`（男声）
  - `cmn-CN-Wavenet-B`（男声）
  - `cmn-CN-Wavenet-C`（女声）
  - `cmn-CN-Wavenet-D`（女声）
  - `cmn-CN-Neural2-A`（男声）
  - `cmn-CN-Neural2-B`（男声）
  - `cmn-CN-Neural2-C`（女声）
  - `cmn-CN-Neural2-D`（女声）

对于 **香港粤语 (yue-HK / zh-HK)**，选项包括 Standard 语音以及可能的新模型（例如，最近为香港中文添加的四个 Standard 语音）。

要获取完整且最新的列表（因为语音会随着时间添加），在您的代码中运行以下内容：

```python
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
voices = client.list_voices(language_code="cmn-CN")  # 或 "zh-CN", "yue-HK"
for voice in voices.voices:
    print(voice.name, voice.ssml_gender)
```

然后，您可以从类似列表中随机选择：

```python
voice_options = [
    "cmn-CN-Neural2-A", "cmn-CN-Neural2-B",
    "cmn-CN-Neural2-C", "cmn-CN-Neural2-D",
    "cmn-CN-Wavenet-A", "cmn-CN-Wavenet-D",  # 等
]
voice_name = random.choice(voice_options)
```

您的 `language_code` 应为 `"cmn-CN"`（或 `"zh-CN"`）以处理普通话输入文本。

您代码的其余部分（例如，用于 small-bluetooth-speaker-class-device 的 `effects_profile_id`）工作方式相同。

**参考资料**：  

- [Supported voices and languages | Cloud Text-to-Speech](https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types)
- [Cloud Text-to-Speech release notes](https://docs.cloud.google.com/text-to-speech/docs/release-notes)