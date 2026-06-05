---
audio: false
generated: true
image: false
lang: en
layout: post
title: FP8 vs FP32 Throughput Explained
translated: false
type: note
---

**Question:** Why does FP8 give a 16x throughput gain over FP32 when the bit width ratio is only 4x (32÷8)?

**Answer:**

The 16x comes from **two separate factors compounding**:

1. **Memory bandwidth × 4** — You fit 4x more FP8 values in the same byte-addressed memory bus
2. **Hardware parallelism × 4** — Tensor cores can execute 4 FP8 operations in the same clock cycles and silicon area as 1 FP32 operation

These **multiply**, not add: 4 × 4 = 16x.

Here's the GPU perspective:

**Memory side:**

```
Same 900 GB/s memory bandwidth, but:
- FP32: 900 GB/s ÷ 4 bytes = 225 GFLOPS (memory-limited)
- FP8:  900 GB/s ÷ 1 byte  = 900 GFLOPS (memory-limited)
```

**Hardware execution side:**
Modern GPUs (NVIDIA Hopper, H100) pack multiple FP8 operations per tensor core instruction:

```
FP32: 1 multiply-accumulate (MAC) per core per clock
FP8:  4 MACs per core per clock (in the same physical space)
```

When you have dense matrix operations (the 2614.9 TFLOPS figure), you're hitting **both advantages simultaneously**:

- 4x more data flows through (bandwidth)
- 4x more ops execute per clock (hardware)
- Result: 16x throughput

The key is that FP8 was designed specifically for this — NVIDIA's tensor cores have native FP8 instructions that exploit both the data density and the arithmetic parallelism.

**Why not always 4x then?** Because some workloads are compute-bound (not memory-bound). If you're memory-bandwidth-limited, you only get 4x. But for matrix multiplies on modern hardware with specialized tensor cores, you get the full 16x.
