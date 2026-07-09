---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress and Loss Update
translated: false
type: note
---

**Update: 39,923 → 50,332**

**Progress:**

- Step 50,332 / 87,000 -- **57.85%** (from 45.89%)
- Elapsed: 1,047.6 min (~17.5h)
- ETA: 763.4 min (~12.7h) remaining
- Gained ~10,409 steps since last check

**Loss finally dropping:**

- Floor has shifted down to **1.12 - 1.24** (was 1.25-1.37)
- Hit a low of **1.126** at step 50,323
- Still bouncing, but the band has clearly moved down by ~0.13

**LR: 0.67** -- cosine decay is doing its job. The model is entering the phase where smaller LR steps let it settle into better minima. The gradient noise is the same, but the update direction is more consistent now.

**Perf:** ~1.25-1.37s/step, ~49-53K tok/s -- stable

**Vibe check:** Looking good. The loss floor dropped right as predicted (LR passing ~0.7-0.8 range). Still ~12.7h to go, and the LR will hit ~0 by the end -- the best gains often come in the last 30% of cosine schedule.
