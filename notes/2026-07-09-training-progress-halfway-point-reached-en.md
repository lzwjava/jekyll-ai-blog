---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Training Progress: Halfway Point Reached"
translated: false
type: note
---

**Update: 35,436 → 39,923**

**Progress:**
- Step 39,923 / 87,000 -- **45.89%** (from 40.7%)
- Elapsed: 830 min (~13.8h)
- ETA: 979 min (~16.3h) remaining
- Gained ~4,487 steps since last check

**Loss:** Still bouncing **1.25 - 1.37** -- no real improvement. LR dropped to **0.84** (cosine schedule), but loss variance hasn't tightened.

**Perf:** Stable ~1.28s/step, ~51K tok/s. Slightly faster than before (was 1.32s).

**Bottom line:** Halfway through. LR is decaying but loss hasn't responded yet -- the next ~10K steps (LR down to ~0.6) will reveal whether this model has more to give or is near its floor on this dataset.