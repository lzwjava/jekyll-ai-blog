---
audio: false
generated: true
image: false
lang: en
layout: post
title: Progress Update and Loss Plateau
translated: false
type: note
---

**Update from last check (25,600 → 35,436):**

**Progress:**

- Step 35,436 / 87,000 -- **40.7%** (up from 29.4%)
- Elapsed: 736 min (~12.3h) -- added ~3.5h
- ETA: 1,072 min (~17.9h) remaining
- Gained **~9,836 steps** since last check

**Loss:**

- Still bouncing in **1.25 - 1.39** range
- No sustained improvement trend -- variance dominates, same as before
- lrm dropping to **0.92** (cosine LR schedule kicking in)

**Performance:**

- dt ~1.32s/step, ~49K tok/s -- slightly slower than before (was ~1.23s)
- bf16_mfu ~148-152% -- MFU calc still buggy
- pq: 20 rg: 1 -- data pipeline stable

**Takeaway:** ~18h to go. Loss hasn't meaningfully dropped from the 1.25-1.45 band seen at 29%. The LR decay just started (0.92), so the next ~30K steps where LR drops to ~0 will tell us if this model can compress further or if it's plateaued.
