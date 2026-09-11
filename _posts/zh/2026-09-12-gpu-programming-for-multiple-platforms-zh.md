---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多平台GPU编程
translated: true
type: note
---

问题：如何开始学习适用于 NVIDIA、AMD 以及跨平台开发的 GPU 编程？

答案：
学习 GPU 编程取决于你的重点是 **AI/深度学习**、**通用高性能计算 (GPGPU)** 还是**图形渲染**。

### 第一阶段：前提条件与核心基础

* **编程语言：** 掌握 **C++**（特别是现代 C++11/17/20）。高性能 GPU 编程严重依赖于 C/C++ 的 memory management、pointers 和 memory layout optimization。
* **计算机体系结构基础：** 理解硬件概念，例如 memory hierarchies（Registers、Shared Memory、L1/L2 Cache、Global VRAM）、SIMD/SIMT (Single Instruction Multiple Threads) 执行模型以及 latency hiding。
* **数学：** 巩固 linear algebra（matrices、vectors、dot products）以及并行数据结构。

---

### 第二阶段：选择主要方向

#### 路径 A：NVIDIA 生态（CUDA）

NVIDIA 的专有平台主导 AI/ML、科学计算以及工业 HPC。

* **核心 API：** 学习 **CUDA C/C++**。理解 Threads、Thread Blocks、Grids 和 Warp execution。
* **库：** 利用预构建的加速库，如 **cuBLAS** (linear algebra)、**cuDNN** (deep learning primitives) 和 **Thrust** (C++ template library)。
* **优化与性能分析：** 使用 **NVIDIA Nsight Systems** 和 **Nsight Compute** 等工具分析瓶颈、memory bandwidth 和 warp execution。

#### 路径 B：AMD 生态（ROCm & HIP）

AMD 使用为数据中心计算和高性能计算集群设计的开源工具。

* **Heterogeneous-Compute Interface for Portability (HIP)：** 用 HIP 编写代码，其语法与 CUDA 几乎相同，并可编译为同时面向 AMD（通过 ROCm）和 NVIDIA GPU 的目标。
* **工具链：** 学习 **ROCm** 栈、**hipBLAS**、**hipGRAPHICS**，并通过 **rocprof** 进行性能分析。

#### 路径 C：跨平台与厂商无关的解决方案

如果你想面向任意硬件平台（NVIDIA、AMD、Intel、Apple Silicon、移动设备）：

* **SYCL / OneAPI：** Khronos 标准，用现代 C++ 编写，可面向 CPU、GPU 和 FPGA。
* **OpenCL：** 底层、广泛支持的框架，适用于传统系统和非 NVIDIA 的移动硬件。
* **WebGPU / Vulkan Compute / Metal：** 最适合从图形开发转向，或构建需要直接访问 compute shaders 的跨平台 Web/桌面应用。

---

### 第三阶段：硬件与执行深入探究

* **内存优化：** 掌握 coalesce memory access、避免 shared memory 中的 bank conflicts 以及最大化 occupancy。
* **高级机制：** 学习使用 atomics 的无锁编程、warp intrinsics、streams/async execution 以及 dynamic parallelism。

---

### 推荐资源

* **书籍：** *Programming Massively Parallel Processors: A Hands-on Approach* (David B. Kirk 与 Wen-mei W. Hajj 著)。
* **文档与交互式教程：** *An Even Easier Introduction to CUDA* (NVIDIA Developer Blog)。
