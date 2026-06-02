---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Completed with Best Checkpoint
translated: false
type: note
---

Training finished cleanly at iter 12000. Summary:

**Final losses**
- Train: 3.3565 / Val: 3.3308
- Best val: **3.2929 at iter 11500** (val ticked up slightly to 3.3308 at the final 12000 step — could be noise or the very start of overfitting; either way, the 11500 checkpoint is your best)

**Curve**
- Started 10.99 (random init, ~ln(50304))
- Fast drop: 10.99 → 4.39 by iter 1000
- Steady descent through iter ~7000 (val 3.42)
- Last ~5000 iters yielded only ~0.1 val loss — clear diminishing returns

**Health**
- Train and val tracked very closely the whole run (gap ~0.05) → no meaningful overfitting
- ~9.34 s/iter, MFU ~13–15%
- ~6.3B tokens seen total (12k × 524,288)

**Comparison point**: nanoGPT's reference GPT-2 (124M) reproduction reaches ~2.85 val on OpenWebText after ~600k iters. You stopped at 1/50th of that compute, so 3.29 is roughly where you'd expect — model is undertrained, not broken.

Best checkpoint: `out-fineweb/` (saved at every eval — the iter-11500 save is your best val).
