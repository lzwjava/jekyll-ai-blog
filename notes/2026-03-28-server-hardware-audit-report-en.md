---
audio: false
generated: true
image: false
lang: en
layout: post
title: Server Hardware Audit Report
translated: false
type: note
---

Here's the hardware report, Boss 🦞

### 🖥️ Server: 8.129.11.206 (ecs instance)

**CPU:**

- Intel Xeon Platinum 8369B @ 2.90GHz
- 16 vCPUs (8 cores × 2 threads)
- x86_64, supports AVX-512 (full suite including AVX-512VNNI — great for ML inference)

**Memory:**

- 91 GiB total (~94 GiB, matches the spec)
- 90 GiB available — pretty much idle

**GPU:**

- **1 × NVIDIA GeForce RTX 3090** (GA102, Rev A1) detected via PCIe
- 24 GB GDDR6X VRAM
- TFLOPS: ~35.6 FP32 / ~142 FP16 (Tensor Core)
- ⚠️ **No NVIDIA driver loaded** — `nvidia-smi` not available, driver module not present

### Summary

| Component | Status |
| ----------- | -------- |
| CPU | ✅ 16 vCPU, Intel Xeon 8369B, AVX-512 |
| Memory | ✅ 91 GiB, 90 GiB free |
| GPU hardware | ✅ RTX 3090 detected on PCIe |
| GPU driver | ❌ Not installed |

The hardware matches an RTX 3090 setup (not the "G39" from Alibaba docs — likely a region-specific SKU name mapping). The GPU is physically there but needs the NVIDIA driver before you can use it. Want me to install the driver?
