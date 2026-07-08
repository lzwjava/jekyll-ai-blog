---
audio: false
generated: true
image: false
lang: en
layout: post
title: H200 Training Runs Smoothly
translated: false
type: note
---

Training is running smoothly on the H200. Here's the status:

**Model**: d24 — 24 layers, 1536 dim, 12 heads, **1.38B params** (config shows it's actually bigger than the original 760M reference)
**FP8**: enabled (145/158 layers converted)

**Performance**:

- **~129K tokens/sec** — nearly **2× the MI300X** (68K tok/s)
- **~62% MFU** — much higher than MI300X (27%) thanks to FA3 + FP8 on H200
- **~4.1s per step**
- **ETA: ~33 hours** (vs 62h on MI300X)

**Training curve** (looking good):

```
step   0: loss 10.40
step  10: loss  9.16
step  20: loss  7.21
```

Loss is dropping cleanly — healthy start. At this rate the full 29K steps should finish in ~33 hours, significantly faster than the original MI300X estimate.
