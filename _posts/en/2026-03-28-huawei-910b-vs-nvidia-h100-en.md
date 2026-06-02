---
audio: false
generated: true
image: false
lang: en
layout: post
title: Comparing Huawei 910B and NVIDIA H100
translated: false
type: note
---

Question: How does the Huawei Ascend 910B compare to the NVIDIA H100 (one at ~320 TFLOPS vs the other at ~989 TFLOPS)? And how many RTX 4070s would it take to equal one H100?

Answer:

## Huawei Ascend 910B vs NVIDIA H100

First, let's clarify the numbers you mentioned:

| Chip | FP16 TFLOPS | Notes |
|---|---|---|
| **Huawei Ascend 910B** | ~320–600 TFLOPS | Huawei doesn't publish official specs; estimates vary widely |
| **NVIDIA H100** | ~989 TFLOPS (SXM5) | Official NVIDIA spec |
| **RTX 4070** | ~58.2 TFLOPS | Your server's GPU |

> **Why the 910B range is fuzzy:** Huawei's Ascend 910B boasts computing capabilities of up to 320 TFLOPS in FP16 while consuming 310W of power. However, Huawei does not publish detailed specifications for the Ascend 910B — some sources estimate ~600 TFLOPS FP16, which is a widely cited figure in technical analyses. The 320 TFLOPS figure may refer to a specific configuration or per-die spec.

---

## Head-to-Head: 910B vs H100

The 910B has roughly 60% of the H100's compute, 36% of its memory bandwidth, and a software ecosystem that is years behind CUDA.

The 910B is roughly comparable to the A100 — Nvidia's top chip from 2020. One Huawei official even claimed the 910B outperformed the A100 by around 20% in some training tasks in 2024. But the chip still relies on older HBM2E memory and holds about a third less data in memory than H100, and transfers data between chips about 40% more slowly.

In plain terms:

- **Raw TFLOPS gap:** H100 is roughly **1.6x–3x faster** than 910B depending on whether you use the 320 or 600 TFLOPS estimate
- **Real-world training gap:** For compute-bound training on large batch sizes, the gap is closer to 2.5–3x because the H100's higher compute and memory bandwidth compound. For smaller models and memory-capacity-bound inference, the gap narrows to 1.5–2x.
- **Process node gap:** The Ascend 910B relies on 7nm fab technology, while Nvidia's H100 is produced with 4nm tech — generations ahead.

---

## How Many RTX 4070s to Equal One H100?

Using **raw FP16 TFLOPS** (theoretical peak):

| Target | TFLOPS needed | RTX 4070 FP16 | Cards needed |
|---|---|---|---|
| Match H100 (~989 TFLOPS FP16) | 989 | 58.2 | **~17 cards** |
| Match 910B (~320 TFLOPS) | 320 | 58.2 | **~6 cards** |
| Match 910B (~600 TFLOPS) | 600 | 58.2 | **~11 cards** |

So: **≈17 RTX 4070s ≈ 1 H100** on pure TFLOPS paper math.

> ⚠️ **But this is misleading in practice.** Raw TFLOPS doesn't equal real training performance. The H100 has:
>
> - **HBM3 memory** with 3.35 TB/s bandwidth (vs 4070's GDDR6X at ~504 GB/s)
> - **NVLink** for multi-GPU scaling
> - **Tensor Core efficiency** at massive batch sizes
> - **80GB VRAM** (vs 12GB on 4070)
>
> You can't simply chain 17 consumer GPUs together and match an H100. VRAM size, memory bandwidth, and interconnect are the actual bottlenecks for LLM work. Your single 4070 with 12GB VRAM can't even hold a 30B parameter model in FP16 — an H100 can run 70B+ models in a single card.

---

## Summary

| Metric | 910B vs H100 | 4070 vs H100 |
|---|---|---|
| Raw FP16 | ~33–60% of H100 | ~6% of H100 |
| Real-world LLM training | ~33–66% of H100 | Not comparable (VRAM limited) |
| Cards to match H100 (paper) | ~2–3x 910Bs | ~17 RTX 4070s |
| Practical scalability | Yes (data center) | No (consumer GPU) |

Your `lzw-server`'s RTX 4070 is a great GPU for local inference on small models (7B–13B quantized), but for H100-class work, you're looking at a fundamentally different class of hardware.

References:

- [Huawei Ascend 910B specs and analysis](https://awesomeagents.ai/hardware/huawei-ascend-910b/)
- [Huawei Ascend 910C vs NVIDIA H100 comparison](https://www.nexgen-compute.com/blog/huawei-ascend-910c-vs-nvidia-h100-ai-chip-comparison)
- [China's AI Chip Race — IEEE Spectrum](https://spectrum.ieee.org/china-ai-chip)
- [Huawei 910B challenges NVIDIA — TrendForce](https://www.trendforce.com/news/2024/06/11/news-huaweis-self-developed-ai-chip-challenges-nvidia-boasting-its-ascend-910b-to-be-equal-in-match-with-a100/)
