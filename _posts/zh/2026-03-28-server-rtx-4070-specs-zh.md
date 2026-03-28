---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 服务器 RTX 4070 参数规格与状态
translated: true
type: note
---

等等 —— 原来这**确实**是在你的服务器（`lzw-server`）上，而不是在笔记本电脑上。它配置了一块 **RTX 4070**（不是 Ti）：

| Spec | Value |
|---|---|
| **GPU** | NVIDIA GeForce RTX 4070 |
| **VRAM** | 12 GB GDDR6X (213 MiB in use) |
| **Driver** | 535.288.01 / CUDA 12.2 |
| **Temp** | 43°C (idle, chillin) |
| **Power** | 10W / 215W (barely breaking a sweat) |
| **Utilization** | 0% |

**理论 FLOPS (RTX 4070):**
- **FP32:** ~29.1 TFLOPS
- **FP16:** ~58.2 TFLOPS  
- **Tensor Cores (FP16, sparse):** ~233 TFLOPS

目前只有 Xorg 和 gnome-shell 在使用 GPU（总计约 207 MiB）。它基本上正无所事事地闲着。

所以你的**笔记本电脑**配备的是 4070 Ti —— 而这台服务器配备的是普通的 4070。想让这家伙开始干活吗？