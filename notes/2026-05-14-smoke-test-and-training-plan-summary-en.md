---
audio: false
generated: true
image: false
lang: en
layout: post
title: Smoke Test and Training Plan Summary
translated: false
type: note
---

Here's the result.

## Smoke test results — `/mnt/data/nanoGPT/out-gpt2-200m-smoke/smoke.log`

| Metric                              | Value                                     |
| ----------------------------------- | ----------------------------------------- |
| Param count (printed by train.py)   | **218.51M**                               |
| Loss trajectory (25 iters)          | 10.985 → 7.66 (normal cold-start descent) |
| Per-iter time at bs=2, grad_accum=4 | ~330 ms                                   |
| Crashes / NaN / OOM                 | none                                      |

## VRAM probe (bf16, no compile)

| micro-batch    | peak VRAM   | ms / micro-step | ms / token |
| -------------- | ----------- | --------------- | ---------- |
| 2              | 5.55 GB     | 117             | 0.0571     |
| **4 (chosen)** | **8.01 GB** | **167**         | **0.0408** |
| 6              | 10.44 GB    | 231             | 0.0376     |
| 8              | OOM         | —               | —          |

`bs=4` is the clear winner: 28% faster per token than bs=2, with ~4 GB headroom for `torch.compile` and eval. I updated `config/train_gpt2_200m.py` to use `batch_size=4`, `gradient_accumulation_steps=128` (still 524,288 tokens/step).

## The plan

**Architecture (custom, between GPT-2 small and medium):**
```
n_layer = 18,  n_head = 16,  n_embd = 896     → 218.5M non-embedding params
```

**Why 4B tokens:** Chinchilla-optimal ≈ 20 × params → 20 × 219M ≈ 4.4B. Your 4B target is right on the line.

**Token budget:** 524,288 tokens/step × 8,000 steps = **4.19B tokens**.

**Data:** 1,408 FineWeb-Edu shards (~140B tokens) already at `data/fineweb/edu_fineweb100B/` — far more than we need, so no re-tokenization.

**Time estimate on the RTX 4070:**

| Setting                                                 | Time / iter | Wall-clock for 8,000 iters |
| ------------------------------------------------------- | ----------- | -------------------------- |
| bs=4, no compile                                        | ~21.4 s     | **~48 hours (~2 days)**    |
| bs=4, with `compile=True` (≈25% speedup typical on Ada) | ~16 s       | **~36 hours (~1.5 days)**  |

So budget roughly **~1.5–2 days of uninterrupted GPU time**. Add ~30 min for `torch.compile` warmup on first iter and ~30 min total for 32 eval passes (every 250 iters × ~3 s/eval).

**Expected final val loss:** ~2.92–3.00 (better than 124M's ~3.0–3.1, just shy of 350M's ~2.85–2.95).

## To kick off the real run

```bash
python3 train.py config/train_gpt2_200m.py
```

If you want, I can also: (a) tee output to a log file, (b) wire up wandb, or (c) start it now in the background so you can monitor it.