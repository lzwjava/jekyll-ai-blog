---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HIP：异构计算可移植接口
translated: true
type: note
---

问题：HIP 代表什么，含义是什么？

回答：**HIP** 代表 **Heterogeneous-compute Interface for Portability**（异构计算可移植接口）。

它是 AMD 开发的一个开源 C++ 运行时环境和编程模型。它允许开发者从单一源代码库编写可在 AMD 和 NVIDIA GPU 上运行的便携代码。

---

### HIP 的关键概念

#### 1. 代码可移植性

在 HIP 出现之前，为 NVIDIA GPU 编写的代码使用 **CUDA**，这无法在 AMD 硬件上原生运行。HIP 通过提供与 CUDA 高度相似的语法解决了这个问题，使开发者能够维护一个单一的 C++ 代码库，在两个平台上编译和运行：

* 在 NVIDIA 平台上编译时，HIP 直接映射到 CUDA，性能开销为零。
* 在 AMD 平台上编译时，它使用 AMD 的 ROCm 编译器（如 `hipcc`）在 AMD 硬件上运行。

#### 2. 生态系统角色

HIP 充当了一个翻译和抽象层。AMD 提供了一个名为 **HIPIFY** 的工具，它可以自动将现有的 CUDA 代码转换为 HIP C++ 代码。转换后，代码可以针对任意硬件系列。

| 特性 | NVIDIA 生态系统 | AMD 生态系统 |
| --- | --- | --- |
| **语言/接口** | CUDA | **HIP** |
| **编译器** | `nvcc` | `hipcc`（使用 LLVM/Clang） |
| **硬件目标** | GeForce / Tesla / Hopper / Blackwell | Radeon / Instinct（例如 MI300X） |

#### 3. 为什么它在您分享的日志中很重要

在您之前的日志中，您看到了诸如 `/opt/rocm-7.2.0/bin/hipcc` 的命令以及以 `.hip` 结尾的源文件。这意味着 **FlashAttention** 代码（最初为 NVIDIA CUDA 编写）已通过 HIP 进行了适配，以便能够在 AMD Instinct GPU 上高效编译和执行。
