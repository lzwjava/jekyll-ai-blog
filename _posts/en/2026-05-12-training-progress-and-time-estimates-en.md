---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress and Time Estimates
translated: false
type: note
---

**Current state (16:23 HKT):**
- iter **1,260 / 19,073** — about **6.6%** done
- loss dropped 11.0 → **3.75** (val 4.04 at iter 1000)
- step time steady at **~11.1 s/iter**, MFU ~12.7%
- 2 checkpoints saved (500, 1000); no errors, no OOMs

**Time remaining (from now):**

| Stop at       | Iters left | Wall time from now                            | Expected loss |
| ------------- | ---------- | --------------------------------------------- | ------------- |
| 5,000         | ~3,740     | **~11.5 hrs** (done early tmrw morning)       | ~3.5–3.8      |
| 10,000        | ~8,740     | **~27 hrs** (done Wed evening)                | ~3.2–3.4      |
| 19,073 (full) | ~17,813    | **~55 hrs ≈ 2.3 days** (done ~Thu late night) | ~2.9–3.1      |

So pacing matches the original estimate — we've burned ~4 hrs, ~55 hrs to go for the full run. Pace and loss trajectory both look healthy; you can kill at any 500-iter boundary without losing the latest checkpoint.