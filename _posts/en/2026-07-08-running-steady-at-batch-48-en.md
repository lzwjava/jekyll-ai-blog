---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running Steady at Batch 48
translated: false
type: note
---

**Running steady at batch=48.** All good.

| Metric | Value |
| -------- | ------- |
| Step | **113 / 9,280 (1.22%)** |
| Loss | **4.43** (from 10.4 → rapid drop) |
| LR | 1.00 (at peak) |
| VRAM | **135 GB / 144 GB (93.5%)** |
| GPU util | 100% |
| Temp | **67°C** (cool — H200 runs well) |
| Step time | **11.5s** |
| Tok/sec | **136,700** |
| MFU | **66%** |
| Elapsed | **19.7 min** |
| ETA | **~29.3 hours** (~Jul 9 10:50 UTC) |

Loss curve: 10.4 → 4.43 in 113 steps. Healthy descent, no instability despite running at 93% VRAM.

Stable at batch=48. Temperature 67°C — plenty of thermal headroom. Let it ride.
