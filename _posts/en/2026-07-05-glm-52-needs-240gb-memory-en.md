---
audio: false
generated: true
image: false
lang: en
layout: post
title: GLM-5.2 Needs 240GB Memory
translated: false
type: note
---

**Question:** Confirm: GLM-5.2 (743B MoE) is not runnable on an RTX 4070 12 GB at any quantization — it needs datacenter-class hardware even at 1–2 bits, right?

**Answer:**

Right, with one small correction to the framing: it's not strictly "datacenter GPU or nothing" — it's "~240 GB of unified memory or nothing," and your 4070 box has ~74 GB total. Same conclusion for you, but the boundary is worth knowing precisely.

The real numbers:

- GLM-5.2 is a ~743B-parameter MoE with 39B active, shipping as BF16 and native-FP8 checkpoints; the FP8 production path targets a single 8×H200 / 8×H20 node.
- The 2-bit dynamic GGUF (UD-IQ2_M) is ~239 GB and needs that much memory at runtime — practical only on a 256GB-class Mac Studio, a 4×RTX 3090 rig with 192 GB of system RAM, or a datacenter node. The key constraint: even though only ~39B parameters are active per token, all 743B MoE weights must be held in memory at once.
- Even then, expect roughly 3–9 tok/s on the consumer/prosumer path. That's not a coding-agent-viable speed.

So the "consumer hardware" success stories you'll see (like the 4×RTX 3090 + Ubuntu + Unsloth 2-bit GGUF walkthrough) are ~$4–6K rigs with 96 GB VRAM + 192 GB RAM. Your workstation (12 GB VRAM + 62 GB RAM) is ~3× short even for the most aggressive quant. Interestingly, the quality story at low bits is better than intuition suggests — Unsloth's KLD benchmarks show dynamic 2-bit retains ~82% top-1 accuracy while being 84% smaller, because important layers stay in higher precision — but that doesn't help if the weights don't fit.

One angle specific to *your* hardware: your AMD Dev Cloud MI300X droplet is the closest thing you have. A single MI300X has 192 GB HBM3, which is still short of the ~239 GB for UD-IQ2_M fully on-GPU, but with llama.cpp ROCm + `--n-cpu-moe` offloading routed experts to the droplet's system RAM, it's borderline runnable as a $2/hr experiment. Worth an hour of droplet time if you're curious; not worth it as a daily driver — at those speeds and prices, the Z.ai API beats self-hosting on every axis except learning value.

For the 4070 box, the previous recommendation stands: GLM-4.5-Air (106B/12B active) with MoE offload, or Qwen3-30B-A3B if you want speed over capability. Skip the GLM-5.2 download.

**References:**

- [Unsloth: GLM-5.2 — How to Run Locally](https://unsloth.ai/docs/models/glm-5.2)
- [GLM-5.2 Hardware Requirements (Compute Market)](https://www.compute-market.com/blog/glm-5-2-local-hardware-guide-2026)
- [vLLM recipe: zai-org/GLM-5.2](https://recipes.vllm.ai/zai-org/GLM-5.2)
- [Running GLM-5.2 Locally on 4×3090 (Medium)](https://medium.com/@ttio2tech_28094/running-glm-5-2-locally-a-744-billion-parameter-model-on-consumer-hardware-1bd58831a5b2)