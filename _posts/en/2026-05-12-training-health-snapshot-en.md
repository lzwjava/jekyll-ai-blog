---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Health Snapshot
translated: false
type: note
---

Looking healthy — training is alive and well. Status snapshot:

|                |                                                                      |
| -------------- | -------------------------------------------------------------------- |
| Process        | PID 1200744, running 1m34s, 88% CPU, alive                           |
| GPU            | 7.5 / 12.3 GB VRAM (~4.8 GB headroom), 100% util, 64°C               |
| Params         | 123.59 M ✓ (matches GPT-2 124M)                                      |
| Optimizer      | fused AdamW ✓                                                        |
| Shards         | train=1407, val=1 ✓                                                  |
| Step 0 eval    | train loss 11.0040, val loss 11.0031 ✓ (matches `ln(50304) ≈ 10.83`) |
| iter 0         | 17.16 s (includes warmup; subsequent iters drop to ~11 s)            |
| Last log write | 75 s ago — we're mid-iter, no print yet                              |

Why no recent log line? `log_interval=20`, so the next print is at iter 20. At ~11 s/iter that's ~220 s into the run (~3.5 min from process start) — should appear in the next minute or two.

Nothing to do. Everything is healthy. Check back in ~5 min to see the first `iter 20:` line and confirm steady-state per-iter time.