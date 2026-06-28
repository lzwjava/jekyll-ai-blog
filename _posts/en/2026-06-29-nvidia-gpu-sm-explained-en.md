---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA GPU SM Explained
translated: false
type: note
---

Question: What does "SM" stand for in NVIDIA GPUs?

Answer:

**SM = Streaming Multiprocessor.**

It's the fundamental compute unit of an NVIDIA GPU. A GPU is essentially a collection of SMs (e.g., H100 has 132 SMs, RTX 4070 has 46 SMs). Each SM contains:

- **CUDA cores** (FP32/INT32 ALUs) — the scalar lanes
- **Tensor Cores** — matrix-multiply-accumulate units (the workhorse for GEMMs in deep learning)
- **Warp schedulers** — dispatch warps (groups of 32 threads) to execution units
- **Register file** — typically 64K 32-bit registers per SM
- **Shared memory / L1 cache** — fast on-chip scratchpad (configurable split, e.g. 228 KB on Hopper)
- **Load/Store units, SFUs** (special function units for transcendentals)

The execution model maps directly to this hierarchy: when you launch a CUDA kernel, **thread blocks** are assigned to SMs. The block stays resident on one SM for its lifetime, and the SM executes its threads in **warps of 32**. Occupancy — a number you'll see constantly in profiling — is the ratio of active warps to the SM's maximum, bounded by register and shared-memory pressure.

So in practice: more SMs + higher clocks + better Tensor Cores per SM = more throughput. When you tune a kernel (tile sizes, shared mem usage, register count), you're really tuning how well work packs into each SM.

References:

- [NVIDIA CUDA C Programming Guide — Hardware Implementation](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#hardware-implementation)
- [NVIDIA H100 Architecture Whitepaper](https://resources.nvidia.com/en-us-tensor-core)
