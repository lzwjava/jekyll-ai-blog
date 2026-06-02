---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA 13 主要更新和破坏性变更
translated: true
type: note
---

## CUDA 12.2.2 → 13.2.0：主要变更概述

这是一个重大的主要版本跳跃。以下是 13.x 系列中变更的全面分解：

---

### 🔴 破坏性变更 / 删除

**放弃的 GPU 架构支持**
- 已移除对 Maxwell、Pascal 和 Volta GPU 架构的支持（compute capabilities 低于 7.5/Turing）。这些架构的离线编译和库支持已在 CUDA 13.0 中删除。
- 支持的架构现为：**Turing (RTX 20xx)、Ampere (RTX 30xx)、Ada Lovelace (RTX 40xx)、Hopper (H100)、Blackwell (B100/B200)**。

**放弃的 OS 支持**
- 从 CUDA 13.0 开始，已放弃对 Ubuntu 20.04 的支持。建议用户迁移到 Ubuntu 22.04 LTS 或更高版本。

**已移除的弃用头文件**
- 与已弃用的 texture 和 surface references 相关的旧版头文件已在 CUDA 13.0 运行时中移除。

**Windows 驱动变更**
- 从 CUDA 13.1 开始，Windows 显示驱动不再捆绑在 CUDA Toolkit 包中。用户必须单独下载并安装 NVIDIA 驱动。

---

### 🟢 新编程模型：CUDA Tile

这是 CUDA 13.x 的亮点功能。

- CUDA 13.0 为新的、补充现有的 SIMT (Single Instruction, Multiple Threads) 模型的基于 tile 的编程模型奠定了基础。
- CUDA Tile 引入了比 SIMT 更高层次的基于 tile 的并行编程虚拟 ISA (Intermediate Representation)。它抽象了 tensor cores，使得使用 CUDA Tile 的代码与当前和未来的 tensor core 架构兼容。
- CUDA 13.1 引入了 CUDA Tile IR（用于基于 tile 的代码生成的虚拟指令集）和 **cuTile** — 一个用于编写高性能 GPU kernels 的 Python DSL。
- CUDA 13.2 将 CUDA Tile 支持扩展到 **Ampere 和 Ada (compute capability 8.x)** 架构，除了 Blackwell (10.x、11.x、12.x)。

---

### 🟢 新硬件与平台支持

- CUDA 13 添加了对 NVIDIA 最新 **Blackwell GPUs**、**Jetson Thor** 高级 AI 和机器人 GPU，以及 **DGX Spark** “桌面超级计算机”的支持。
- 新 OS 支持包括 Red Hat Enterprise Linux 10、Debian 12.10、Fedora 42 和 Rocky Linux 10.0/9.6。
- 统一的 ARM 平台支持：CUDA 13.0 为服务器级和嵌入式 ARM 设备（Jetson Thor）引入了单一工具链。

---

### 🟢 性能与库更新

- 向量类型已更新为 32 字节对齐，以提高在 Blackwell GPUs 上的性能。包括 cuBLAS、cuSPARSE、cuSOLVER 和 cuFFT 在内的库已更新。
- CUDA 13.0 中的 cuBLAS 更新引入了新 API，通过在 GB200 NVL72 和 RTX PRO 6000 Blackwell 的 Tensor Cores 上进行 FP 仿真来提升双精度 (FP64) 矩阵乘法性能。
- NCCL 2.28 引入了融合通信和计算，提升了分布式 AI 和 HPC 工作负载的性能。

---

### 🟢 编译器与工具更新

- NVCC 编译器现在支持 **GCC 15** 和 **Clang 20**，并引入新语言功能以改善 ABI 集成。
- NVIDIA Compute Sanitizer 2025.4 添加了通过 `-fdevice-sanitize=memcheck` 的 NVCC 编译时修补功能，提升了内存错误检测和性能。
- CUDA 13.2 通过 **Nsight Python**（用于 Python 中的集成 kernel 分析）、初步支持 **Numba-CUDA kernel 调试**，以及 **Nsight Copilot**（AI CUDA 助手）扩展了开发者工具。

---

### 🟢 Python 生态系统更新 (CUDA 13.2)

- CCCL 3.2 提供了现代 CUDA C++ 运行时 API，引入了 `cub::DeviceTopK` 用于高效 Top-K 选择、新分段扫描和二分搜索原语，并与更新的 CUDA Python 和 CuPy 集成。
- CuPy 现在支持 CUDA 13.0 和 13.1，并在 PyPI 上提供 wheels，并实现了 **CUDA Stream Protocol**，实现了与 PyTorch、JAX 和其他框架的零拷贝互操作。

---

### ⚠️ 重要兼容性警告

如果您依赖旧 GPU（Maxwell/Pascal/Volta — GTX 900/1000/Volta 系列），此升级将**破坏这些设备的编译支持**。对于这些 GPU，您应保留在 CUDA 12.x。

参考资料：

- [CUDA Toolkit 13.2 Release Notes](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)
- [CUDA 13.2 Blog — NVIDIA](https://developer.nvidia.com/blog/cuda-13-2-introduces-enhanced-cuda-tile-support-and-new-python-features/)
- [CUDA 13.1 Blog — NVIDIA](https://developer.nvidia.com/blog/nvidia-cuda-13-1-powers-next-gen-gpu-programming-with-nvidia-cuda-tile-and-performance-gains/)
- [What's New in CUDA 13.0 — NVIDIA](https://developer.nvidia.com/blog/whats-new-and-important-in-cuda-toolkit-13-0/)
- [CUDA 13 Overview — All About Circuits](https://www.allaboutcircuits.com/news/nvidia-issues-major-update-cuda-toolkit-to-accelerate-cpus-gpus/)
