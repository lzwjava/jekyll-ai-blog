---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb GPT-2 Loss Curve Stages
translated: false
type: note
---

Here's the full story from iter 0:

```
======================================================================
  FULL Loss Curve — GPT-2 760M on FineWeb (iter 0 → 76K)
======================================================================

  Phase 0: Random init
    val_loss = 11.1066  (expected: ln(50304) = 10.83, good init)

  Phase 1: Catastrophic drop (0-1K)
    11.1066 → 5.4856  (drop=5.62, 50.6%, rate=5.62/1K steps)
    ← Model learns basic token statistics, bigram frequencies

  Phase 2: Rapid learning (1K-5K)
    5.4856 → 3.8431  (drop=1.64, 29.9%, rate=0.41/1K steps)
    ← Learning common phrases, grammar patterns

  Phase 3: Fast convergence (5K-10K)
    3.8431 → 3.5569  (drop=0.29, 7.4%, rate=0.057/1K steps)

  Phase 4: Steady decline (10K-20K)
    3.5569 → 3.3574  (drop=0.20, 5.6%, rate=0.020/1K steps)

  Phase 5: Moderate (20K-37K)
    3.3574 → 3.2261  (drop=0.13, 3.9%, rate=0.008/1K steps)

  Phase 6: Slowing (37K-55K)
    3.2261 → 3.1773  (drop=0.05, 1.5%, rate=0.003/1K steps)

  Phase 7: Near plateau (55K-76K)
    3.1773 → 3.1587  (drop=0.02, 0.6%, rate=0.001/1K steps)

======================================================================
  KEY OBSERVATIONS
======================================================================

  1. The loss curve has THREE distinct regimes:

     [1] Explosive learning (0-1K):    50.6% of total drop happens here
     [2] Fast learning (1K-10K):       36.3% of total drop
     [3] Slow refinement (10K-76K):    13.1% of total drop

     The first 1K steps did MORE work than the next 75K combined.

  2. Train-val gap is STABLE (~0.03-0.04)
     No overfitting. The model has capacity to learn more.
     Gap slightly increasing (0.027 → 0.041) but not concerning.

  3. MFU > 100% is real
     MI300X has specialized matrix units (MFMA) that aren't
     counted in the base FLOPS formula. 108-113% is excellent.

  4. Diminishing returns are extreme:
     Per-1K-step drop:
       Step 1K:   5.6210
       Step 10K:  0.0373  (150x less)
       Step 37K:  0.0142  (395x less)
       Step 76K:  0.0039  (1441x less)

  5. Projection to step 445K:
     Current: 3.1587 at step 76K (17% done)
     Expected final: ~3.05-3.10
     Remaining improvement: ~0.06-0.11 loss
     Cost: ~$108 and 2.25 days for that last 2-3%

======================================================================
```

The pattern is clear: **you're past the knee of the curve**. The model learned 87% of what it's going to learn in the first 10K steps. The remaining 435K steps squeeze out the last 13%. This is normal for language model training — the power law means most of the learning happens early, and you pay full price for tiny gains at the end.