---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Running at Full Capacity
translated: false
type: note
---

Training is running fine, not stuck at all.

Status:
- Process PID 71496: running at 99% CPU, 83 min uptime
- GPU: RTX 4070 at 100% utilization, 5050 MiB VRAM used, 65°C, 208W draw
- Script: `train.py config/train_github_code_124m.py` on nanoGPT

The only output so far are two warnings (deprecated GradScaler API + "not enough SMs for max_autotune_gemm"), but the GPU being pegged at 100% with 5GB VRAM confirms active computation. The inductor/compile step may have been slow initially, but it's crunching now.
