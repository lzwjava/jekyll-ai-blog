---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenCL CUDA Compatibility Harden
translated: false
type: note
---

Pushed as **`muda 0.6.0`** (`aca4fe6`).

## What this round added

I chose to harden the current stack rather than risk the native driver (unbinding `nvidia` would break your working ComfyUI/llama setup, and the Maxwell compute path is a multi-week effort).

**Expanded CUDA source compatibility** (`src/muda_translate.c`):
- Qualifiers: `__launch_bounds__(...)`, `__forceinline__`, `__inline__`, `__noinline__`, `__device_builtin__`, `__align__(...)`
- Math intrinsics: `fmaf`, `__expf`, `__exp10f`, `__logf`, `__log2f`, `__log10f`, `__powf`, `__sinf`, `__cosf`, `__tanf`, `__sqrtf`, `rsqrtf`, `__fdividef`, `__saturatef`, `__ldg`
- Atomics: `atomicAdd`, `atomicExch`, `atomicMax`, `atomicMin`, `atomicCAS` for `int`, `unsigned int`, `unsigned long`, **and `float`** (compare-and-swap loop)

**New**: `MUDA_CL_OPTIONS` env var to pass `clBuildProgram` options; `tests/test_translate.c` suite.

## The interesting debugging detour

I first tried `_Generic` for type dispatch, but the NVIDIA OpenCL compiler **silently always picks `default`** — `_Generic(1, int:7, default:0)` returned `0`, in both CL1.2 and CL3.0 modes. I switched to `__builtin_types_compatible_p(__typeof__(*(p)), float)`, which works correctly, and verified it end-to-end.

## Verified on the M40

```
make test
  35 passed   core runtime
  18 passed   mudaBLAS
  11 passed   mudart
   5 passed   CUDA source compatibility   (new)
  mudac vector_add: OK
  mudac 1D (ints, scalar arg): OK
  mudac 2D (dim3): OK
```

That's **69 checks + 3 mudac programs**, all green. Python binding still runs (SGEMM 1024³ ≈ 1.17 TFLOP/s).

## Where to go next

Options, in order of how safely completable they are:
1. **`driver_cpu`** — a memory-only reference backend (returns `NotSupported` for launches) so `mudainfo`/API tests run GPU-less. Quick.
2. **A reduction example** in normal `.cu` through `mudac`, using the new `atomicAdd` — a nice showcase.
3. **Native `nouveau` spike** — the true "no NVIDIA user space" path, on a throwaway/rebindable setup (I won't touch your live driver without explicit go-ahead).

Say the word and I'll continue with 1+2, or start the native spike on a branch.