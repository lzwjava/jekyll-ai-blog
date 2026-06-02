---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress and Estimated Completion
translated: false
type: note
---

Training is healthy and progressing.

**Current status (session 7):**

- Iter ~12,120 / 19,073 (≈64% done)
- Latest checkpoint step 12000: train loss 3.1166, val loss 3.0866
- Step time: ~11.11s/iter, MFU ~12.85%

**Loss trajectory (val loss at checkpoints):**

- 10000 → 3.1121
- 10500 → 3.1356
- 11000 → 3.1043
- 11500 → 3.0830
- 12000 → 3.0866

Val loss is slowly descending (~3.08–3.14 range), training is stable.

**Remaining time estimate:**

- ~6,953 iters left × 11.11s = ~77,300s ≈ **21.5 hours**
- Plus ~14 more eval/checkpoint pauses (~18s extra each) → add ~4 min
- ETA: roughly **21–22 hours** from now
