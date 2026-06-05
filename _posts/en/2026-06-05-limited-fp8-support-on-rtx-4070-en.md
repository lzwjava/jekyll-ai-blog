---
audio: false
generated: true
image: false
lang: en
layout: post
title: Limited FP8 Support on RTX 4070
translated: false
type: note
---

Question: Why doesn't the RTX 4070 support FP8 well?

Answer:

Actually, the RTX 4070's Tensor cores do support FP8 with sparsity — Ada does have 4th gen Tensor Cores with FP8 capability. But the "well" part is the catch. Here's why it's limited in practice:

**Hardware vs. Software Gap**

While the hardware supports FP8, it's "not clear how useful that is in all workloads, and figuring out just what uses FP8 versus FP16, plus sparsity, can be tricky". Most frameworks (PyTorch, TensorFlow) don't automatically leverage FP8 — you need explicit quantization tooling and framework support.

**Chip-Level Limitations**

The RTX 4070 uses the AD104 die, which is the lower-end Ada variant. FP8 is "a forward-looking capability aimed at improving efficiency in AI service deployment", but mature FP8 implementations are concentrated on Hopper (H100/H200) and higher-tier Ada chips (RTX 4090, RTX 6000 Ada). The ecosystem prioritizes data center hardware.

**Memory Bandwidth Bottleneck**

While FP8 can "halve storage and memory bandwidth requirements compared to FP16", the RTX 4070 uses a narrower 192-bit memory interface, resulting in lower peak bandwidth. The gains from FP8 compute get throttled by the memory wall.

**Practical Consequence**

For your workload (nanoGPT-scale training, LoRA fine-tuning), the speedup from FP8 on RTX 4070 is negligible because:

1. Framework support is still immature
2. Memory bandwidth is the bottleneck, not compute
3. Most quantization in practice uses INT8 or FP16 with better tooling

**Better approach:** Use BF16 or mixed FP16/FP32 — well-supported, proven, and gets you 80%+ of the theoretical wins with zero friction.

References:

- [Tom's Hardware - RTX 40-series tensor cores and FP8 support](https://www.tomshardware.com/reviews/nvidia-geforce-rtx-4070-review)
- [BestGPUsForAI - RTX 4070 vs 3080 tensor architecture](https://www.bestgpusforai.com/gpu-comparison/4070-vs-3080)
