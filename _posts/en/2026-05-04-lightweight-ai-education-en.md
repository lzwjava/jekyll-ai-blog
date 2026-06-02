---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lightweight AI Library for Education
translated: false
type: note
---

**Axono** is a lightweight AI/deep learning library (written in Chinese, targeting education/research use cases) with:

- **C++ core** (CPU + CUDA backends) with Python bindings via CMake
- **Tensor abstraction** with support for int8–float64 dtypes
- **Operators**: matmul (`@`), add (`+`), relu
- **NumPy interop**: `to_numpy()` / `from_numpy()`
- **Device support**: CPU and NVIDIA CUDA GPUs
- **Neural network module system** (`axono.nn`) with layers

Think of it as a minimal PyTorch-like framework for teaching tensor operations.
