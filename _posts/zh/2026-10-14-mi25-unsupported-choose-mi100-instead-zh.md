---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI25 不支持：请改用 MI100
translated: true
type: note
---

### 那非官方 workarounds 呢？

一些社区项目和老旧的软件栈可能支持未受支持的 GPU，但能否在 MI25 上成功取决于 ROCm 版本以及具体应用的 kernels。

对于 MI25，其 GPU 目标是 `gfx900`。AMD 的官方文档明确将其标记为 **不支持**，无论是在 ROCm 6.1 还是当前文档中。[AMD ROCm](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.1.5/reference/system-requirements.html?utm_source=chatgpt.com)

如果你要买一张二手卡用于 AI，我会优先考虑：

| GPU | VRAM | ROCm 支持情况 |
|---|---:|---|
| Instinct MI25 | 16GB | 官方不支持 |
| Instinct MI50 | 16GB/32GB | 旧版；当前官方支持已移除 |
| Instinct MI100 | 32GB | 官方支持 |
| Instinct MI210 | 64GB | 官方支持 |

参见 AMD 的 [GPU 兼容性文档](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html)。

**我的建议：** 如果你找到一张价格极低的 MI25，请将其视为一个硬件/软件 hacking 项目，而不是一个可靠的 ROCm 加速器。如果你想要一块较老的 AMD GPU 来进行认真的 PyTorch 实验，MI100 是更安全的选择。