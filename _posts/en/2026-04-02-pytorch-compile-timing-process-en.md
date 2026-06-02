---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding PyTorch Compile Process and Timing
translated: false
type: note
---

Here's what's happening under the hood:

## torch.compile() — What It Does

`torch.compile()` transforms your model into optimized CUDA kernels via **TorchInductor**. It's not just-in-time in the simple sense — it goes through multiple phases:

### Phase 1: Graph Tracing (what you saw at iter 0)
- Torch runs the model once, recording every operation into a computational graph
- This is slow because it's running unoptimized
- 113s at iter 0 was this phase

### Phase 2: Kernel Compilation (what's happening now)
- Inductor analyzes the graph and generates **C++/CUDA kernels** for each operation
- It parallelizes this across 24 workers (`--workers=24`) to speed things up
- Each kernel is compiled independently, then linked together
- This is why you still see 21s/step — the kernel compilation is ongoing

### Phase 3: Code Generation & Optimization
- Once kernels are ready, Inductor fuses ops (e.g., combine matmul + bias + activation into one kernel)
- Reduces memory bandwidth and kernel launch overhead

## Why It's Slow Right Now

The compile workers are still building kernels in the background. Your GPU is at 100% Util because it's running the unoptimized model + simultaneously compiling new kernels. That's why:
- Power draw is high (691W) — GPU is working hard
- But step time is still 21s — because the compute graph isn't fused/optimized yet

## When It'll Get Fast

Once all workers finish (typically 2-10 minutes after training starts for a 1.5B model), you'll see:
- Step time drops from 21s → **1-3s**
- MFU jumps to realistic numbers (50-70%+)
- The "compiling the model..." message won't appear again

## Your Current State

```
GPU: 100% Util ✓ — working, not idle
Power: 691W ✓ — under load
Memory: 77GB ✓ — model loaded correctly
Workers: 24 compile workers running — waiting for completion
```

Everything looks correct. The 21s/step is temporary compilation overhead. By iter 100-200 you'll likely see the real speed.

## One More Thing

If `compile = True` but you'd rather skip the wait and just run (slower but immediately fast), you could set `compile = False`. But since you have 4-5 hours of training ahead, the compile wait (5-10 min) is worth it — it speeds up every subsequent step by 5-10x. 🦞
