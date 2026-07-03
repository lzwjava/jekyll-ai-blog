---
audio: false
generated: true
image: false
lang: en
layout: post
title: GLM-5.2 Too Large for 4070
translated: false
type: note
---

**Question:** I have an RTX 4070 (12 GB). Which quant should I download from `unsloth/GLM-5.2-GGUF`?

**Answer:**

Honest answer: **none of them**. GLM-5.2 is out of reach for your 4070 box — and probably worth knowing before you burn 200+ GB of bandwidth.

**The math (first principles):**

GLM-5.2 is a ~743B total / 39B active MoE. GGUF memory ≈ `total_params × bits / 8` — MoE routing doesn't save you disk or RAM, only FLOPs, because *all* experts must be resident (any token can route to any expert).

```
Q4_K_M:  743B × 4.5 / 8 ≈ 418 GB
Q2_K:    743B × 2.6 / 8 ≈ 240 GB   ← matches reported numbers
TQ1_0:   743B × 1.7 / 8 ≈ 158 GB   (1-bit dynamic, if unsloth ships it)
```

Even the aggressively-quantized 2-bit GGUF is about 239 GB on disk and needs that much memory at runtime. Your best machine (`192.168.1.36`: 62 GB RAM + 12 GB VRAM = 74 GB total) is ~3x short of even Q2. Also note: as of right now the repo tree only contains `README.md` — the quant shards haven't finished uploading yet anyway.

**What actually works on your hardware:**

The MoE offload trick in llama.cpp (`--n-cpu-moe`: attention + shared expert on GPU, routed experts in RAM) makes ~100B-class MoE models the sweet spot for your workstation:

```bash
# GLM-4.5-Air: 106B total / 12B active — the largest GLM that fits your box
huggingface-cli download unsloth/GLM-4.5-Air-GGUF \
  --include "*UD-Q3_K_XL*" --local-dir ~/models   # ~50 GB

./llama-server -m ~/models/GLM-4.5-Air-UD-Q3_K_XL.gguf \
  --n-gpu-layers 999 --n-cpu-moe 40 -c 32768 -fa
```

With 12B active params, expect ~8–15 tok/s on DDR-bound decode — usable for interactive coding. Check newer Air-class releases too (GLM-4.6/4.7-Air-tier, Qwen3-30B-A3B-class) — anything ≤110B total / ≤13B active is your ceiling at Q3–Q4.

**If you really want GLM-5.2 weights under your fingers:**

Your MI300X droplet (192 GB HBM3) is the only machine you have that's even close — a 1-bit dynamic quant (~158 GB) would fit on a single MI300X with room for KV cache, and llama.cpp has ROCm support. That's a legitimately interesting experiment: frontier 743B MoE on one GPU at $2/hr. But wait for unsloth to actually upload the shards, and check the `UD-TQ1_0` folder size before committing. For daily GLM-5.2 usage, the Z.ai API is the rational path — it's MIT-licensed with metered API access, and running it yourself below ~4 bits costs you meaningful quality on exactly the agentic-coding tasks it's good at.

**References:**

- [unsloth/GLM-5.2-GGUF](https://huggingface.co/unsloth/GLM-5.2-GGUF)
- [vLLM recipe: zai-org/GLM-5.2](https://recipes.vllm.ai/zai-org/GLM-5.2)
- [GLM-5.2 local hardware guide](https://www.compute-market.com/blog/glm-5-2-local-hardware-guide-2026)
