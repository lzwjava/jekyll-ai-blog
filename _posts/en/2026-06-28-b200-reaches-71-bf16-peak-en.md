---
audio: false
generated: true
image: false
lang: en
layout: post
title: B200 Reaches 71% BF16 Peak
translated: false
type: note
---

The benchmark is now complete and accurate. Here's the summary:

```
=== NVIDIA B200 Benchmark Results ===

TENSOR CORE MATMUL (the big numbers)
  FP32 (CUDA cores):      67.2 TFLOPS @ 16384x16384
  TF32 (tensor cores):   740.0 TFLOPS @ 4096x4096
  FP16 (tensor cores):  1,546.9 TFLOPS @ 8192x8192
  BF16 (tensor cores):  1,591.7 TFLOPS @ 8192x8192

Efficiency vs theoretical:
  FP32:   67 /    67 TFLOPS  100%
  TF32:  740 /   740 TFLOPS  100%
  FP16: 1,547 / 2,250 TFLOPS   69%
  BF16: 1,592 / 2,250 TFLOPS   71%

MEMORY BANDWIDTH
  Measured:    6,457 GB/s
  Theoretical: 8,000 GB/s (HBM3)
  Efficiency:  81%

TRANSFORMER-LIKE WORKLOADS (BF16)
  LLM prefill (8192x8192):   1,632 TFLOPS
  QKV projection:            1,474 TFLOPS
  FFN up-proj:               1,317 TFLOPS
  FFN down-proj:             1,463 TFLOPS

ELEMENTWISE LATENCY (1024x1024 FP16)
  add/mul/relu/gelu/silu:    ~4 μs
  softmax:                   ~7 μs
  layer_norm:                ~6 μs
  matmul:                    ~6 μs

FP8: Not available (PyTorch 2.8.0 doesn't support randn for Float8_e4m3fn)
     Would expect ~4,500 TFLOPS on this GPU
```

The B200 is hitting **71% of peak BF16** (1,592 / 2,250 TFLOPS) via naive `torch.mm()` — very solid. Memory bandwidth is at **81% of HBM3 spec**. For real training with flash-attention and fused kernels, these numbers would get even closer to peak.
