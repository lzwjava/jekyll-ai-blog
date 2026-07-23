---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD ROCm GPU计算栈
translated: true
type: note
---

这是 **ROCm** 单体仓库 — **AMD 的开源 GPU 计算平台**。

它是一个元仓库（GitHub 上的官方 `ROCm/ROCm` 仓库），用于记录和组织整个 ROCm 生态系统，包括：

- **HIP** — C++ 运行时 API 和内核语言（兼容 CUDA）
- **数学库** — rocBLAS、rocFFT、rocRAND、rocSPARSE 等
- **运行时与编译器** — ROCclr、ROCm-CompilerSupport、OpenMP、OpenCL
- **性能分析与调试** — rocprofiler、roctracer、ROCdbgapi
- **深度学习** — 与 PyTorch、TensorFlow 的集成
- **通信库** — RCCL（类似于 AMD 的 NCCL）

可以将其视为 NVIDIA CUDA 生态系统的 AMD 对应版本 — 一个完整的 GPU 加速 HPC、AI/ML 和科学计算栈，运行在 AMD GPU（Instinct、Radeon）上。这个特定的仓库是顶层清单/文档仓库，将所有子项目整合在一起。
