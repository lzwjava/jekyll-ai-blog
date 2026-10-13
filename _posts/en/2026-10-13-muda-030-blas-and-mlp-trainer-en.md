---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Muda 0.3.0: BLAS and MLP Trainer"
translated: false
type: note
---

Milestone 1 is done and pushed as **`muda 0.3.0`** (`51f504c`).

## What was added

**`mudaBLAS`** (`include/mudablas.h`, `src/mudablas.c`) — row-major linear algebra on muda:

| | |
| --- | --- |
| `mudaSgemm` | shared-memory tiled, 64×64 block, 4×4/thread, all four transpose combos |
| `mudaSgemmNaive` | one-thread-per-element reference |
| `mudaSgemv` | transpose-aware |
| `mudaSaxpy` | float4 vectorized path |
| `mudaSscal` | |
| `mudaSrelu` / `mudaSreluBackward` | |
| `mudaSsigmoid`, `mudaSsub` | |
| `mudaSaddBias`, `mudaScolSum` | |

**Tuned SGEMM results on the M40:**

```
    size  naive GFLOP/s  tuned GFLOP/s    speedup
     256          274.8          590.9      2.15x
     512          320.5         1293.9      4.04x
    1024          243.8         1171.4      4.80x
```

**Tiny-MLP trainer** (`examples/mlp.c`) — 2-32-32-1 ReLU/sigmoid, full-batch SGD, forward+backward expressed entirely in `mudaSgemm` + elementwise kernels. Reaches **94%** on a circle-classification task (95% is Bayes-optimal given the injected 5% label noise).

**Tests** — `tests/test_mudablas.c`, 18 checks against CPU references (all transpose combos, non-multiple sizes, GEMV, AXPY/SCAL, activations, bias/reduction). `make test` now runs both suites: **35 + 18, 0 failures**.

## Bugs found and fixed along the way

- `expf` → `exp` (OpenCL C overloads `exp`; NVIDIA's compiler rejects `expf`).
- Launch config was passing the tile size (64) instead of the thread-block size (16) — fixed with separate tile/block params.
- A latent "read the cached kernel handle before lazy init" bug in the GEMM wrappers.

## Suggested next step (Milestone 2)

The drop-in CUDA **runtime** shim + Python binding:

1. `include/mudart.h` implementing `cudaMalloc`, `cudaMemcpy`, `cudaLaunchKernel`, `cudaDeviceSynchronize`, `<<<...>>>`-style launches via a `mudaConfigureCall`/`mudaSetupArgument` pair, so existing single-file `.cu` programs compile against muda with almost no edits.
2. A `ctypes` Python module (`muda.py`) with numpy interop, plus a `mudaBLAS`-backed `matmul`.

Want me to start Milestone 2?
