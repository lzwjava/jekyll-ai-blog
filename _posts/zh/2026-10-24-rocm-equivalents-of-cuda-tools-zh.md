---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ROCm的CUDA工具等价物
translated: true
type: note
---

问题：在AMD ROCm生态系统中，CUDA和nvcc的等价物是什么？什么替代了CUDA的"compute capability" (cc)？

答案：

## Platform / SDK

| NVIDIA | AMD |
|---|---|
| **CUDA** (platform) | **ROCm** (Radeon Open Compute) |
| **CUDA API** (`cuda*` calls) | **HIP** (Heterogeneous-compute Interface for Portability) |

HIP是直接等同于CUDA的programming model。Code通常可以通过`hipify-perl`或`hipify-clang`进行port，它们会自动将`cuda*` prefix转换为`hip*` prefix。

## Compiler

| NVIDIA | AMD |
|---|---|
| **`nvcc`** | **`hipcc`** |

`hipcc`是`amdclang++`（基于LLVM）的wrapper。它可以route到AMD GPU backend，或者当targeting NVIDIA GPUs时，可以invoke `nvcc`——使得HIP code能够在两个vendors之间port。

## Compute Capability (cc) equivalent

NVIDIA使用simple integer pair（例如，`sm_80`用于Ampere，`sm_90`用于Hopper）。AMD使用**`gfx` target identifiers** tied to LLVM AMDGPU backend:

| AMD GPU | gfx target | Rough CUDA cc analog |
|---|---|---|
| RX 5700 (RDNA1) | `gfx1010` | — |
| RX 6000 (RDNA2) | `gfx1030` | — |
| RX 7000 (RDNA3) | `gfx1100` | — |
| MI100 (CDNA1) | `gfx908` | — |
| MI200 series (CDNA2) | `gfx90a` | — |
| MI300 series (CDNA3) | `gfx940 / gfx941 / gfx942` | — |

在compile time指定target：

```bash
# nvcc equivalent
nvcc -arch=sm_80 kernel.cu -o kernel

# hipcc equivalent
hipcc --offload-arch=gfx90a kernel.hip -o kernel
```

一次指定多个targets（类似nvcc的fat binary）：

```bash
hipcc --offload-arch=gfx90a --offload-arch=gfx1100 kernel.hip -o kernel
```

## Quick Summary

| Concept | NVIDIA | AMD |
|---|---|---|
| Platform | CUDA | ROCm |
| API | CUDA Runtime | HIP |
| Compiler | `nvcc` | `hipcc` (`amdclang++`) |
| Architecture target | `sm_XX` / compute capability | `gfxXXX` target |
| Porting tool | — | `hipify-clang` / `hipify-perl` |

`gfx` number是最需要get right的single most important thing——使用wrong target意味着no GPU kernel will run，完全类似于使用nvcc指定错误的`sm_` flag。