---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA计算能力概述
translated: true
type: note
---

**CC** 代表 **Compute Capability**（或 CUDA Compute Capability）。

它是 NVIDIA 为 GPU 架构特性设定的版本编号：

| CC | Architecture | Era |
|----|-------------|-----|
| **3.0** | Kepler | 2012 |
| **3.5** | Kepler (K80) | 2014 |
| **5.0–5.2** | **Maxwell ← Your M40** | 2015 |
| **6.0–6.2** | Pascal (P100, P40) | 2016 |
| **7.0–7.5** | Volta / Turing (V100, T4) | 2018 |
| **8.0–8.9** | Ampere (A100, A6000) | 2020 |
| **9.0** | Hopper (H100) | 2023 |
| **10.0** | Blackwell | 2024 |

更高的 CC 意味着：
- **更新的 CUDA 特性**（例如 sparse tensor ops、bfloat16 硬件等）
- **框架设定了最低 CC 要求**——PyTorch 和 vLLM 需要 **CC 7.0+**
- **llama.cpp 能够运行**，因为它自行编写原始 CUDA 内核，可以直接针对 CC 5.2

你的 M40（CC 5.2）停留在 **Maxwell 时代**——对现代 ML 框架来说过于老旧，但如果不经过 PyTorch，它依然可以胜任。