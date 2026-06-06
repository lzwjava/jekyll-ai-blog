---
audio: false
generated: true
image: false
lang: en
layout: post
title: LR Schedule Risk vs. Extension Options
translated: false
type: note
---

Here's the situation with extending to 130k steps:

```
=== SCHEDULE PROBLEM ===

The LR warmdown is tied to num_iterations. At 87k steps, the LR has
already decayed to near zero (warmdown started at step 30,450).

If you resume with --num-iterations 130000 --warmdown-ratio 0.65:
  - Warmdown restarts from step 45,500 to 130,000
  - At step 87k the new schedule gives lrm = 0.53 (was ~0 at end of old run)
  - This is an LR SPIKE — risky but could also help explore

=== OPTIONS ===

1) RESUME + ACCEPT LR BUMP (simplest)
   Command:
     python -m scripts.base_train \
       --resume-from-step 87000 \
       --num-iterations 130000 \
       --run rtx4070-d12-extended \
       --save-every 10000 \
       --eval-every 2000 \
       --warmdown-ratio 0.65

   Pros: simple, ~14 hours extra, loss was still decreasing
   Cons: LR jumps to 0.53 at step 87k — may cause a loss bump
   Risk: medium — the bump could destabilize or could help explore

2) RETRAIN FROM SCRATCH (cleanest)
   Same config but --num-iterations 130000 from the start.
   Pros: clean LR schedule, no discontinuities
   Cons: wastes the 28.4h already spent, total ~42.5 hours
   Risk: low

3) EXTEND WARMDOWN (most conservative)
   Resume with --warmdown-ratio 0.75 instead of 0.65
   At step 87k, lrm = 0.47 (still a bump, but smaller)
   Warmdown ends at step 130k — gives more flat training time

=== TIME & DATA ===
  Remaining:  43,000 steps → ~14 hours extra
  Total:      130,000 steps → ~42.5 hours
  Tokens:     8.5B total (32.6x params — beyond Chinchilla-optimal 20x)
  Note:       Going beyond Chinchilla is called "over-training" —
              you trade compute-optimal for better quality at inference time
              (fewer params needed for same performance). This is standard
              practice for deployed models.

=== VERDICT ===
Option 1 is worth trying — the loss was still decreasing at 87k, and a
brief LR bump before final convergence could help. If the loss explodes,
you can always stop and fall back to the 87k checkpoint.
```

Want me to kick off the extended training? I'd go with option 1 — resume from 87k with `--num-iterations 130000`. The LR bump is a risk but the model was healthy and you can always abort.
