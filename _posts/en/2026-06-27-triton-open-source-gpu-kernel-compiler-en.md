---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Triton: Open-Source GPU Kernel Compiler"
translated: false
type: note
---

Here's what Triton is:

**Triton** (v3.8.0 in your checkout) is an open-source language + compiler for writing high-performance GPU kernels. Created by OpenAI (now under triton-lang org), it sits between CUDA and Python — you write kernels in Python-like syntax, and the compiler generates optimized GPU machine code (PTX for NVIDIA, AMDGCN for AMD).

**Core idea:** Instead of manually managing threads, shared memory, and synchronization like in CUDA C++, Triton lets you express computations at the *tile* level. You declare pointer blocks, and the compiler handles tiling, memory coalescing, and register allocation for you.

**Architecture (what's in the repo):**

1. **Frontend (Python)** — `python/triton/language/core.py` defines the DSL: `tl.load`, `tl.store`, `tl.dot`, `tl.program_id`, `tensor` operations. The `@triton.jit` decorator JIT-compiles Python functions into GPU kernels.

2. **Compiler (MLIR-based, C++)** — The heavy lifting:
   - `lib/Dialect/Triton/` — Triton IR dialect (the high-level tile ops)
   - `lib/Dialect/TritonGPU/` — TritonGPU IR (GPU-specific layout/scheduling)
   - `lib/Conversion/TritonToTritonGPU/` — Lower tiles → GPU-specific ops
   - `lib/Conversion/TritonGPUToLLVM/` — Lower to LLVM IR → PTX/AMDGCN

3. **GPU backends** — `third_party/nvidia/` (NVIDIA SM80+, WGMMA, tensor memory) and `third_party/amd/` (ROCm, MFMA, WMMA)

4. **Runtime** — `python/triton/runtime/` — JIT compilation, autotuning, caching, kernel launch

5. **Proton** — `third_party/proton/` — GPU profiler/diagnostic tool

6. **Gluon** — `python/triton/experimental/gluon/` — experimental lower-level DSL for fine-grained memory layout control

**What you'd actually write:**

```python
import triton
import triton.language as tl

@triton.jit
def add_kernel(X, Y, Z, N, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offsets = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offsets < N
    x = tl.load(X + offsets, mask=mask)
    y = tl.load(Y + offsets, mask=mask)
    tl.store(Z + offsets, x + y, mask=mask)
```

This compiles down to optimized PTX without you touching shared memory, warp scheduling, or memory coalescing logic.

**Why it matters for your trajectory:** Triton is *the* bridge between Python-level ML code and GPU hardware. Understanding the compiler pipeline (TTIR → TTGIR → LLVM IR → PTX) is exactly the kind of deep AI infra knowledge that separates ML engineers from AI engineers. It's also where Karpathy-style first-principles thinking meets real hardware — you need to understand memory hierarchies, warp-level primitives, and GPU architectures to write good Triton kernels.
