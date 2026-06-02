---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch框架仓库概述
translated: true
type: note
---

这是 **PyTorch** 仓库——Meta 的开源 machine learning 框架。以下是概述：

**它是什么：**
- 一个 Python-first 的 deep learning 框架，提供 tensor computation 与 GPU acceleration，以及基于 tape 的 autograd 系统用于训练 neural networks
- 版本：**2.13.0a0**（dev/trunk 构建）
- 从 `git@github.com:pytorch/pytorch.git` 克隆

**代码库规模：**
- 约 4,464 个 Python 文件，约 2,077 个 C++ 文件（不含 third_party）
- 磁盘占用约 224 MB（不含 .git）

**关键目录：**
- `torch/` —— 核心 Python 包
  - `nn/` —— neural network 模块（Linear, Conv, Transformer 等）
  - `distributed/` —— 分布式训练（DDP, FSDP, RPC, device mesh）
  - `autograd/` —— automatic differentiation 引擎
  - `cuda/` —— CUDA 绑定与 GPU 支持
  - `fx/` —— 图变换与 compiler IR
  - `_dynamo/` —— TorchDynamo，动态编译器
  - `compiler/` —— TorchInductor 及其他编译后端
- `c10/` —— C++ 核心库（tensor 抽象、日志、工具）
- `aten/` —— A Tensor Library —— 底层 C++/CUDA kernel 实现
- `caffe2/` —— 遗留的 Caffe2（正在合并到 ATen）
- `torchgen/` —— operator 绑定的代码生成
- `functorch/` —— 函数变换（vmap, grad, jvp）
- `test/` —— 庞大的测试套件
- `third_party/` —— 捆绑的依赖（eigen, cpuinfo, sleef 等）
- `docs/` —— 文档源文件

**活跃开发：**
- 近期提交涉及 ROCm 修复、Dynamo operator 支持以及 Native DSL 工作
- 这是一个实时主干检出，并非发布分支

这是目前最大、最复杂的开源 C++/Python 项目之一。构建系统为 CMake + setuptools，项目使用自定义代码生成器（`torchgen`）将 Python 绑定连接到 C++/CUDA kernel。
