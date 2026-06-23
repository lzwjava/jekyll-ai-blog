---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 Training Loss Spike
translated: false
type: note
---

================================================================
  GPT-2 124M TRAINING — github-code dataset
================================================================

CURRENT PROGRESS
  Iteration:      257,240 / 427,000 = 60.2%
  Tokens seen:    ~8.43B / 14B
  Latest ckpt:    step 257,000 (ckpt.pt, 1.4GB)

LOSS TRAJECTORY
  Step 187,000:   train 3.1404, val 3.1927
  Step 234,000:   train 2.6758, val 2.6576
  Step 257,000:   train 3.0636, val 2.9376

⚠ NOTE: Loss increased from 234k → 257k
  Train: 2.6758 → 3.0636 (+0.39)
  Val:   2.6576 → 2.9376 (+0.28)

  This could indicate:
  - Learning rate still too high (currently decaying from 6e-4)
  - Data ordering causing variance (normal in long runs)
  - Model hitting a plateau and bouncing

HARDWARE (RTX 4070)
  GPU: 100% util, 66°C, 208W
  VRAM: 5.3 / 12.3 GB
  MFU: 14.43%, 622ms/step

ESTIMATED TIME REMAINING
  ~170k steps left × 622ms = ~29.5 hours (~1.2 days)

HEALTH CHECK
  ⚠ Loss regression from best checkpoint at 234k
  You may want to monitor the next few eval intervals to see
  if it recovers. If not, consider:
  - Rolling back to the 234k checkpoint
  - Reducing learning rate further
================================================================

Want me to keep monitoring, or check if the loss trend is stabilizing?
