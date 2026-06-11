---
audio: false
generated: true
image: false
lang: en
layout: post
title: M2 Air Performance Analysis
translated: false
type: note
---

Single-threaded scalar code on M2 Air — no SIMD, no threads. ~83M words × 22 inner iterations × 200-dim dot products is a lot. The original C code uses pthreads (4-12 threads).

The 344k words/s we measured on the tiny corpus was fine, but text8 has 16.7M tokens × 5 epochs = 83.5M words → ~240 seconds at that rate. But it's probably slower because the larger vocabulary (71k vs 137) means the 100M-entry negative sampling table doesn't fit in L2/L3 cache.

Want me to run it on your workstation (RTX 4070) instead? Should be similar speed since this is CPU-bound, but the i9 has more cores if I add threading.

Or I can add multi-threading to the training loop now — would cut time proportionally to core count (M2 has 4P+4E cores, so ~3-4x speedup).
