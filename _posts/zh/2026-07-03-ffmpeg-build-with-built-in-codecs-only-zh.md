---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 仅内置编解码器的FFmpeg构建
translated: true
type: note
---

构建完成。摘要如下：

- **Commit**: `14ed5e8` (2026-07-02)
- **Compiler**: GCC 13 (Ubuntu 24.04)
- **Configuration**: `--enable-gpl --enable-version3 --enable-nonfree`
- **Binaries**: `ffmpeg` (29 MB), `ffprobe` (29 MB)
- **Libraries**: libavutil 61.2, libavcodec 63.3, libavformat 63.3, libavdevice 63.2, libavfilter 12.2, libswscale 10.2, libswresample 7.2

二进制文件位于项目根目录，文件名为 `ffmpeg` 和 `ffprobe`。由于未安装相应的 `-dev` 包，未链接任何外部编解码库（如 x264、x265 等）——此次构建仅包含 FFmpeg 内置的编解码器。如果您需要 libx264 或 libmp3lame 等外部编码器，请安装对应的 `-dev` 包，然后重新运行 configure 和 make。
