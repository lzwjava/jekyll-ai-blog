---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: FLAC 无损音频格式详解
translated: true
type: note
---

Question: What is an introduction to the FLAC audio format?

Answer:

**FLAC** (Free Lossless Audio Codec) 是一种流行的 **open-source** 音频格式，专为数字音频的 **lossless compression** 而设计。

### Core Concept
FLAC 压缩音频文件（通常将其减小到原始大小的 **50–70%**），而不会丢失 **任何** 音频信息。当你解压（播放）一个 FLAC 文件时，你会得到与原始未压缩音频（通常是来自 CD 或高分辨率录音的 PCM 数据）完全一致的 **bit-perfect** 副本。

这与以下 lossy 格式有很大不同：
- MP3
- AAC
- Opus（通常使用下）

这些格式会永久移除“较不重要”的数据以实现更小的体积，这会引入一定的质量损失。

### History
- 首次发布于 **2001** 年（2001 年 7 月发布 1.0 版本）
- 由 **Xiph.Org Foundation** 开发和维护
- 在 **2024** 年底成为正式的 IETF 标准 (RFC 9639)
- 保持完全的 **royalty-free**、无专利且 open-source

### Main Features and Advantages
- **Truly lossless** — 数学上可验证的位一致重构
- 对大多数音乐具有出色的压缩率（比 ZIP 处理音频效果更好）
- 极快的 decoding 速度（低 CPU 占用） — 适合实时播放
- 支持高分辨率音频：
  - Sample rates 最高可达 **1,048,575 Hz**（理论值）
  - Bit depths 最高可达 **32 bits**
  - 1–8 声道
- 内置 **error detection**（原始音频的 MD5 checksum）
- 支持 **metadata** (tags) — Vorbis comments（与 Ogg Vorbis 相同）
- **Streamable** — 适合互联网流媒体
- Hardware support — 在 2025–2026 年极其广泛（几乎涵盖所有现代 DAP、许多汽车主机、AV receivers、智能扬声器、智能手机等）
- 存在多个独立的实现方案（非常健壮的生态系统）

### Typical Use Cases (2026)
- 以完美质量归档 CD 收藏，且文件比 WAV 更小
- 存储高解析音频 (24-bit/96 kHz, 24-bit/192 kHz 等)
- 在本地存储（手机、DAPs、NAS → streamer setups）上进行发烧级聆听
- 一些高质量音乐流媒体服务提供 FLAC（特别是 lossless/hi-res 档位）
- 许多销售无损文件的音乐下载商店的首选格式

### Comparison Table (rough real-world averages)

| Format     | Type      | CD (1411 kbps) size | Hi-res example size | Quality after decode | Patent/Royalty-free |
|------------|-----------|----------------------|----------------------|----------------------|---------------------|
| WAV        | Uncompressed | ~100%               | ~100%               | Perfect             | Yes                |
| **FLAC**   | Lossless  | ~40–70%             | ~45–75%             | Perfect             | Yes                |
| Apple ALAC | Lossless  | ~45–75%             | ~50–80%             | Perfect             | Yes (open spec)    |
| MP3 (320)  | Lossy     | ~20–25%             | Not recommended     | Some loss           | Yes                |
| AAC (256)  | Lossy     | ~18–22%             | Not recommended     | Some loss           | No (patents)       |

### File Extension and Identification
- Extension: **.flac**
- Magic number (first bytes): **`fLaC`**

总之，FLAC 在 2026 年仍然是开放、免版税、高质量 lossless 音频存储和播放的 **de facto standard** — 它结合了出色的音质、合理的体积和极广泛的兼容性。

References:

- [https://xiph.org/flac](https://xiph.org/flac)
- [https://en.wikipedia.org/wiki/FLAC](https://en.wikipedia.org/wiki/FLAC)
- [https://datatracker.ietf.org/doc/rfc9639](https://datatracker.ietf.org/doc/rfc9639)
