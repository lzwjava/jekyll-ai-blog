---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Ahead of Projection
translated: false
type: note
---

Big jump since the snapshot — run is now at **iter ~6,180 / 19,073 (~32.4%)** and val loss is well below what the projection expected.

Val loss progression (last 5 evals):

```
iter 4000 → 3.3454
iter 4500 → 3.2967  (delta -0.049)
iter 5000 → 3.2596  (delta -0.037)
iter 5500 → 3.2581  (delta -0.002)  ← briefly flat
iter 6000 → 3.2473  (delta -0.011)
```

So the "iter 4000 flat" reading was noise, not the slow-progress regime — val resumed its decline. We've already blown past the ~3.30 target the snapshot put at the 5,000-iter stop (actual at 5000: **3.26**).

Other vitals — all unchanged / nominal:
- Step time **11.10–11.11 s/iter**, MFU **12.86%**
- Checkpoints saved cleanly at 4500, 5000, 5500, 6000 (12 total now)
- No errors, no slowdowns
- Train losses keep dipping into the 2.9s (iter 5700: 2.93, 5780: 2.95, 5960: 2.94)

Updated time-remaining from now (iter 6,180, ~11.11 s/iter):

```
Stop at        Iters left   Wall time    ETA (HKT)
10,000         ~3,820       ~11.8 hrs    ~14:00 Wed
19,073 (full)  ~12,890      ~39.8 hrs    ~17:30 Thu
```

Run is healthy and **ahead of the loss curve** the snapshot projected. Nothing to do.
