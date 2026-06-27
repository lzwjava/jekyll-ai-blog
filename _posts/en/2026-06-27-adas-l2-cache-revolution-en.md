---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ada's L2 Cache Revolution
translated: false
type: note
---

Question: What's an unpopular/lesser-known fact about NVIDIA's Ada Lovelace GPU architecture?

Answer:

The most underrated fact: **Ada Lovelace (AD10x) has dramatically more L2 cache than Ampere, and this — not raw compute — is the real architectural story.**

The AD102 die jumped from 6 MB L2 (GA102) to **98 MB L2** — a ~16x increase. This was a direct copy of AMD's "Infinity Cache" strategy and a quiet admission that GDDR6X bandwidth wasn't scaling fast enough. The 4090 actually has a *narrower* memory bus (384-bit) than you'd expect for its tier, and the giant cache hides that. For your inference work, this matters: Ada's effective bandwidth for cache-resident working sets is far better than the spec-sheet 1 TB/s suggests, but it falls off a cliff once your KV cache + weights exceed L2.

Other genuinely unpopular facts:

1. **FP8 (E4M3/E5M2) tensor cores exist on Ada but are software-crippled vs Hopper.** Ada's 4th-gen tensor cores do FP8, but NVIDIA reserved the FP8 *with FP32 accumulate at full rate* and the Transformer Engine's full feature set for Hopper. On consumer Ada you get FP8 matmul but the Transformer Engine path is neutered — relevant if you're benchmarking 4090 vs H100 for training.

2. **Ada has no NVLink.** Even the 4090 dropped the NVLink connector that the 3090 had. This was deliberate market segmentation to push multi-GPU training buyers toward H100/datacenter SKUs. For your dual-GPU experiments, 4090s are stuck on PCIe peer-to-peer.

3. **The "AD102 is barely used" fact.** The 4090 ships with AD102 *heavily cut down* — 128 of 144 SMs enabled. The full die never appeared in a consumer card; it was saved for the RTX 6000 Ada / L40. So the most powerful gaming GPU of its generation was a salvage bin part.

4. **SER (Shader Execution Reordering)** was marketed for ray tracing but is a general latency-hiding mechanism for divergent workloads — barely discussed outside graphics.

5. **Ada's tensor cores added FP8 but *removed* nothing — yet sparsity (2:4 structured) is still mostly unused** because no mainstream training framework reliably exploits it, making half the "sparse TFLOPS" marketing numbers irrelevant in practice.

For your 4070 (AD104, 36 MB L2, 12 GB): the cache story is why it punches above its bandwidth class on small models but chokes the moment a model spills past ~10 GB.

References:

- [NVIDIA Ada GPU Architecture Whitepaper](https://images.nvidia.com/aem-dam/Solutions/Data-Center/l4/nvidia-ada-gpu-architecture-whitepaper-v2.1.pdf)
- [Chips and Cheese — Ada's L2 cache analysis](https://chipsandcheese.com/)

(Note: I didn't run a live search here — these are from the published whitepaper and architecture coverage. If you want me to verify the exact SM/cache counts per die with sources, I can search.)
