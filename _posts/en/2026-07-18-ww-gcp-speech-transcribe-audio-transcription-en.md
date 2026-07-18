---
audio: false
generated: true
image: false
lang: en
layout: post
title: ww gcp-speech transcribe audio transcription
translated: false
type: note
---

It's already wired into the `ww` CLI under the `gcp-speech` group. The command is:

```
ww gcp-speech transcribe <audio_file> [options]
```

**Arguments:**

- `<audio_file>` — path to audio file (mp3, m4a, wav, ogg, mp4, etc.)
- `--lang LANG` — language code override (default: auto-detect from filename suffix: `-zh`/`-cn` → Chinese, otherwise English)
- `--wait` — wait for the job to finish and download results (default is async: submit, print console link, exit)

**Examples:**

```sh
ww gcp-speech transcribe ~/Downloads/recording.mp3
ww gcp-speech transcribe ~/Downloads/recording-zh.mp3 --lang cmn-Hans-CN
ww gcp-speech transcribe ~/Downloads/long.mp3 --wait
```

It uploads the audio to GCS (`test2x` bucket), submits a batch job via Google Cloud Speech-to-Text v2, and either prints a console link (async) or polls for the result and saves a `.md` transcript alongside the audio file (`--wait`).
