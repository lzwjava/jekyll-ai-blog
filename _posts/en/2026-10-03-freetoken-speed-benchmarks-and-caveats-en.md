---
audio: false
generated: true
image: false
lang: en
layout: post
title: FreeToken Speed Benchmarks and Caveats
translated: false
type: note
---

Question: How fast is FreeToken (FlashML-org/FreeToken), and what is its serving speed?

Answer:

The repo README states no speed numbers; it only says FreeToken runs 290B+ MoE models on a gaming PC "at blistering interactive speeds." The numbers come from the project's paper (UC Berkeley / UT Austin authors) and third-party write-ups. They are the authors' own results, not independent benchmarks.

**Decode speed (tokens/s)**

| Hardware | Model | Speed |
| --- | --- | --- |
| RTX 4060 Laptop (8 GB VRAM, 32 GiB RAM) | Qwen3.6-35B-A3B (NVFP4) | 39.3 tokens per second |
| RTX 5090 (32 GB) | Qwen3.6-35B-A3B | 77–83 tok/s |
| RTX 5090 (32 GB) | DeepSeek-V4-Flash (284B total) | 22–25 tok/s |
| RTX PRO 6000 (96 GB) | GLM-5.2 (753B total, 40B active) | 14.9 tokens/s, compared with 7.3 tokens/s for llama.cpp |

**Comparison with other engines**

- The paper reports 1.5–2.3x higher decode throughput than state-of-the-art edge serving across all workloads. The baselines include llama.cpp, Ollama, KTransformers and MoE-Infinity.
- Prefill reaches 6.7k tokens/s at 16,000 tokens.
- Time-to-first-token is under 44 seconds in the worst case across the evaluated workloads. For comparison, other systems might time out on the most demanding ones.
- One third-party test against Ollama, with a model larger than VRAM, found 132.5 tokens/second median versus 58.8, about a 2.25x speedup.
- When the model fits entirely in VRAM, there is no gain. In the same test Ollama reached 239.6 tokens/second and FreeToken 225.3.

**Caveats**

- The speed advantage applies mainly when the model is larger than your VRAM.
- It currently targets NVIDIA RTX 30/40/50 GPUs. A community AMD port got only about 9 tok/s on an 8 GB card, though its author attributes the gap to hardware rather than method.
- Real speed depends on your RAM and PCIe bandwidth, the quantization format, and the workload. Run `ft serve` on your own machine to confirm.

References:

- [FreeToken GitHub repository](https://github.com/FlashML-org/FreeToken)
- [FreeToken paper (HTML version)](https://arxiv.org/html/2608.16157v1)
- [FreeToken AI Review: Hardware, Benchmarks & Setup (Wavect)](https://wavect.io/blog/freetoken-ai-inference-engine-review/)
- [FreeToken: Running Massive MoE Models Locally at 2-4x Ollama's Speed (Better Stack)](https://betterstack.com/community/guides/ai/freetoken-moe-inference/)
- [Emergent Mind paper summary](https://www.emergentmind.com/papers/2608.16157)
- [FreeToken_AMD community port](https://github.com/alpaslan-exe/FreeToken_AMD)
