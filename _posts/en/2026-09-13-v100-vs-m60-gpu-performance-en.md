---
audio: false
generated: true
image: false
lang: en
layout: post
title: V100 vs M60 GPU Performance
translated: false
type: note
---

**Question:** What is the Tesla V100's FP32 compute performance?

**Answer:**

No search needed — the V100 specs are well established:

| Spec | Tesla M60 | Tesla V100 | RTX 4070 |
|---|---|---|---|
| Architecture | Maxwell (2015) | Volta (2017) | Ada Lovelace (2023) |
| CUDA Cores | 4,096 | 5,120 | 5,888 |
| **FP32 Compute** | **~8.1 TFLOPS** | **~15.7 TFLOPS** | **29.15 TFLOPS** |
| **FP16 Compute** | **~8.1 TFLOPS** | **~125 TFLOPS** | **~116 TFLOPS** |
| VRAM | 16GB GDDR5 | 16GB HBM2 | 12GB GDDR6X |
| Memory Bandwidth | ~160 GB/s | **900 GB/s** | 504 GB/s |
| Tensor Cores | None | 640 (1st gen) | 184 (4th gen) |
| TDP | ~300W | ~250W | 200W |

**Key observations:**

- In raw FP32, the V100 (~15.7 TFLOPS) is about **2× faster than the M60** but still only **~54% of the RTX 4070**.
- Where the V100 **truly shines** is FP16 with Tensor Cores — ~125 TFLOPS, which is actually **comparable to the RTX 4070's FP16** and vastly better than the M60.
- The V100's **HBM2 memory bandwidth (900 GB/s)** is the biggest hidden advantage — nearly **2× the RTX 4070** and **5.6× the M60**. This matters enormously for LLM inference, where memory bandwidth is usually the bottleneck, not raw FLOPS.

**Bottom line:** For AI/LLM work, the V100 at 800–1,000 CNY is a much better buy than the M60 at 288 CNY. The bandwidth and Tensor Core advantage make it genuinely faster for inference despite being a similar price tier in the secondhand market.