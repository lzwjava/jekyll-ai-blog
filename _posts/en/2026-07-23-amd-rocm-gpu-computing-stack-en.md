---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD ROCm GPU Computing Stack
translated: false
type: note
---

This is the **ROCm** monorepo — **AMD's open-source GPU computing platform**.

It's a meta-repository (the official `ROCm/ROCm` repo on GitHub) that documents and organizes the entire ROCm ecosystem, which includes:

- **HIP** — C++ runtime API & kernel language (CUDA-compatible)
- **Math libraries** — rocBLAS, rocFFT, rocRAND, rocSPARSE, etc.
- **Runtimes & compilers** — ROCclr, ROCm-CompilerSupport, OpenMP, OpenCL
- **Profiling & debugging** — rocprofiler, roctracer, ROCdbgapi
- **Deep learning** — integrations with PyTorch, TensorFlow
- **Communication libraries** — RCCL (like NCCL for AMD)

Think of it as the AMD equivalent of NVIDIA's CUDA ecosystem — a full stack for GPU-accelerated HPC, AI/ML, and scientific computing on AMD GPUs (Instinct, Radeon). This particular repo is the top-level manifest/doc repo that ties all the sub-projects together.
