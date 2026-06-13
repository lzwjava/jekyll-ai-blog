---
audio: false
generated: true
image: false
lang: en
layout: post
title: "TileLang: Pythonic DSL for GPU Kernels"
translated: false
type: note
---

**Question:** What is `tile-ai/tilelang`?

**Answer:**

TileLang is a **Pythonic DSL for writing high-performance GPU/CPU kernels**, built on top of TVM as a compiler backend. Think of it as the "middle ground" between writing raw CUDA/HIP (tedious, not portable) and using cuBLAS/CUTLASS (opaque, not flexible) — you get close-to-metal control with Python ergonomics.

**6.5k stars, 597 forks** — it's gaining real traction.

---

### What problem it solves

Writing kernels like FlashAttention, GEMM, or MLA by hand in CUDA requires dealing with:

- tile/block/thread hierarchy manually
- shared memory layout, bank conflicts
- async copy, pipelining (TMA on Hopper)
- warp-level matmul intrinsics (WMMA/WGMMA)

TileLang abstracts all of that while still letting you express the key algorithmic decisions (tile sizes, swizzle, pipeline stages).

---

### Core abstractions

```python
with T.Kernel(T.ceildiv(N, block_N), T.ceildiv(M, block_M), threads=128) as (bx, by):
    A_shared = T.alloc_shared((block_M, block_K), dtype)   # shared mem
    C_local  = T.alloc_fragment((block_M, block_N), accum_dtype)  # register tile

    T.clear(C_local)

    for ko in T.Pipelined(T.ceildiv(K, block_K), num_stages=3):  # async pipeline
        T.copy(A[by * block_M, ko * block_K], A_shared)  # parallelized gmem->smem
        T.copy(B[ko * block_K, bx * block_N], B_shared)
        T.gemm(A_shared, B_shared, C_local)  # dispatches to CuTe/HIP intrinsics

    T.copy(C_local, C[by * block_M, bx * block_N])
```

Key primitives:

- `T.Kernel(...)` — grid launch
- `T.alloc_shared` / `T.alloc_fragment` — smem and register tiles
- `T.Pipelined(...)` — software pipelining with `num_stages`
- `T.copy(...)` — parallelized async copy (maps to TMA on Hopper)
- `T.gemm(...)` — tile-level matmul (dispatches to WGMMA / WMMA / MatrixCore)
- `T.Parallel(...)` — elementwise over a tile
- `T.use_swizzle(panel_size=10)` — L2 cache swizzle

---

### Why it's relevant to you specifically

You trained GPT-2 on **MI300X** — TileLang explicitly supports MI300X with `Async Copy` support and even has a **FlashMLA implementation for AMD MI300X** that matches hand-optimized assembly (Aiter). This is directly useful if you want to write custom attention or MoE routing kernels for your training runs.

The DeepSeek MLA decode kernel is only **80 lines of Python** and matches FlashMLA on H100 — that's the kind of productivity/performance tradeoff this DSL is targeting.

---

### Stack

- **Compiler backend:** Apache TVM (with a heavily patched fork as submodule)
- **Targets:** CUDA (NVIDIA H100/A100/V100/4090/3090), HIP (AMD MI250/MI300X), Apple Metal, WebGPU, Huawei Ascend NPU
- **New backend (Dec 2025):** CuTe DSL — compiles to NVIDIA CUTLASS CuTe
- **SMT integration:** Z3 theorem prover embedded into TVM Arith for symbolic correctness verification
- **Language:** 50% Python, 48% C++

---

### TileLang vs alternatives

| | TileLang | Triton | CUTLASS/CuTe | Raw CUDA |
|---|---|---|---|---|
| Abstraction level | Tile | Block/warp | Thread block | Thread |
| Portability | CUDA+HIP+Metal | Mainly CUDA | CUDA only | CUDA only |
| Async pipeline control | ✅ explicit | ✅ | ✅ | manual |
| AMD support | ✅ MI300X | partial | ❌ | HIP |
| Pythonic | ✅ | ✅ | ❌ | ❌ |

The main differentiator vs Triton: TileLang gives you **explicit shared memory layout control and per-thread ops** (critical for dequant GEMM), while Triton abstracts that away. It's also used as the backend for **Microsoft BitBLAS** and **AttentionEngine**.

---

### Quick try on your RTX 4070

```bash
pip install tilelang
```

Then run the GEMM example from the README — it should JIT-compile and benchmark cleanly on CUDA.

For MI300X on AMD Dev Cloud:

```bash
pip install tilelang -f https://tile-ai.github.io/whl/nightly  # nightly for latest ROCm fixes
```

---

**References:**

- [tile-ai/tilelang GitHub](https://github.com/tile-ai/tilelang)
- [TileLang Puzzles (learning exercises)](https://github.com/tile-ai/tilelang-puzzles)
- [FlashMLA AMD MI300X example](https://github.com/tile-ai/tilelang/blob/main/examples/deepseek_mla/amd/README.md)
- [Microsoft BitBLAS (uses TileLang)](https://github.com/microsoft/BitBLAS)
