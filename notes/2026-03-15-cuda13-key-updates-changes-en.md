---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA 13 Key Updates and Breaking Changes
translated: false
type: note
---

Question: What are the major updates and changes in the CUDA 12.2.2 → 13.x (up to 13.2.0) upgrade?

Answer:

## CUDA 12.2.2 → 13.2.0: Major Changes Overview

This is a significant major version jump. Here's a comprehensive breakdown of what changed across the 13.x series:

---

### 🔴 Breaking Changes / Removals

**Dropped GPU Architecture Support**
- Support for Maxwell, Pascal, and Volta GPU architectures (compute capabilities below 7.5/Turing) has been removed. Offline compilation and library support for these architectures were dropped in CUDA 13.0.
- Supported architectures now: **Turing (RTX 20xx), Ampere (RTX 30xx), Ada Lovelace (RTX 40xx), Hopper (H100), Blackwell (B100/B200)**.

**Dropped OS Support**
- Ubuntu 20.04 support has been dropped starting with CUDA 13.0. Users are advised to migrate to Ubuntu 22.04 LTS or later.

**Deprecated Headers Removed**
- Legacy header files related to deprecated texture and surface references have been removed from the CUDA 13.0 runtime.

**Windows Driver Change**
- Starting with CUDA 13.1, the Windows display driver is no longer bundled with the CUDA Toolkit package. Users must download and install the NVIDIA driver separately.

---

### 🟢 New Programming Model: CUDA Tile

This is the headline feature of CUDA 13.x.

- CUDA 13.0 lays the foundation for a new, complementary tile-based programming model alongside the existing SIMT (Single Instruction, Multiple Threads) model.
- CUDA Tile brings a virtual ISA (Intermediate Representation) for tile-based parallel programming at a higher level than SIMT. It abstracts away tensor cores so that code using CUDA Tile is compatible with current and future tensor core architectures.
- CUDA 13.1 introduced CUDA Tile IR (a virtual instruction set for tile-based code generation) and **cuTile** — a Python DSL for authoring high-performance GPU kernels.
- CUDA 13.2 expanded CUDA Tile support to **Ampere and Ada (compute capability 8.x)** architectures, in addition to Blackwell (10.x, 11.x, 12.x).

---

### 🟢 New Hardware & Platform Support

- CUDA 13 adds support for NVIDIA's newest **Blackwell GPUs**, the **Jetson Thor** advanced AI and robotics GPU, and **DGX Spark** "desktop supercomputer".
- New OS support includes Red Hat Enterprise Linux 10, Debian 12.10, Fedora 42, and Rocky Linux 10.0/9.6.
- Unified ARM platform support: CUDA 13.0 introduced a single toolchain for both server-class and embedded ARM devices (Jetson Thor).

---

### 🟢 Performance & Library Updates

- Vector types have been updated with 32-byte alignment for increased performance on Blackwell GPUs. Libraries including cuBLAS, cuSPARSE, cuSOLVER, and cuFFT have been updated.
- The cuBLAS update in CUDA 13.0 introduced new APIs for boosting double-precision (FP64) matrix multiplication performance through FP emulation on Tensor Cores in GB200 NVL72 and RTX PRO 6000 Blackwell.
- NCCL 2.28 introduces fused communication and computation, enhancing performance for distributed AI and HPC workloads.

---

### 🟢 Compiler & Tooling Updates

- NVCC Compiler now supports **GCC 15** and **Clang 20**, with new language features to improve ABI integration.
- NVIDIA Compute Sanitizer 2025.4 adds NVCC compile-time patching via `-fdevice-sanitize=memcheck`, enhancing memory error detection and performance.
- CUDA 13.2 expanded developer tooling with **Nsight Python** for integrated kernel profiling in Python, initial support for **Numba-CUDA kernel debugging**, and **Nsight Copilot** (an AI CUDA assistant).

---

### 🟢 Python Ecosystem Updates (CUDA 13.2)

- CCCL 3.2 delivers modern CUDA C++ runtime APIs, introduces `cub::DeviceTopK` for efficient Top-K selection, new segmented scan and binary search primitives, and integrates with updated CUDA Python and CuPy.
- CuPy now supports CUDA 13.0 and 13.1 with wheels available on PyPI, and implements the **CUDA Stream Protocol** enabling zero-copy interoperability with PyTorch, JAX, and other frameworks.

---

### ⚠️ Important Compatibility Warning

If you rely on older GPUs (Maxwell/Pascal/Volta — GTX 900/1000/Volta series), this upgrade will **break compilation support** for those devices. You should stay on CUDA 12.x for those GPUs.

References:

- [CUDA Toolkit 13.2 Release Notes](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)
- [CUDA 13.2 Blog — NVIDIA](https://developer.nvidia.com/blog/cuda-13-2-introduces-enhanced-cuda-tile-support-and-new-python-features/)
- [CUDA 13.1 Blog — NVIDIA](https://developer.nvidia.com/blog/nvidia-cuda-13-1-powers-next-gen-gpu-programming-with-nvidia-cuda-tile-and-performance-gains/)
- [What's New in CUDA 13.0 — NVIDIA](https://developer.nvidia.com/blog/whats-new-and-important-in-cuda-toolkit-13-0/)
- [CUDA 13 Overview — All About Circuits](https://www.allaboutcircuits.com/news/nvidia-issues-major-update-cuda-toolkit-to-accelerate-cpus-gpus/)
