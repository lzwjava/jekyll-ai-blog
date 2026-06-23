---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 124M Training Summary
translated: false
type: note
---

Here's the comprehensive summary:

================================================================
  GPT-2 124M TRAINING — github-code dataset
================================================================

MODEL
  Architecture:   GPT-2 124M (12 layers, 12 heads, 768 embd)
  Parameters:     ~124M
  Dropout:        0.0
  Bias:           False

DATASET
  Name:           github-code
  Location:       /mnt/data/zz/datasets/github-code-tok
  Total tokens:   ~14B

TRAINING CONFIG
  Batch size:     4 × 1024 tokens × 8 grad accum = 32,768 tokens/step
  Total steps:    427,000
  Learning rate:  6e-4 → 6e-5 (cosine decay, 2000 warmup)
  Optimizer:      AdamW (β1=0.9, β2=0.95, wd=0.1)
  Grad clip:      1.0
  Compiled:       Yes

CURRENT PROGRESS
  Iteration:      234,000 / 427,000 = 54.8%
  Tokens seen:    ~7.67B / 14B
  Latest ckpt:    step 234,000 (saved to out-github-code-124m/ckpt.pt, 1.4GB)

LOSS TRAJECTORY
  Step 187,000:   train 3.1404, val 3.1927
  Step 234,000:   train 2.6758, val 2.6576
  Trend:          ↓ steadily improving, ~0.46 drop over 47k steps

HARDWARE STATUS (RTX 4070)
  GPU util:       100%
  Mem util:       51%
  VRAM:           5,283 / 12,282 MiB (43%)
  Temp:           66°C
  Power:          207.5W
  MFU:            14.43%
  Step time:      622ms

ESTIMATED TIME REMAINING
  ~193,000 steps left × 622ms = ~33.5 hours (~1.4 days)
  Completion:     roughly June 25 evening

HEALTH
  Training is healthy. Loss is decreasing smoothly, val loss
  tracks train loss closely (no overfitting). GPU is fully
  utilized at reasonable temps. Checkpoints saving normally.
================================================================
