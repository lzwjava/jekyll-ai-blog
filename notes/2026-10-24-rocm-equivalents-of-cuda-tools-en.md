---
audio: false
generated: true
image: false
lang: en
layout: post
title: ROCm Equivalents of CUDA Tools
translated: false
type: note
---

Question: In the AMD ROCm ecosystem, what are the equivalents of CUDA and nvcc — and what replaces CUDA's "compute capability" (cc)?

Answer:

## Platform / SDK

| NVIDIA | AMD |
| --- | --- |
| **CUDA** (platform) | **ROCm** (Radeon Open Compute) |
| **CUDA API** (`cuda*` calls) | **HIP** (Heterogeneous-compute Interface for Portability) |

HIP is the direct programming model equivalent to CUDA. Code can often be ported with `hipify-perl` or `hipify-clang`, which mechanically converts `cuda*` → `hip*` prefixes.

---

## Compiler

| NVIDIA | AMD |
|---|---|
| **`nvcc`** | **`hipcc`** |

`hipcc` is a wrapper around `amdclang++` (LLVM-based). It routes to either the AMD GPU backend or, when targeting NVIDIA GPUs, can invoke `nvcc` — making HIP code portable across both vendors.

---

## Compute Capability (cc) equivalent

NVIDIA uses a simple integer pair (e.g. `sm_80` for Ampere, `sm_90` for Hopper).
AMD uses **`gfx` target identifiers** tied to the LLVM AMDGPU backend:

| AMD GPU | gfx target | Rough CUDA cc analog |
| --- | --- | --- |
| RX 5700 (RDNA1) | `gfx1010` | — |
| RX 6000 (RDNA2) | `gfx1030` | — |
| RX 7000 (RDNA3) | `gfx1100` | — |
| MI100 (CDNA1) | `gfx908` | — |
| MI200 series (CDNA2) | `gfx90a` | — |
| MI300 series (CDNA3) | `gfx940 / gfx941 / gfx942` | — |

You specify the target at compile time:

```bash
# nvcc equivalent
nvcc -arch=sm_80 kernel.cu -o kernel

# hipcc equivalent
hipcc --offload-arch=gfx90a kernel.hip -o kernel
```

Multiple targets at once (like nvcc's fat binary):

```bash
hipcc --offload-arch=gfx90a --offload-arch=gfx1100 kernel.hip -o kernel
```

---

## Quick Summary

| Concept | NVIDIA | AMD |
| --- | --- | --- |
| Platform | CUDA | ROCm |
| API | CUDA Runtime | HIP |
| Compiler | `nvcc` | `hipcc` (`amdclang++`) |
| Architecture target | `sm_XX` / compute capability | `gfxXXX` target |
| Porting tool | — | `hipify-clang` / `hipify-perl` |

The `gfx` number is the single most important thing to get right — using the wrong target means no GPU kernel will run, exactly like specifying the wrong `sm_` flag with nvcc.
