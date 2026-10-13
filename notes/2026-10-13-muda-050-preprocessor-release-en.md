---
audio: false
generated: true
image: false
lang: en
layout: post
title: Muda 0.5.0 Preprocessor Release
translated: false
type: note
---

Milestone 3 is done and pushed as **`muda 0.5.0`** (`4ea6be2`).

## What was added

**`mudac` — a `<<<...>>>` preprocessor** (`tools/mudac.c`)

It turns a normal `.cu` file into something that compiles against muda, with no `nvcc`:

```sh
make build/mudac
build/mudac prog.cu -o prog.cc
c++ -std=gnu++17 -Iinclude prog.cc build/libmuda.a -ldl -lpthread -lm -o prog
./prog
```

It:
1. **Extracts** every `__global__`/`__device__` function into a string constant and removes the definition from the host code (the driver compiles it at runtime).
2. **Rewrites** `kernel<<<grid, block, shared, stream>>>(a, b, n)` into `mudartLaunchByName("kernel", ...)`, using a GNU statement expression to take the address of each argument — so `2.0f`, `n+1`, etc. work.
3. **Replaces** `#include <cuda_runtime.h>` with `#include "mudart.h"`.

Dimensions can be ints or `dim3`; the generated code picks whichever you wrote.

## Runtime support added to `mudart`
- `mudartLoadKernelSource` / `mudartLaunchByName` with a name→function cache
- A runtime constructor so `cudaMalloc` works before the first launch
- C++ `dim3` constructor + overloaded dimension helpers (for C++ compilation), with `MUDAC_AUTO` mapping to `auto` in C++ and `__auto_type` in C

## Verified
```
make test
  35 passed  (core)
  18 passed  (mudaBLAS)
  11 passed  (mudart)
  mudac vector_add: OK                          # stock CUDA program
  mudac 1D (ints, scalar arg): OK
  mudac 2D (dim3): OK
```

Two real bugs found and fixed: C++ overloads can't live inside `extern "C"`, and `-x c++` must be reset with `-x none` before passing the static archive.

## Where this leaves the project
`muda` now covers the full arc: raw runtime → CUDA-compatible API → CUDA runtime shim → `<<<>>>` source front-end → BLAS + MLP demo → Python. The README roadmap lists next steps (`cudaMemcpyToSymbol`/`__constant__` in mudac, double-buffered GEMM, a `driver_cpu`, and the native `driver_nouveau`).

Want me to keep going with the **native `nouveau` backend spike** (the real "no NVIDIA user space" path), or harden the current stack (more mudac coverage + `driver_cpu` for GPU-less CI)?