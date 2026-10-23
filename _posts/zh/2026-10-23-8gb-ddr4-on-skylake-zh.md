---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Skylake平台上的8GB DDR4内存
translated: true
type: note
---

**DDR4.** 在 `.137` 上：

- **类型：DDR4**
- 安装了 **1× 8 GB 内存条**（3 个空插槽）
- 内存条标称 **DDR4-2400**（CL16-16-16 时序），当前运行在 **2133 MT/s**（Q170/Skylake 平台上的默认 JEDEC 速度）
- 1.2 V 标准 DDR4 电压

这对该代硬件来说很合理——i5-6500（Skylake，LGA1151）+ Q170 芯片组是 DDR4 时代的主板，并且与 `free` 显示的 7.7 GiB 相符。

所以考虑到 H3 的限制：8 GB DDR4 内存条是 RAM bottleneck 的一个重要部分——提升到 16/32 GB（4 个插槽上 4×8 最高可达 64 GB）将有助于主机端 offload，但 GPU 上的 24 GB VRAM 和 Maxwell 架构的限制仍然是 hard blockers。

要不要我顺便也检查一下 `.34` 上的 RAM 类型？
