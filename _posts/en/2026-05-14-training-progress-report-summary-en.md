---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Report Summary
translated: false
type: note
---

Healthy and on-track. Quick read:

| Metric          | Value                             | Verdict                        |
| --------------- | --------------------------------- | ------------------------------ |
| Elapsed         | 1h 14m                            | —                              |
| Iter            | 220 / 8000 (2.75%)                | —                              |
| Per-iter time   | **18.53 s** (rock-steady)         | Better than my 21.4 s estimate |
| Loss trajectory | 10.99 → 9.46 → 7.64 → 7.10 → 6.41 | Healthy descent                |
| MFU             | 13.7%                             | Normal for no-compile on 4070  |
| GPU             | 100% util, 9.7 GB, 64°C, 212 W    | All good                       |

**Revised total ETA:** 18.53 s × 8000 = **~41 hours** (≈ 1.7 days), faster than my earlier 47h projection. Should finish around **Saturday May 16, early morning**.

**First val checkpoint coming at iter 250** (~9 min from now). That's the first real quality signal — I'd expect val ≈ 6.0–6.5.

Nothing to do. Check back at iter 250 or iter 500 for the first val loss reading.