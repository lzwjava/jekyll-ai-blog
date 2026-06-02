---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD ROCm 开放 GPU 计算平台
translated: true
type: note
---

以下是这个项目的介绍：

**AMD ROCm（Radeon Open Compute）—— 官方开源 GPU 计算平台**

克隆自：`git@github.com:ROCm/ROCm.git`

它是 AMD 对标 NVIDIA CUDA 的产品——一个面向 GPU 计算的开源软件栈，专注于 HPC、AI/ML、科学计算和 CAD 工作负载。

**此仓库的主要组成部分：**

1. **文档** (`docs/`) —— 主要的 ROCm 文档站点（基于 Sphinx），涵盖安装指南、API 参考、兼容性矩阵、概念概述、操作指南和发布说明。这实际上是此仓库的主要内容。

2. **构建系统** (`tools/rocm-build/`) —— 97 个 Shell 脚本和配置文件，用于从源码构建各个 ROCm 子项目。包括以下构建脚本：
   - 数学库：rocBLAS、rocFFT、rocRAND、rocSOLVER、rocSPARSE、hipBLAS 等。
   - 机器学习/计算机视觉：MIOpen、MIVisionX、AMDMIGraphX
   - 通信：RCCL（集合通信）
   - 编译器/运行时：HIP、LLVM、ROCclr、HSA 运行时
   - 性能分析：ROCm Profiler、Omniperf、Omnitrace
   - 适用于 Ubuntu 22/24 的 Docker 构建环境

3. **仓库清单** (`default.xml`) —— 一个 repo-tool 清单文件，将约 30 多个子项目固定到 `rocm-7.2.0` 标签（ROCK 内核驱动、HIPIFY、LLVM、ROCgdb、可组合内核等）。通过它可以 `repo sync` 获取完整的源码树。

4. **CMakeLists.txt** —— 一个轻量级的 CMake 包装器（v5.7.1），主要用于构建文档。

5. **CHANGELOG.md** （490KB）—— 所有 ROCm 版本的详细发布历史。

**总结：** 此仓库是整个 ROCm 平台的伞式/清单仓库。它不包含实际的运行时或库源码（那些位于单独的仓库中，如 `ROCm/rocm-systems`、`ROCm/llvm-project` 等）。相反，它提供：文档、构建编排脚本以及用于将所有子项目组装成连贯版本的仓库清单。
