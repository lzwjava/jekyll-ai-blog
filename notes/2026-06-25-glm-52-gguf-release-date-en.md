---
audio: false
generated: true
image: false
lang: en
layout: post
title: GLM-5.2 GGUF Release Date
translated: false
type: note
---

**Question:** When was `unsloth/GLM-5.2-GGUF` released?

**Answer:**

GLM-5.2 was announced by Z.ai on **June 13, 2026**, with the MIT-licensed open weights and metered API rolling out across the following week. The Unsloth GGUF quantization repo would have followed shortly after the base weights dropped.

Key facts on the model itself:

- 744B params (~40B active per token), MoE architecture, 1M-token context window, MIT license.
- Introduces IndexShare — reuses the same indexer across every four sparse attention layers, cutting per-token FLOPs by 2.9× at 1M context. MTP layer improvements increase speculative decoding acceptance length by up to 20%.
- Benchmarks: 81.0 on Terminal-Bench 2.1 and 62.1 on SWE-bench Pro, making it the highest-ranked open-source model across long-horizon coding benchmarks (FrontierSWE, PostTrainBench, SWE-Marathon).

Given you're already on deepseek-v4-pro/flash heavily — GLM-5.2 at MIT + 1M context is worth spinning up via the Unsloth GGUF on your AMD MI300X (192GB HBM3 can comfortably handle the quantized version).
