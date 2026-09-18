---
audio: false
generated: true
image: false
lang: en
layout: post
title: GRPO Fine-Tuning Live Progress
translated: false
type: note
---

Attached non-interactively and read the pane — here's the live state of tmux session **`2`** (window 0, `.venv/bin/python train_grpo.py`).

## What's running
GRPO fine-tuning with TRL: **Qwen/Qwen2.5-1.5B** (4-bit + LoRA r=16, 18.5M trainable / 1.18%) on the synthetic math dataset.

```
run.sh → train_grpo.py --model Qwen/Qwen2.5-1.5B --dataset synthetic \
  --output-dir ./grpo_qwen15b_math --num-epochs 2 --per-device-batch-size 2 \
  --grad-accum 4 --num-generations 4 --max-completion-length 384 \
  --lr 5e-6 --beta 0.02 --temperature 1.0
```

## Progress right now

| | |
|---|---|
| Step | **175 / 760 (23%)** |
| Elapsed / ETA | 29:12 / **~48 min remaining** |
| Speed | ~4.93 s/it |
| Epoch | 0.46 of 2 |
| Inner bar | 18/20 (generation loop) |
| Checkpoints | `checkpoint-125`, `checkpoint-150` (latest written 18:53) |
| GPU | RTX 4070 — 71% util, 6.9 / 12.3 GB, 47 °C |

## Metrics trend (from scrollback)
- **Reward is climbing**: early steps ~0.41–0.44 → recent steps mostly **0.62–1.0**, with several 1.0s. `reward_correctness/mean` now commonly 0.6–0.9.
- **KL is low and flat** (~0.011–0.05) — no drift/divergence from the reference model.
- Entropy 0.50–0.74, `clip_ratio/*_mean` ≈ 0 — policy updates are gentle, clipping never triggers.
- `frac_reward_zero_std` often 0.5 → half the groups have identical rewards within a group, so those contribute no gradient signal. Normal for easy synthetic math, but it means effective learning signal per step is lower than it looks.

## Health
No errors, no NaN in loss or grad_norm, process alive (CPU 83%, 37:44 total uptime incl. model download/load). Only benign warnings in the log:
- `warmup_ratio is deprecated` (transformers 5.x)
- `urllib3/charset_normalizer doesn't match a supported version`
- tokenizer PAD/BOS/EOS alignment notice

To attach yourself: `tmux a -t 2` (then detach with `Ctrl-b d`). Note there's also a `0:mihomo` session running separately.

Rough finish: ~48 min out, so ~19:41 wall clock if throughput holds.