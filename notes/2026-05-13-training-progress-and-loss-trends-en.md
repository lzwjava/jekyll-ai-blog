---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress and Loss Trends
translated: false
type: note
---

## Progress (02:14 HKT Wed, +3h09m since last check)

**Current state:**

- iter **~4,440 / 19,073** — **23.3% done** (was 17.9% at 23:05)
- last val loss **3.3454** at iter 4000 (down from 3.40 at iter 3000)
- recent train losses settled in **3.0–3.4** band, occasional dip below 3.0 (iter 3740: 2.99, iter 3940: 2.99, iter 4020: 2.94)
- step time still **~11.11 s/iter**, MFU 12.84%
- **8 checkpoints saved** (500 → 4000); next save at iter 4500 in ~11 min
- no errors, no slowdowns

**Val loss trajectory** — still improving, slope flattening as expected:

| iter | val loss |
| ---- | -------- |
| 1000 | 4.04     |
| 1500 | 3.77     |
| 2000 | 3.57     |
| 2500 | 3.47     |
| 3000 | 3.40     |
| 3500 | 3.34     |
| 4000 | 3.35     |

Note: val at 4000 (3.345) is basically flat vs 3500 (3.343) — first time the eval-to-eval delta has been ~zero. Could be noise, could be the start of the slower-progress regime; worth watching at iter 4500/5000.

**Time remaining from now:**

| Stop at       | Iters left | Wall time            | ETA (HKT)  | Expected loss |
| ------------- | ---------- | -------------------- | ---------- | ------------- |
| 5,000         | ~560       | ~1.7 hrs             | ~04:00 Wed | ~3.30         |
| 10,000        | ~5,560     | ~17.2 hrs            | ~19:30 Wed | ~3.0–3.1      |
| 19,073 (full) | ~14,630    | ~45.2 hrs ≈ 1.9 days | ~23:30 Thu | ~2.9–3.0      |

Run is healthy and on pace. The 5,000-iter stop point is now just under 2 hours away if you want a natural early-exit window.
