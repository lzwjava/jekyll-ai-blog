---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Axono: Deep Learning Framework Overview"
translated: false
type: note
---

Here's a comprehensive breakdown of **Axono**:

---

## What It Is

A **from-scratch deep learning framework** built in C++ with Python bindings — similar in spirit to a mini PyTorch, targeting education, research, and prototyping. Made by ByteRainTech, version 0.2.0, Apache 2.0 licensed.

---

## Architecture

### Layer Stack
```
Python API (axono.*)
      ↕  pybind11
C++ Core (libaxono) — shared .so/.dll
      ↕
CPU backend (OpenMP + AVX2/AVX SIMD)
CUDA backend (NVIDIA GPUs)
```

### Build System
- **CMake** (C++17) with pybind11 for Python bindings
- Auto-detects architecture: enables AVX2+FMA on x86, generic fallback on ARM
- Compiled with `-O3 -march=native -ffast-math` for maximum CPU performance
- Output: `python/axono/library/*.so` (loaded at runtime)

---

## Core Components

### `axono.core.Tensor`
Python wrapper around a C++ `Tensor` class. Key capabilities:
- **Dtypes**: `int8/16/32/64`, `float32/64`, `bool`
- **Devices**: `"cpu"` or `"cuda:<id>"`, switchable via `.to(device)`
- **Factory methods**: `Tensor.zeros()`, `Tensor.ones()`, `Tensor.full()`, `Tensor.randn()`
- **NumPy bridge**: `Tensor.from_numpy(arr)` / `tensor.to_numpy()` — zero-copy view where possible
- **Operators**: `@` (matmul), `+` (add), `.transpose()`
- **Mutation**: `.reshape()`, `.resize()`, `.fill()`, `.fill_zero()`

### `axono.core.operators` / `axono.core.ops`
Thin Python wrappers that delegate to C++ implementations:
- `matmul(a, b)` — matrix multiplication (CPU: OpenMP+SIMD, CUDA: cuBLAS-style kernel)
- `add(a, b)` — elementwise addition
- `relu(x, inplace=False)` — ReLU activation

Each operator has separate CPU and CUDA kernel headers under `include/axono/ops/{cpu,cuda}/`.

### `axono.nn`
- **`Module`** — base class tracking `_parameters` dict, mirrors PyTorch's `nn.Module`. Has `add_weight()`, `parameters()`, `train()`
- **`Linear`** — fully connected layer: `y = x @ W.T + b`, weights initialized with He-init (`scale = sqrt(2/in_features)`)

---

## C++ Internals (from headers)

```
include/axono/core/
├── tensor.h          # Core Tensor class
├── types.h           # DataType enum, Status codes
├── ops.h             # Op dispatch interface
├── module.h          # C++ Module base
├── macros.h          # Cross-platform macros
├── cpu/tensor/
│   ├── kernel.h      # CPU compute kernels
│   └── transpose.h   # CPU transpose
└── cuda/
    ├── detail.h      # CUDA helpers
    └── tensor/
        ├── kernel.h  # CUDA kernels
        └── transpose.h
```

---

## Performance (CPU benchmarks vs PyTorch & PaddlePaddle)

| Op | Axono vs Torch (4000×4000) |
|---|---|
| `from_numpy` | ~15× slower than Torch |
| `add` | comparable (~0.06s vs 0.07s) |
| `relu` | ~3× slower than Torch |
| `matmul` | ~10× slower than Torch |

Matmul is the weakest point — PyTorch uses highly optimized BLAS (MKL/OpenBLAS); Axono uses hand-written SIMD kernels which are educational but not production-tuned.

---

## Examples

The `examples/` directory shows the **aspirational API** (not all implemented yet):
- `mnist_classification.py` — CNN on MNIST using `axono.models.CNN`, `axono.train.Trainer`, `axono.data.DataLoader`, `axono.viz` — most of these modules don't exist in the current codebase, representing future roadmap
- `text_classification.py`, `time_series_prediction.py` — similarly aspirational

---

## Current State (v0.2.0)

**Implemented**: Tensor, from_numpy/to_numpy, matmul, add, relu, Linear layer, Module base class

**Not yet implemented** (referenced in examples): DataLoader, CNN models, Trainer, optimizers (Adam), visualization tools, `no_grad()` context

This is an **early-stage educational framework** with a solid C++/Python foundation and a clearly mapped-out roadmap toward a more complete PyTorch-like API.