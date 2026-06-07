---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA TensorRT-LLM 概述
translated: true
type: note
---

问：什么是 ensorRT-LLM？

答：假设你指的是 **TensorRT-LLM**（修正了拼写错误），这是一个由 NVIDIA 开发的开源库，专门用于在 NVIDIA GPU 上优化、加速并最大化大型语言模型（LLM）推理的性能。

无论是运行在本地桌面 GPU、边缘设备还是大规模数据中心集群上，TensorRT-LLM 都能编译神经网络图并结合软硬件协同设计，实现高效的 token 生成。

### 关键特性与优化

TensorRT-LLM 作为一个工具包，位于深度学习框架（如 PyTorch）和底层硬件之间。它使用多种先进技术加速文本生成：

* **In-Flight Batching**：无需等待整个请求批次完成再开始新批次，而是动态排队并实时处理新请求，大幅提升 GPU 利用率。
* **Paged Attention**：受操作系统虚拟内存启发，优化键值缓存（KV cache）内存管理，使系统能处理更长的上下文窗口，并在不耗尽显存的情况下支持更多并发用户。
* **高级量化**：支持低精度格式，如 **FP8**（Hopper H100 及更新架构）和 **FP4/NVFP4**（Blackwell B200 架构），大幅降低内存消耗，将吞吐量提升一倍且对精度影响极小。
* **多 GPU / 多节点并行**：开箱支持张量并行、流水线并行以及专家并行（用于 DeepSeek 等混合专家模型），将大模型拆分到多个芯片上。
* **推测解码**：通过运行一个较小的草稿模型预先预测 token，再由较大的目标模型同时验证这些 token，从而加速文本生成。

### 架构与组件

TensorRT-LLM 分为两个主要部分：

1. **模型定义（Python API）**：采用 PyTorch 原生语法，允许开发者定义、自定义并编译流行的架构（如 Llama 3/4、DeepSeek、Qwen、Gemma），生成高度优化的 TensorRT 引擎图。
2. **C++ 运行时**：高度优化的执行引擎，负责编排实际部署、token 采样和底层内存处理，常被封装到 NVIDIA Triton 推理服务器或兼容 OpenAI 的端点服务器等生产工具中。

参考：

* [NVIDIA TensorRT-LLM 开发者概览](https://developer.nvidia.com/tensorrt-llm)
* [NVIDIA TensorRT-LLM 文档](https://docs.nvidia.com/tensorrt-llm/index.html)
* [TensorRT-LLM GitHub 仓库](https://github.com/NVIDIA/TensorRT-LLM)
