---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mixed GPU Strategy for RL Pipeline
translated: false
type: note
---

Question: With an RTX 4070 (12GB) at home and 1-2 secondhand MI50s (being tested at a repair shop, ROCm status TBD), plus occasional RunPod H200 bursts (10hr sessions, not enough for real research) — what should I actually build with this specific hardware mix, and what research fits it?

Answer:

Don't think "which GPU is better," think "which GPU does which *job* in the RL pipeline." Your GRPO/agentic-RL plan from before has two very different compute profiles, and your hardware maps onto them almost perfectly by accident:

**Job A — rollout generation (inference, embarrassingly parallel, VRAM/bandwidth-bound, no backward pass).** This is 80%+ of wall-clock time in any RL post-training loop — sampling completions from the policy, scoring them, computing reference log-probs for KL. It doesn't need tensor cores or FlashAttention-grade flops, it needs cheap VRAM sitting there 24/7.

**Job B — the actual optimizer step (backward pass, needs real BF16/FP16 flops, FlashAttention, modern kernels).** This is the 10-30 min GRPO update after each rollout batch. This is what actually benefits from H200.

Your MI50 is a good match for Job A and a bad match for Job B. Here's the honest state of MI50 in 2026: it's officially deprecated in ROCm, AMD stopped building it, and it's weak on compute — 27 FP16 TFLOPS with no matmul-acceleration hardware, so real gradient training on it is painful and unreliable. But it has 16GB (32GB on the MI50 32GB SKU) of HBM2 at ~1TB/s bandwidth, and the community has kept inference alive for it specifically: the nlzy/vllm-gfx906 fork runs vLLM on gfx906 (Radeon VII/MI50/MI60), supports GPTQ/AWQ quantization plus quantized MoE models, on ROCm 6.3+. That fork exists precisely because people use MI50s as cheap always-on inference boxes, not training boxes.

So the build:

```
┌─────────────────────────────────────────────┐
│  MI50 x2-3 (always-on, home)                 │
│  → vllm-gfx906, GPTQ/AWQ quantized weights   │
│  → serves: frozen reference policy (KL calc) │
│  → serves: rollout generation (policy π_old) │
│  → serves: reward/verifier model             │
└───────────────────┬───────────────────────────┘
                     │ rollouts + rewards written to disk/queue
                     ▼
┌─────────────────────────────────────────────┐
│  RTX 4070 (dev loop, always-on)              │
│  → debug GRPO loss, small-scale sanity runs  │
│  → 124M model, fast iterate on reward hacking│
└───────────────────┬───────────────────────────┘
                     │ once stable, burst
                     ▼
┌─────────────────────────────────────────────┐
│  RunPod H200 (burst, 10hr sessions)          │
│  → real GRPO backward pass on 760M           │
│  → sync updated weights back to MI50 servers │
└─────────────────────────────────────────────┘
```

This is why your "10 hours isn't enough" feeling is correct but you were solving the wrong problem — you don't need H200 to be always-on, you need the *rollout generation* to be always-on (that's the part that benefits from 24/7 availability, since RL needs a constant stream of fresh samples), and only rent H200 for the short, spiky optimizer-step compute. That's a much cheaper shape: MI50s running continuously at near-zero marginal cost, H200 rented in short bursts synced against a checkpoint.

Practical setup notes for the MI50s specifically:
- Ubuntu 24.04 + ROCm 6.4.3 (community reports this as the stable combo for gfx906; AMD's official installer no longer targets it, so expect to add repos manually).
- Use `nlzy/vllm-gfx906` (or the maintained `mixa3607/ML-gfx906` docker builds) rather than upstream vLLM — upstream doesn't target gfx906 anymore.
- Quantize everything you serve on the MI50s (GPTQ/AWQ) — unquantized models run "slightly slow," quantized MoE models specifically are reported as "significantly slow" on this fork, so if your reference/reward model is MoE (e.g. DeepSeek-V2-Lite), budget extra latency or keep the MoE model as the thing you train on H200/4070 instead of serving from MI50.
- Don't attempt full training runs on MI50 — treat it as strictly inference infrastructure. If the repair shop confirms the cards are healthy, buy 2 not 1: one for reference-policy serving, one for rollout serving, so KL computation and sampling don't contend for the same GPU.

What research this hardware profile is actually *for*: not "train a bigger model" — you can't, VRAM and flops cap you around 760M-1B realistically. It's for **iterating fast on the RL loop itself** (reward design, KL/entropy ablations, environment/tool-use tasks, distillation pipeline) cheaply and continuously, then using rented H200 hours surgically for the few actual training runs that need real throughput. That's a more defensible research niche than "I trained a bigger model" anyway — cheap-hardware RL-loop engineering is exactly the skill gap most well-funded labs don't have because they never had to solve it.

References:
- [vllm-gfx906 — vLLM fork for MI50/MI60/Radeon VII](https://github.com/nlzy/vllm-gfx906)
- [ROCm Device Support Wishlist — MI50 status, ROCm 6.4.3 setup](https://github.com/ROCm/ROCm/discussions/4276)
- [AMD GPUs for LLM inference — MI50 specs, deprecation status](https://llm-tracker.info/howto/AMD-GPUs)
- [ML-gfx906 — maintained Docker builds for gfx906](https://github.com/mixa3607/ML-gfx906)
