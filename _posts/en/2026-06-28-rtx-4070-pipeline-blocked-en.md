---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 Pipeline Blocked
translated: false
type: note
---

Here's the honest assessment:

## RTX 4070 (12 GB) — Feasibility Analysis

**Hardware snapshot:**

- VRAM: 12 GB (11.6 GB free right now)
- RAM: 62 GB (55 GB available)
- Disk: 55 GB free out of 916 GB (94% full)

### Verdict: Can't run the full pipeline. Here's why per stage

**1. Data Preparation — BLOCKED (disk)**

- Target cache for Qwen3-4B = ~38 TB. You have 55 GB free. This alone kills it.
- Also needs SGLang serving Qwen3-4B (~8 GB VRAM just for the model), which barely fits.

**2. Training — BLOCKED (VRAM + disk + GPU count)**

- Default config assumes 8 GPUs, `sharding_strategy="no_shard"`, `global_batch_size=512`
- Qwen3-4B in bf16 ≈ 8 GB. Even though the draft model is small (~5 layers), loading the target model to copy embeddings/lm_head requires ~8 GB VRAM temporarily
- The target cache dataset needs to be on disk — 38 TB requirement
- Single GPU with 12 GB can't fit both models + activations + gradients

**3. Evaluation — TIGHT but possible with modifications**

- Needs target model (Qwen3-4B, ~8 GB) + draft model loaded simultaneously
- 12 GB VRAM is borderline — might work with `torch.float16` and careful memory management, but will likely OOM

### What COULD work with aggressive modifications

| Change | Impact |
| -------- | -------- |
| Use a much smaller target model (e.g. Qwen3-0.6B if it exists) | Fits in 12 GB |
| Drastically reduce training data (100 samples instead of 1.3M) | Cache fits in ~few GB |
| Use gradient checkpointing + bf16 + `local_batch_size=1` | Reduces VRAM |
| Skip target cache, run target model on-the-fly during training | Saves disk, but slower and needs VRAM for both models |
| Use Eagle3 (1 layer draft) instead of DSpark (5 layers) | Smaller draft model |

### Better options for you

1. **AMD Dev Cloud (MI300X, 192 GB HBM3)** — can run the full pipeline comfortably. At ~$2/hr, a full training run would be affordable for experimentation.

2. **Your workstation for eval only** — if you download a pre-trained DSpark checkpoint (DeepSeek released them), you could potentially run evaluation with Qwen3-4B in fp16 with `max_new_tokens` capped low.

3. **Rent 8x A100/H100 on cloud** — for the full training pipeline with default settings.

Want me to try setting up a minimal eval-only run on the workstation with a pre-trained checkpoint, or explore the AMD Dev Cloud route?
