---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gitignore仅保留源文件
translated: true
type: note
---

在 `/Users/lzwjava/projects/video-factory/` 中创建了 `.gitignore`。Git status 确认只有源文件/文本文件保持可见——所有 binaries 和 generated artifacts 现在都被忽略了：

- **macOS junk**: `.DS_Store`
- **Audio + derived transcription files**: `deliver.m4a`, `deliver.wav`, `deliver.wav.{srt,txt,vtt}`
- **Generated dirs**: `whisper_out/`, `output/` (video + segments), `slides/` (rendered PNGs)
- **Font binaries**: `fonts/`

保留在 version control 中：`build_video.py`, `render_slides.py`, `scenes.json`, `transcript.md`, `deliver-transcription.md`, 和 `.gitignore` 本身。

一点说明：我忽略了 `fonts/`，因为它们是 2MB 的 binary files——如果你更愿意将它们作为 build dependencies 提交，请删除那一行。