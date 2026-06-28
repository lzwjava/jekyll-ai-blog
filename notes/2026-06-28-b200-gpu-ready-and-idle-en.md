---
audio: false
generated: true
image: false
lang: en
layout: post
title: B200 GPU Ready and Idle
translated: false
type: note
---

B200 GPU is healthy and ready. Here's the summary:

```
=== B200 GPU Summary ===

Hardware
  GPU:              NVIDIA B200 (Blackwell architecture)
  Memory:           183 GB HBM3 (178.4 GB usable)
  SMs:              148
  Compute cap:      10.0
  PCIe:             Gen 5 x16
  ECC:              Enabled (0 errors)
  Temp:             33°C (idle)
  Power:            190W / 1000W limit

Software
  Driver:           580.126.20
  CUDA:             13.0 (driver) / 12.8 (PyTorch)
  PyTorch:          2.8.0+cu128
  Kernel:           6.8.0-107-generic

Host System
  CPU:              AMD EPYC 9555 64-Core
  RAM:              2.2 TB (446 GB used, 1.8 TB available)

Benchmarks
  Matmul 4096x4096:   415.8 ops/s
  Matmul 8192x8192:   59.8 ops/s
  Memory bandwidth:   2,222 GB/s
```

GPU is idle, no processes running, 182 GB free memory, 2.2 TB host RAM. The 80GB vs 183GB memory and 148 SMs confirm this is the full B200 (not a cut-down variant). Compute capability 10.0 is Blackwell-gen — supports FP4/FP8 natively, 5th-gen Tensor Cores.

Ready to train.
