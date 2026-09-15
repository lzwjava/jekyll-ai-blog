---
audio: false
generated: true
image: false
lang: en
layout: post
title: Expert Offloading on A16
translated: false
type: note
---

Question: Is the A16 GPU optimization strategy for DeepSeek deployment based on keeping active experts in VRAM and inactive experts in DRAM, transferred via PCIe?

Answer:

Yes, exactly right. This is called **Expert Offloading** — a well-known optimization for running MoE (Mixture of Experts) models like DeepSeek efficiently on memory-constrained hardware.

**How it works:**

```
┌─────────────────────────────────────┐
│           GPU VRAM (48GB A16)       │
│  ┌─────────────────────────────┐    │
│  │  Active Experts (Top-K)     │    │
│  │  Attention layers           │    │
│  │  Shared weights             │    │
│  └─────────────────────────────┘    │
└──────────────────┬──────────────────┘
                   │ PCIe Bus
                   │ (bandwidth bottleneck)
┌──────────────────┴──────────────────┐
│         System DRAM (256GB+)        │
│  ┌─────────────────────────────┐    │
│  │  Inactive Experts (cold)    │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

**Why A16 makes sense here:**

- A16 has **64GB VRAM** (4×16GB), large enough to hold the "hot" expert cache
- Server-grade platform = large DRAM headroom (512GB+ possible)
- PCIe 4.0 x16 gives ~32 GB/s bandwidth — sufficient if expert swap frequency is low

**The key bottleneck:**
DeepSeek-V2/V3 activates only **top-2 out of 256 experts** per token. So cache hit rate on "popular" experts is high, minimizing PCIe transfers. This is what makes the strategy viable for acceptable TPS.

**Tools that implement this:**

- `llama.cpp` with `-ngl` + offload tuning
- `mlx` (Apple) — similar philosophy
- `KTransformers` — specifically designed for this expert-offload pattern on CPU+GPU hybrid

The A16's value proposition is essentially: large VRAM pool at a lower cost-per-GB than A100/H100, perfect for this cache-heavy workload.

References:

- [KTransformers: Expert Offloading for MoE Models](https://github.com/kvcache-ai/ktransformers)
- [DeepSeek-V2 Technical Report (MoE Architecture)](https://arxiv.org/abs/2405.04434)
- [llama.cpp GPU Offloading Docs](https://github.com/ggerganov/llama.cpp)
