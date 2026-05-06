---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Whisper CLI转录音频
translated: true
type: note
---

文件和 `whisper` CLI 均已存在。基本命令：

```bash
whisper "meeting_01 2.mp4" --model small --output_format txt --output_dir .
```

实用调整：
- `--model` — `tiny`、`base`、`small`、`medium`、`large-v3`（越大越慢，但越准确）
- `--language en` — 如果已知语言，可跳过自动检测
- `--output_format` — `txt`、`srt`、`vtt`、`json` 或 `all`
- `--device cuda` — 如果有 GPU（默认为 CPU）
- `--fp16 False` — 在 CPU 上需要以避免警告

适用于 CPU 的示例：

```bash
whisper "meeting_01 2.mp4" --model small --language en --fp16 False --output_format txt --output_dir .
```

这会在当前目录下生成 `meeting_01 2.txt`（其他格式使用相同基本文件名）。需要我运行它吗？