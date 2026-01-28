---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Chinese Voice Options in Google TTS
translated: false
type: note
---

Question: For Chinese, what voice options can we use in Google Cloud Text-to-Speech similar to the en-US-Journey voices?

Answer: 

Google Cloud Text-to-Speech supports **Mandarin Chinese** (Mainland China, code: `cmn-CN` or `zh-CN`) and **Chinese (Hong Kong)** (Cantonese, code: `yue-HK` or `zh-HK`).

Unlike English, there are currently no **Journey** voices available for Chinese (the Journey series appears limited to certain languages like en-US, en-GB, etc.).

Here are the main voice options for **Mandarin Chinese (cmn-CN / zh-CN)** that you can use in `VoiceSelectionParams(name=...)`:

- Standard voices (lower cost, good quality):
  - `cmn-CN-Standard-A` (Male)
  - `cmn-CN-Standard-B` (Male)
  - `cmn-CN-Standard-C` (Female)
  - `cmn-CN-Standard-D` (Female)

- Higher quality voices (more natural):
  - `cmn-CN-Wavenet-A` (Male)
  - `cmn-CN-Wavenet-B` (Male)
  - `cmn-CN-Wavenet-C` (Female)
  - `cmn-CN-Wavenet-D` (Female)
  - `cmn-CN-Neural2-A` (Male)
  - `cmn-CN-Neural2-B` (Male)
  - `cmn-CN-Neural2-C` (Female)
  - `cmn-CN-Neural2-D` (Female)

For **Hong Kong Cantonese (yue-HK / zh-HK)**, options include Standard and possibly newer models (e.g., recent additions of four Standard voices for Chinese (Hong Kong)).

To get the full and up-to-date list (as voices are added over time), run this in your code:

```python
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
voices = client.list_voices(language_code="cmn-CN")  # or "zh-CN", "yue-HK"
for voice in voices.voices:
    print(voice.name, voice.ssml_gender)
```

You can then randomly select from a list like:

```python
voice_options = [
    "cmn-CN-Neural2-A", "cmn-CN-Neural2-B",
    "cmn-CN-Neural2-C", "cmn-CN-Neural2-D",
    "cmn-CN-Wavenet-A", "cmn-CN-Wavenet-D",  # etc.
]
voice_name = random.choice(voice_options)
```

Your `language_code` should be `"cmn-CN"` (or `"zh-CN"`) for Mandarin input text.

The rest of your code (e.g., `effects_profile_id` for small-bluetooth-speaker-class-device) works the same way.

References:  

- [Supported voices and languages | Cloud Text-to-Speech](https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types)
- [Cloud Text-to-Speech release notes](https://docs.cloud.google.com/text-to-speech/docs/release-notes)