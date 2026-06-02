---
audio: false
generated: true
image: false
lang: en
layout: post
title: Healthy Training Run in Progress
translated: false
type: note
---

Training is healthy and running. Here's the status:

**Process**: `train.py config/train_gpt2_200m.py --compile=False` (PID 1681991), GPU at 100%, 211W.

**Progress**: iter **1840 / 8000** (23%), last val loss **3.6331** at step 1750 (down from 10.99 at start).

**Speed**: ~18.53s/iter (one 4070, no compile, batch_size=4, grad_accum=128 → 524K tokens/step). Eval+checkpoint every 250 iters costs ~28s extra.

**Time remaining**: 6160 iters × 18.53s + ~25 checkpoint stalls ≈ **31–32 hours from now**, ETA roughly **Saturday 2026-05-16, ~05:30 local**.

**Elapsed so far**: 9h 34m.

Suggestions if you want it faster:

- Enable `--compile=True` next run — typically 1.3–1.8× speedup on a 4070, would shave ~10 hours.
- Or cut `max_iters` if val loss plateaus; current val curve (6.21 → 5.36 → 4.56 → 4.08 → 3.87 → 3.69 → 3.63) is still descending healthily, no plateau yet.
