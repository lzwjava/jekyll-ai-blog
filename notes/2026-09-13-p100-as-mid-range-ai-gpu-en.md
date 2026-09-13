---
audio: false
generated: true
image: false
lang: en
layout: post
title: P100 as Mid-Range AI GPU
translated: false
type: note
---

No search needed — P100 specs are well established:

| Spec | Tesla M60 | Tesla P100 | Tesla V100 | RTX 4070 |
| --- | --- | --- | --- | --- |
| Architecture | Maxwell (2015) | Pascal (2016) | Volta (2017) | Ada Lovelace (2023) |
| CUDA Cores | 4,096 | 3,584 | 5,120 | 5,888 |
| **FP32 Compute** | **~8.1 TFLOPS** | **~10.6 TFLOPS** | **~15.7 TFLOPS** | **29.15 TFLOPS** |
| **FP16 Compute** | **~8.1 TFLOPS** | **~21.2 TFLOPS** | **~125 TFLOPS** | **~116 TFLOPS** |
| VRAM | 16GB GDDR5 | 16GB HBM2 | 16GB HBM2 | 12GB GDDR6X |
| Memory Bandwidth | ~160 GB/s | **~732 GB/s** | **~900 GB/s** | 504 GB/s |
| Tensor Cores | None | None | 640 (1st gen) | 184 (4th gen) |
| TDP | ~300W | ~250W | ~250W | 200W |

**Key observations:**

- FP32-wise, the P100 (~10.6 TFLOPS) edges out the M60 but is meaningfully behind the V100.
- Like the V100, the P100's **HBM2 bandwidth (~732 GB/s)** is its biggest strength — great for inference throughput.
- However, the P100 has **no Tensor Cores**, so FP16 is only ~21 TFLOPS (native FP16, not accelerated), versus the V100's ~125 TFLOPS with Tensor Cores. This is a significant gap for AI workloads.

**Ranking for AI/LLM use at this price tier:**

1. 🥇 **V100** — best overall (Tensor Cores + HBM2 bandwidth)
2. 🥈 **P100** — great bandwidth, no Tensor Cores but still solid for inference
3. 🥉 **M60** — weakest; only advantage is availability at very low price

The P100 typically sells for **400–700 CNY** secondhand, putting it between the M60 and V100 in both price and performance — a reasonable middle ground if V100 units are unavailable locally.
