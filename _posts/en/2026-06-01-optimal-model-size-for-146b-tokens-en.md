---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimal Model Size for 14.6B Tokens
translated: false
type: note
---

Now let me do the full analysis. Here's what we have and what's optimal:

---

**Machine: MI300X, 192 GB HBM3, single GPU**

**Data: 14.6B tokens (147 shards × 100M uint16, 28 GB on disk)**

**Existing configs:**

| Config | Params | Architecture | Designed for |
|--------|--------|-------------|-------------|
| train_gpt2.py | 124M | 12L/768d/12h | 8×A100, 300B tokens |
| train_gpt2_200m.py | 219M | 18L/896d/16h | RTX 4070 12GB, 4B tokens |
| train_fineweb.py | 124M | 12L/768d/12h | 12GB VRAM |
| train_fineweb_gpt3.py | 124M | 12L/768d/12h | RTX 4070 12GB, 10B tokens |
| train_fineweb1_5b.py | 1.5B | 48L/1600d/25h | H200 143GB, ~7B tokens |

**None of these are designed for 192 GB VRAM + 14.6B tokens.** We need a new config.

**Chinchilla scaling law analysis:**

The Chinchilla paper (Hoffmann et al. 2022) says optimal training tokens ≈ 20× parameters. So:

- 124M → 2.5B tokens (we have 14.6B → massively over-trained)
- 350M → 7B tokens (close but we have more)
- 760M → 15.2B tokens ← **sweet spot for 14.6B tokens**
- 1.5B → 30B tokens (we'd under-train by 2×)
- 3B → 60B tokens (way under-trained)

**But** Chinchilla is a *compute-optimal* law — it minimizes loss per FLOP. If we have spare VRAM and don't mind using more FLOPs, a larger model trained on fewer tokens still gives better *absolute* loss. The LLaMA-1 paper showed 7B trained on 1T tokens beats Chinchilla-optimal at that scale.

**Memory budget (bf16 training, Adam):**

Per parameter: 2 (bf16 params) + 4 (fp32 master) + 4 (m) + 4 (v) + 2 (grad) ≈ 16 bytes

| Model | Params | Train mem | + Activations | Total | Fits 192GB? |
|-------|--------|-----------|---------------|-------|-------------|
| 760M | 760M | 12 GB | ~10 GB | ~22 GB | ✅ easily |
| 1.5B | 1.5B | 24 GB | ~20 GB | ~44 GB | ✅ easily |
| 3B | 3B | 48 GB | ~40 GB | ~88 GB | ✅ yes |
| 7B | 7B | 112 GB | ~60 GB | ~172 GB | ✅ tight |
| 13B | 13B | 208 GB | ~80 GB | ~288 GB | ❌ no |

**Recommendation: 3B model (GPT-2 3B)**

Why 3B over 7B:

- 3B on 14.6B tokens = ~5× over-training. That's fine — LLaMA-1 7B was trained on 1T tokens (143× Chinchilla-optimal). Over-training always helps absolute loss.
- 7B on 14.6B tokens = ~2× under-training. You'd get a model that hasn't converged.
- 3B fits comfortably with large batch sizes → faster training
- 3B at ~5× over-training will beat 7B at ~2× under-training

**Proposed config: GPT-2 3B**

```python
# 3B params: n_layer=48, n_head=32, n_embd=2560
# ~10.2 GB per layer in bf16
# Total train memory: ~48 GB params/opt + ~40 GB activations ≈ 88 GB (well under 192)
# Allows large batch_size for throughput

batch_size = 32              # 32 × 1024 = 32K tokens per micro-step
block_size = 1024
gradient_accumulation_steps = 64  # effective batch = 32 × 1024 × 64 = 2M tokens

n_layer = 48
n_head = 32                  # head_size = 2560/32 = 80
n_embd = 2560
dropout = 0.0
bias = False

learning_rate = 3e-4
min_lr = 3e-5
warmup_iters = 2000
max_iters = 11500            # 11500 × 2M = 23B tokens (passes over data ~1.6×)
lr_decay_iters = 11500
weight_decay = 0.1
beta2 = 0.95
grad_clip = 1.0
compile = True
```

Alternative: if you want to train longer and iterate faster, start with **1.5B** (GPT-2 XL arch) and do multiple passes:

```python
# 1.5B: reuse train_fineweb1_5b.py but with larger batch
n_layer = 48
n_head = 25
n_embd = 1600
batch_size = 64              # fits easily on 192GB
gradient_accumulation_steps = 32  # effective = 64 × 1024 × 32 = 2M tokens
max_iters = 15000            # 15000 × 2M = 30B tokens (2× over data)
```

Which do you want — 3B (better final loss, ~2-3 days) or 1.5B (faster iterations, can experiment more)?
