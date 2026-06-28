---
audio: false
generated: true
image: false
lang: en
layout: post
title: Triton GPU Programming Language History
translated: false
type: note
---

Question: Give me an intro to the history of Triton, the GPU programming language.

Answer:

Triton started as **Philippe Tillet's PhD work** at Harvard. The foundational paper is *"Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations"* (MAPL 2019). The core thesis: GPU kernel authoring sits at an awkward extreme — CUDA gives you control but forces you to manually manage shared memory, coalescing, and warp-level scheduling; high-level DSLs hide the hardware but can't express novel ops. Triton's bet was a **tile-based abstraction**: you program in terms of blocks (tiles) of data, and the compiler handles intra-tile memory layout, coalescing, and SM scheduling.

Rough timeline:

- **2019** — MAPL paper. Original implementation was a standalone C++ compiler with a custom IR, LLVM backend targeting PTX. Tillet was the sole author.
- **2020** — Tillet joins OpenAI. Triton gets rewritten with a Python-embedded frontend (`@triton.jit` decorator). This is the inflection point — it goes from research artifact to something ML engineers actually use, because you write kernels in Python-looking code and get CUDA-class performance.
- **2021** — OpenAI open-sources it publicly with the blog post *"Introducing Triton."* The headline demo: a fused softmax and matmul matching cuBLAS/cuDNN in far fewer lines, no CUDA expertise required.
- **2022–2023** — The compiler is re-architected on top of **MLIR** (replacing the bespoke IR). This is a big deal architecturally — MLIR's dialect system lets Triton lower through progressive abstraction levels (Triton dialect → TritonGPU dialect → LLVM/PTX) and made multi-backend support tractable.
- **2023** — **PyTorch 2.0 ships `torch.compile`**, and its GPU backend **TorchInductor generates Triton code**. This is what made Triton infrastructure rather than a niche tool — suddenly every `torch.compile` user runs Triton kernels whether they know it or not.
- **2023–2024** — Backend expansion beyond NVIDIA: **AMD (ROCm/HIP)** support matures, Intel GPU backend, and CPU experiments. Relevant to you given the MI300X — Triton-on-ROCm is the path to portable kernels across your RTX 4070 and the MI300X without rewriting CUDA.

The programming-model insight worth internalizing: in CUDA you reason at **thread** granularity (each thread computes one element, you orchestrate the grid). In Triton you reason at **block/tile** granularity — a single `@triton.jit` "program instance" operates on a whole tile, and you express loads/stores with `tl.load`/`tl.store` over ranges plus masks. The compiler decides the thread mapping. That's why a Triton matmul is ~30 lines vs a few hundred for a competitive CUDA one — you've delegated the warp-level scheduling and shared-memory staging.

Minimal kernel to anchor the mental model — vector add:

```python
import triton
import triton.language as tl
import torch

@triton.jit
def add_kernel(x_ptr, y_ptr, out_ptr, n, BLOCK: tl.constexpr):
    pid = tl.program_id(0)                      # which tile am I
    offs = pid * BLOCK + tl.arange(0, BLOCK)    # this tile's element indices
    mask = offs < n                             # guard the ragged tail
    x = tl.load(x_ptr + offs, mask=mask)
    y = tl.load(y_ptr + offs, mask=mask)
    tl.store(out_ptr + offs, x + y, mask=mask)

def add(x, y):
    out = torch.empty_like(x)
    n = x.numel()
    grid = lambda meta: (triton.cdiv(n, meta["BLOCK"]),)
    add_kernel[grid](x, y, out, n, BLOCK=1024)
    return out
```

Note what's absent: no `threadIdx`, no `__shared__`, no explicit coalescing. `tl.arange` over a `BLOCK` and a `mask` is the whole tiling story. The `BLOCK: tl.constexpr` is compile-time specialized — Triton autotunes over these.

Where it sits today: Triton is the de-facto **kernel authoring layer for ML** when cuBLAS/cuDNN/FlashAttention don't already cover your op. FlashAttention-2/3, fused MoE kernels (directly relevant to your DeepSeek v4 MoE exploration — the expert-routing gather/scatter and grouped GEMM are exactly the kind of thing people write in Triton), and most custom fused ops in modern training stacks are Triton or Triton-adjacent. The strategic reason it won over "just write CUDA": it decouples kernel logic from hardware-specific scheduling, so the same kernel autotunes across SM generations and increasingly across vendors.

For your trajectory specifically: Triton is the highest-leverage GPU skill to build right now because (1) it's the substrate under `torch.compile`, (2) it's the practical path to MI300X kernels without CUDA's NVIDIA lock-in, and (3) writing a fused attention or MoE kernel in Triton teaches you the memory-hierarchy reasoning (SRAM tiling, recomputation vs materialization) that transfers to understanding *why* FlashAttention works at the math level.

References:

- [Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations (Tillet et al., MAPL 2019)](https://www.eecs.harvard.edu/~htk/publication/2019-mapl-tillet-kung-cox.pdf)
- [Introducing Triton (OpenAI, 2021)](https://openai.com/index/triton/)
- [Triton GitHub repository](https://github.com/triton-lang/triton)
- [Triton tutorials (official docs)](https://triton-lang.org/main/getting-started/tutorials/index.html)

I gave the history from what I have rather than searching, so treat the exact dates as approximate — the MLIR rewrite and ROCm-maturity timelines in particular shifted over multiple releases. If you want, I can pull the precise release-by-release changelog or the current state of the AMD backend.
