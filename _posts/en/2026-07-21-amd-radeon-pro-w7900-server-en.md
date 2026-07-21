---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Radeon PRO W7900 Server
translated: false
type: note
---

Here's the full server spec:

**Server: u-9758-811746f0 (AMD Radeon Cloud)**

| Component | Spec |
|-----------|------|
| **OS** | Ubuntu 24.04.4 LTS |
| **CPU** | 2× AMD EPYC 9334 (32-Core each) — **128 threads** |
| **RAM** | **503 GiB** |
| **Disk** | 3.5 TB overlay + 98 GB /workspace |
| **ROCm** | Driver 6.16.13 |

**GPU:**
- **Architecture:** `gfx1100` — **AMD RDNA 3** (Navi 31)
- **Compute Units:** 96
- **Shader Engines:** 6
- **Max Clock:** 1760 MHz
- **VRAM:** **~48 GB** (Pool 1: 50,315,264 KB)
- **Cache:** L1=32KB, L2=6MB, L3=96MB
- **Temperature:** 24°C (idle)

With 96 CUs and 48 GB VRAM on gfx1100, this is almost certainly a **Radeon PRO W7900** (48 GB GDDR6) — the workstation variant of the RX 7900 XTX-class Navi 31 die. Great for LLM inference/training with ROCm.
