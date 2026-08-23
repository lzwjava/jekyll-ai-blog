---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reading GPU-Burn Benchmark Output
translated: false
type: note
---

**Question:** How do I read/interpret the gpu-burn benchmark output?

**Answer:**

Here's a breakdown of each part of the output:

---

### Setup Info

```
GPU 0: NVIDIA GeForce RTX 4070
Initialized device 0 with 11839 MB of memory (10248 MB available, using 9223 MB of it), using FLOATS
Results are 268435456 bytes each, thus performing 34 iterations
```

- **11839 MB** — total VRAM on the card
- **10248 MB available** — free VRAM at test start (some is reserved by the OS/driver)
- **9223 MB used by test** — gpu-burn allocates ~90% of available VRAM to stress it
- **FLOATS** — using 32-bit float precision (vs DOUBLES for FP64)
- **34 iterations** — how many matrix multiplication passes fit in the allocated memory

---

### Progress Lines

```
65.0%  proc'd: 238 (20497 Gflop/s)   errors: 0   temps: 60 C
```

| Field | Meaning |
| --- | --- |
| `65.0%` | % of the 20-second burn elapsed |
| `proc'd: 238` | Total matrix multiplication batches completed so far |
| `20497 Gflop/s` | Throughput — **~20.5 TFLOPs**, your GPU's FP32 compute speed |
| `errors: 0` | No computational errors detected (values compared against CPU reference) |
| `temps: 60 C` | GPU core temperature at that moment |

---

### What the Numbers Mean for Your RTX 4070

- **~20,400 Gflop/s (~20.4 TFLOPs)** — consistent and healthy; the RTX 4070's rated FP32 is ~29 TFLOPs, but gpu-burn typically achieves 60–75% of peak due to memory bandwidth and overhead, so this is **normal**
- **Temps peaked at 61°C** — very cool for a full load test; excellent thermal headroom
- **errors: 0** — GPU compute is stable, no memory bit-flip or calculation errors
- **Final verdict: `GPU 0: OK`** — the card passed the burn test

---

### Summary

Your RTX 4070 is **healthy**: consistent throughput, cool temperatures, and zero errors across the entire 20-second stress test.

---

**References:**

- [gpu-burn GitHub Repository](https://github.com/wilicc/gpu-burn)
