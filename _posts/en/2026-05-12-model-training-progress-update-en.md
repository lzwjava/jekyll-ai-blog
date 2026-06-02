---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Training Progress Update
translated: false
type: note
---

## Progress (23:05 HKT, +6h42m since your 16:23 snapshot)

**Current state:**

- iter **~3,420 / 19,073** — **17.9% done** (was 6.6% at 16:23)
- last val loss **3.4043** at iter 3000 (down from 4.04 at iter 1000)
- recent train losses bouncing in **3.2–3.5** band (was 3.7–3.9 last check)
- step time still **~11.11 s/iter**, MFU 12.83%
- **6 checkpoints saved** (500 → 3000); next save at iter 3500 in ~16 min
- no OOMs, no errors, no slowdown

**Val loss trajectory** — healthy, slope flattening as expected:

| iter | val loss |
| ---- | -------- |
| 1000 | 4.04     |
| 1500 | 3.77     |
| 2000 | 3.57     |
| 2500 | 3.47     |
| 3000 | 3.40     |

**Time remaining from now:**

| Stop at       | Iters left | Wall time            | ETA (HKT)  | Expected loss |
| ------------- | ---------- | -------------------- | ---------- | ------------- |
| 5,000         | ~1,580     | ~4.9 hrs             | ~04:00 Wed | ~3.2–3.3      |
| 10,000        | ~6,580     | ~20.3 hrs            | ~19:30 Wed | ~3.0–3.1      |
| 19,073 (full) | ~15,650    | ~48.3 hrs ≈ 2.0 days | ~23:00 Thu | ~2.9–3.0      |

We've shaved roughly 7 hours off the full-run ETA since 16:23. Run is on rails — pace is steady, loss is decreasing monotonically at the eval boundaries, and you can still kill at any 500-iter mark without losing the latest checkpoint.
