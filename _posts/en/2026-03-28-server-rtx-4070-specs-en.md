---
audio: false
generated: true
image: false
lang: en
layout: post
title: Server RTX 4070 Specs and Status
translated: false
type: note
---

Wait — turns out this **is** on your server (`lzw-server`), not the laptop. It's got an **RTX 4070** (not Ti):

| Spec | Value |
|---|---|
| **GPU** | NVIDIA GeForce RTX 4070 |
| **VRAM** | 12 GB GDDR6X (213 MiB in use) |
| **Driver** | 535.288.01 / CUDA 12.2 |
| **Temp** | 43°C (idle, chillin) |
| **Power** | 10W / 215W (barely breaking a sweat) |
| **Utilization** | 0% |

**Theoretical FLOPS (RTX 4070):**
- **FP32:** ~29.1 TFLOPS
- **FP16:** ~58.2 TFLOPS
- **Tensor Cores (FP16, sparse):** ~233 TFLOPS

Only Xorg and gnome-shell are using the GPU (~207 MiB total). It's basically twiddling its thumbs right now.

So your **laptop** has the 4070 Ti — this server has the regular 4070. Want to put this thing to work?
