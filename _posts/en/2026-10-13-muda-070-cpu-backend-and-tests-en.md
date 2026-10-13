---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Muda 0.7.0: CPU Backend and Tests"
translated: false
type: note
---

Pushed as **`muda 0.7.0`** (`8bb848f`).

## What this round added

**`driver_cpu`** (`src/driver_cpu.c`) — a second, fully pluggable backend:

- Implements the entire memory/context/stream/event surface over host memory.
- Kernel launch returns `mudaErrorNotSupported` (clearly a reference backend).
- `MUDA_DRIVER=cpu` selects it; if OpenCL is missing, `mudaInit` now **auto-falls back** to it, so `muda` always initializes.

**`examples/reduction.cu`** — a real CUDA block reduction (shared memory + `__syncthreads` + `atomicAdd(float)`), compiled through `mudac` and run in `make test`. It matches the reference harmonic sum (14.4402) and exercises the float atomics from 0.6.0.

**`tests/test_memory.c`** + `make test-cpu` — a driver-independent memory/stream/event suite that runs against both backends.

## Verified

```
make test
  35 passed   core
  18 passed   mudaBLAS
  11 passed   mudart
   5 passed   CUDA source compatibility
   8 passed   memory/stream/event
  mudac vector_add: OK
  reduction: OK (got 14.4402, ref 14.4402)   <- new
  mudac 1D (ints, scalar arg): OK
  mudac 2D (dim3): OK

make test-cpu
  driver: cpu
  8 passed, 0 failed
```

That's **77 checks + 4 mudac programs**, all green.

## State of the project

`muda` now has: a CUDA-compatible API, a CUDA runtime shim, a `<<<>>>` preprocessor, a BLAS, a Python binding, two pluggable drivers, expanded CUDA intrinsics/atomics, and six example workloads — all without `libcuda` or `nvcc`.

## Remaining directions

1. **Native `nouveau` spike** — the true "no NVIDIA user space" path. I'd do this on a branch, with a tested `unbind`/`rebind` script and a clear warning, since it temporarily takes the M40 away from your ComfyUI/llama setup. This is the biggest remaining item.
2. **`cudaMemcpyToSymbol` + `__constant__`** — used by many CUDA samples.
3. **Performance** — double-buffered SGEMM to push past the current ~1.4 TFLOP/s toward the M40's ~6.8 TFLOP/s peak.

Which one should I take? If you're fine with the native path touching the driver (and a reboot to restore), I'll start there; otherwise I'd do `__constant__` support next.
