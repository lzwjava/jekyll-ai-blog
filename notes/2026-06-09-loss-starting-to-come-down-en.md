---
audio: false
generated: true
image: false
lang: en
layout: post
title: Loss Starting to Come Down
translated: false
type: note
---

Good, loss is starting to come down (3.02 → 2.91 over the last 300 steps). Here's the full analysis:

---

TRAINING STATUS (step 130598/200000)
=====================================

lr schedule: CORRECT
  lrm = 1.00 (flat, as intended with --warmdown-ratio=0)

Effective LR math (after batch scaling by 0.3536):
  Old run at step 130k: matrix_lr=0.02 × 0.3536 × lrm(0.05) = 0.000354
  New run at step 130k: matrix_lr=0.001 × 0.3536 × lrm(1.0) = 0.000354
  => Same effective LR. No LR spike. ✓

Loss progression (raw per-step):
  step 130041: 2.839
  step 130110: 2.947  (↑ climbing)
  step 130260: 3.021  (↑ peak)
  step 130390: 2.984  (↓ starting to recover)
  step 130505: 2.983  (→ stabilizing)
  step 130598: 2.911  (↓ coming down)

Comparison with previous run:
  Old 130k run: smooth_train_loss = 2.602, val_bpb = 0.780
  Current raw loss ~2.91 is consistent (raw > smoothed always)

ONE ISSUE: Muon momentum
  Old run at step 130k: momentum = 0.90 (warmdown complete)
  New run: momentum = 0.97 (flat, warmdown-ratio=0)
  The 0.90→0.97 momentum jump caused the initial loss spike.
  It's recovering now (~600 steps in).

VERDICT: Training is healthy. The LR is correct. The initial bump was
from the momentum discontinuity, not the learning rate. Loss is trending
down again. Wait for the eval at step 135000 to confirm val_bpb improves.

If you want to also fix the momentum schedule for future runs, add
--warmdown-ratio=0.33 (so momentum decays 0.97→0.90 in the last 33%
of steps). But for now, let this run continue — it should converge.
