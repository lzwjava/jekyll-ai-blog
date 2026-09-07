---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 Cannot Run GLM-5.3
translated: false
type: note
---

Short answer: **no, not realistically.** The target model (GLM-5.3-Flash-NVFP4) has hard requirements that an RTX 4070 can't meet:

**1. Not enough VRAM (12 GB vs ~17+ GB minimum)**
Even the most memory-lean config in `examples/serve_full.sh` needs roughly:

- ~17 GB for the dense (non-expert) weights alone
- +31 GB resident expert layers, KV pool, CUDA overhead on top

The dense portion alone already exceeds the 4070's 12 GB. There's no config in this repo that fits.

**2. NVFP4 needs Blackwell (sm_100+)**
The checkpoint is NVFP4-quantized. FP4 tensor-core acceleration only exists on Blackwell; the RTX 4070 is Ada (sm_89). The `--nvfp4-backend auto` and the Triton kernels here are tuned for Blackwell shapes/bandwidth. Even if you could dequantize to FP8/BF16 on the fly, you'd blow past the VRAM budget.

**3. Not enough system RAM**
The script preflights for **≥138 GB MemAvailable** (129 GB pinned host bank for offloaded experts + engine overhead). A typical 4070 machine has 32–64 GB RAM. The full expert set is 181 GB — it has to live somewhere.

**4. PCIe bandwidth would halve speed anyway**
The whole design is PCIe-bound: the reference box uses Gen5 x16 (~64 GB/s). The 4070 is Gen4 x16 (~32 GB/s), so even if everything else worked, decode would land at roughly half the measured numbers.

**What the 4070 *could* do:**

- Run much smaller models (the upstream FreeToken server itself is model-agnostic)
- Potentially serve a small dense model fully in VRAM, or a small MoE with light offload — but that's upstream FreeToken territory, not what this patch set optimizes for

If you're stuck with 12 GB VRAM + typical RAM, a better fit would be running a ~7–14B dense model directly (vLLM/llama.cpp), or a small MoE like Qwen3-30B-A3B with CPU offload.
