---
audio: false
generated: true
image: false
lang: en
layout: post
title: MEM 1215 MHz Meaning
translated: false
type: note
---

Question: What does "MEM 1215 MHz" mean in an NVIDIA GPU?

Answer:

**MEM MHz** refers to the **memory clock speed** of your GPU — specifically how fast the VRAM (video RAM) cycles data per second.

**1215 MHz** means the memory chips on your GPU are clocked at 1,215 million cycles per second. However, the *effective* (actual data transfer) speed is much higher depending on the memory type:

| Memory Type | Base Clock | Effective Speed (multiply by) |
| --- | --- | --- |
| GDDR5 | 1215 MHz | × 4 → ~4860 MHz |
| GDDR5X | 1215 MHz | × 8 → ~9720 MHz |
| GDDR6 | 1215 MHz | × 16 → ~19440 MHz |

So the number you see in tools like GPU-Z or nvidia-smi is the **base clock**, not the final bandwidth rate.

**Why it matters:**

- Higher MEM MHz = faster data transfer between VRAM and the GPU cores
- Affects performance in memory-intensive tasks: 4K gaming, AI/ML workloads, video editing
- You can overclock MEM MHz to gain extra performance, but too high causes artifacts or crashes

**1215 MHz specifically** is a common stock clock for mid-range NVIDIA GPUs (e.g., GTX 1060, GTX 1070 era).

References:

- [GPU Memory Clock Explained – GPU-Z](https://www.techpowerup.com/gpuz/)
- [NVIDIA GDDR Memory Types](https://www.nvidia.com/en-us/geforce/graphics-cards/)
