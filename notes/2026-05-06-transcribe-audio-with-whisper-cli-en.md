---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transcribing Audio with Whisper CLI
translated: false
type: note
---

File and `whisper` CLI are both present. Basic command:

```bash
whisper "meeting_01 2.mp4" --model small --output_format txt --output_dir .
```

Useful tweaks:
- `--model` — `tiny`, `base`, `small`, `medium`, `large-v3` (bigger = slower, more accurate)
- `--language en` — skip auto-detection if you know the language
- `--output_format` — `txt`, `srt`, `vtt`, `json`, or `all`
- `--device cuda` — if you have a GPU (default is CPU)
- `--fp16 False` — required on CPU to avoid a warning

CPU-friendly example:

```bash
whisper "meeting_01 2.mp4" --model small --language en --fp16 False --output_format txt --output_dir .
```

This writes `meeting_01 2.txt` (and same basename for other formats) into the current directory. Want me to run it?
