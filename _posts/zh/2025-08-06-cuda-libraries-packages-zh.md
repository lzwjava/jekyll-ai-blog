---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA库与软件包
translated: true
type: note
---

以下是您正在安装的各个软件包的简要说明：

* **nvidia-cusparselt-cu12**
  NVIDIA cuSPARSELt 库，用于在 CUDA 12 上实现超高效低精度稀疏矩阵运算。

* **nvidia-cusparse-cu12**
  cuSPARSE 库，提供在 CUDA 12 上运行的通用稀疏线性代数例程（如稀疏求解器）。

* **nvidia-cudnn-cu12**
  cuDNN 库，为 CUDA 12 上的深度神经网络提供高度优化的基础算子（卷积、池化、激活函数等）。

* **nvidia-cublas-cu12**
  cuBLAS 库，在 CUDA 12 上实现高性能稠密线性代数（BLAS）例程。

* **nvidia-cufft-cu12**
  cuFFT 库，用于在 CUDA 12 设备上计算快速傅里叶变换。

* **nvidia-cusolver-cu12**
  cuSOLVER 库，包含在 CUDA 12 上运行的稠密/稀疏直接求解器、特征值问题求解等例程。

* **nvidia-curand-cu12**
  cuRAND 库，用于在 CUDA 12 上生成高质量随机数。

* **nvidia-cufile-cu12**
  cuFile 库，支持在 CUDA 12 上实现直接异步的 GPU 加速文件 I/O 操作。

* **nvidia-nvtx-cu12**
  NVTX（NVIDIA 工具扩展），用于在 CUDA 12 环境中标注和分析代码执行区间。

* **nvidia-nvjitlink-cu12**
  NVJITLink 库，支持在 CUDA 12 运行时即时链接（JIT-link）CUDA 内核。

* **nvidia-cuda-nvrtc-cu12**
  NVRTC 运行时编译器，用于在 CUDA 12 环境下动态编译 CUDA C 内核代码。

* **nvidia-cuda-cupti-cu12**
  CUPTI（CUDA 性能分析工具接口），用于在 CUDA 12 上采集细粒度性能分析和跟踪数据。

* **nvidia-cuda-runtime-cu12**
  核心 CUDA 运行时库，用于在 CUDA 12 上管理并启动内核。

* **nvidia-nccl-cu12**
  NCCL 库，为 CUDA 12 提供高效的多 GPU 和多节点集合通信基础算子。

* **torch**
  核心 PyTorch 库，支持张量运算、自动微分和深度学习模型构建。

* **networkx**
  用于创建、操作和分析复杂网络与图结构的 Python 软件包。

* **mpmath**
  纯 Python 库，支持任意精度实数和复数运算。

* **sympy**
  用于符号数学（代数、微积分、方程求解等）的 Python 库。

* **triton**
  一种编程语言和编译器，可帮助比原始 CUDA 更轻松地编写自定义高性能 GPU 内核。
