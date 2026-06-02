---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix OGG Opus Decoding Errors Easily
translated: false
type: note
---

Short answer: don’t set `audio_channel_count` (or `sample_rate_hertz`) in `ExplicitDecodingConfig` for your OGG/Opus. That’s what’s tripping v2 with:

```
explicit_decoding_config.audio_channel_count: audio_channel_count is out of range
```

## What to change (code)

In your `.ogg` branch, build the config **without** channels/rate so the service infers them:

```python
if file_extension == "ogg":
    # Keep only the encoding; let STT infer rate/channels.
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

> If you **know for sure** the file is stereo/48 kHz Opus, you may set `sample_rate_hertz=48000` and `audio_channel_count=2`. Otherwise, omit both—don’t guess.

---

## Should you pre-process with ffmpeg?

You don’t have to if the above change works. But if you still see decoding complaints (mixed streams, odd container, variable channels), transcoding to a “boring” format makes the batch API very happy. Either of these is safe:

### Option A: FLAC (lossless, preferred)

```bash
ffmpeg -y -i haifeng_and_zhiwei.ogg -ac 1 -ar 16000 -c:a flac haifeng_and_zhiwei.flac
```

### Option B: Linear16 WAV (lossless)

```bash
ffmpeg -y -i haifeng_and_zhiwei.ogg -ac 1 -ar 16000 -c:a pcm_s16le haifeng_and_zhiwei.wav
```

Then upload that file to the same GCS bucket and run with **`auto_decoding_config`** (no explicit decoding needed for FLAC/WAV):

```python
# for .flac or .wav
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

## Quick sanity checks

* Make sure your language tag is valid BCP-47. For Mandarin you can use `"cmn-CN"` or `"cmn-Hans-CN"`.
* Keep filenames simple (ASCII) to avoid odd container metadata.
* If you want to confirm channels/rate before deciding, you can inspect with:

  ```bash
  ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,channels,sample_rate -of default=nw=1 haifeng_and_zhiwei.ogg
  ```

**Bottom line:** First try removing `audio_channel_count` (and `sample_rate_hertz`). If it still fails, transcode to FLAC/WAV and switch to `auto_decoding_config`.
