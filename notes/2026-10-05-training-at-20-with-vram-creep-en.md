---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training at 20% with VRAM Creep
translated: false
type: note
---

Re-checked at 19:33 — still running, just crossed 20%:

## Status @ 19:33 (was 16:30)

| Metric | Now | Last check |
|---|---|---|
| Progress | **step 749 / 3712 (20.18%)** | 614 (16.54%) |
| Loss | ~2.79–3.04 | ~2.97–3.11 |
| Speed | ~12.9–13.8k tok/s, 76–81 s/step, MFU 91–99% | ~13.0–13.6k |
| ETA | ~3,741 min ≈ **62.4 h ≈ 2.6 days** (finish ~Oct 8) | ~3,890 min |
| GPU | 100% util, **11.68/12.28 GB (95.1%)**, 56°C, 145 W, 2835 MHz | 11.32 GB |
| Process | PID 3976056 alive, 16h35m elapsed, 100% CPU | — |

**Checkpoints:** still only step 250 + 500 — you're literally *at* step 749, so the step-750 save (`model_000500` → `*_000750`, ~6.8 GB) should be writing right now.

**Two things to keep an eye on:**
1. **VRAM creeping up**: 11.36 → 11.32 → **11.68 GB** across checks (92% → 95%). Slight growth consistent with fragmentation — reinforces the earlier advice to add `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` before the step-2000 eval.
2. **Throughput slightly wobbly**: MFU bounces 91–99% (was pinned at ~99%) and steps vary 76–81 s. Nothing serious — GPU clocks are high (2835 MHz) and temp is cool.

Step 2000 eval (the OOM point of the previous run) is now ~27 h away, around **Oct 6 ~22:30**.