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

Running great. Here's the summary:

- Model: 286M params (depth=12, dim=768)
- Throughput: ~55,700 tok/sec (~1.17s per step)
- Loss: 10.40 → 7.25 (first 32 steps, warmup phase — loss dropping fast, all good)
- ETA: ~196 minutes (~3.3 hours) for 10K steps
- Val bpb at step 0: 3.22
- VRAM: well within 12GB (device_batch_size=8 is fine)
- GPU utilization: 98%

Everything looks healthy. Loss is decreasing smoothly during warmup. It'll slow down once warmup ends and LR stabilizes, then drop further during the long training phase.
