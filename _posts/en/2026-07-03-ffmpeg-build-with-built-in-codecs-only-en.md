---
audio: false
generated: true
image: false
lang: en
layout: post
title: FFmpeg Build with Built-in Codecs Only
translated: false
type: note
---

Build complete. Here's the summary:

- **Commit**: `14ed5e8` (2026-07-02)
- **Compiler**: GCC 13 (Ubuntu 24.04)
- **Configuration**: `--enable-gpl --enable-version3 --enable-nonfree`
- **Binaries**: `ffmpeg` (29 MB), `ffprobe` (29 MB)
- **Libraries**: libavutil 61.2, libavcodec 63.3, libavformat 63.3, libavdevice 63.2, libavfilter 12.2, libswscale 10.2, libswresample 7.2

The binaries are in the project root as `ffmpeg` and `ffprobe`. No external codec libraries (x264, x265, etc.) were linked since their `-dev` packages aren't installed — the build includes only FFmpeg's built-in codecs. If you need external encoders like libx264 or libmp3lame, install the corresponding `-dev` packages and re-run configure + make.