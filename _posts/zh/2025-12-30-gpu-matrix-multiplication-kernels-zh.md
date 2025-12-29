---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 高性能 GPU 矩阵乘法算子
translated: true
type: note
---

Question: What does the content of the blog post at https://www.aleksagordic.com/blog/matmul say?

Answer:

这篇标题为 **"Inside NVIDIA GPUs: Anatomy of high performance matmul kernels - From GPU architecture and PTX/SASS to warp-tiling and deep asynchronous tensor core pipelines"** 的博客文章由 Aleksa Gordić 撰写，发布于 2025 年 9 月 29 日。

这是一篇技术深度极高的文章，深入探讨了如何在 NVIDIA GPUs 上实现 state-of-the-art (SOTA) 的 matrix multiplication (matmul) kernel，主要针对 Hopper architecture（例如 H100 GPU）。文章强调 matmul 是 transformers 中最关键的操作（用于 linear layers、attention projections 等），在 training 和 inference 过程中消耗了大部分 FLOPs，因此 GPU 优化具有极高的价值。

### 结构与主要章节

该文章分为四个主要部分：

1. **NVIDIA GPU Architecture Fundamentals**
    
    - 详细解释了 memory hierarchy：Global Memory (HBM/GMEM)、L2 cache、L1 cache/shared memory (SMEM) 以及 registers。  
    - 计算单元：Tensor Cores、CUDA cores、load/store units 以及 warp schedulers。  
    - 相关概念如 parallelism vs. concurrency、"speed-of-light" (SoL) 峰值性能计算、power throttling 对 clock speeds 的影响，以及 Hopper 中的 Tensor Memory Accelerator (TMA)。

2. **GPU Assembly: PTX and SASS**
    
    - 介绍了从 CUDA C++ 到 PTX (virtual assembly) 再到 SASS (native ISA) 的编译管线。  
    - 展示了如何检查和影响底层代码生成以获得更好的性能。

3. **Synchronous Warp-Tiling Matmul Kernel**
    
    - 引入 warp-tiling 技术，通过减少 global memory 流量来提升 arithmetic intensity。  
    - 解释了 tiling 策略、将矩阵 A 和 B 加载到 shared memory 中（为了 vectorized loads 进行转置）、通过 swizzling 处理 bank conflicts，以及在 registers 中计算中间结果。  
    - 包含了 naive vs. tiled kernels 的代码片段和性能分析。

4. **Asynchronous SOTA Matmul on Hopper**
    
    - 利用 Hopper 特有的特性：用于 Tensor Cores 的异步 `wgmma.mma_async` 指令，用于异步 GMEM-to-SMEM 传输的 TMA，以及 pipelining。  
    - 描述了带有 circular buffers 的 producer-consumer pipelines、warp-group 协作（128 threads）、消除 bank conflicts 的 swizzling、persistent kernels 以及高级调度（例如用于更好 cache locality 的 Hilbert curves）。  
    - 实现了巨大的性能提升（例如从 ~32 TFLOP/s 提升到 ~317 TFLOP/s）。

### 关键技术见解

- **为什么要优化 Matmul？** 它是 embarrassingly parallel 的，并且主导了 transformer 的计算。
- **性能瓶颈：** Memory-bound vs. compute-bound (roofline model)、bank conflicts、uncoalesced accesses、occupancy 以及 wave/tile quantization。
- **重点优化的技术：**  
    - Vectorized/coalesced loads。  
    - Shared memory tiling 和 outer-product formulation。  
    - 异步操作以实现计算与内存传输的 overlap。  
    - SMEM 中的 Swizzling 和 multicasting。  
    - Cluster-level 协调和 persistent blocks。

文章包含大量图表（如 memory hierarchies、bank conflict 示意图、pipeline stages）、带注释的代码片段（CUDA、PTX、SASS）、数学推导（如峰值 FLOPs 公式）以及来自 Nsight Compute 等工具的性能指标。

### 结论/总结

高性能 matmul 需要对 GPU 硬件和底层编程有深入的了解。Pre-Hopper GPUs 依赖 warp-tiling 来获得接近 SOTA 的结果，但 Hopper 的异步特性实现了数量级的提升。作者强调“计算机是可以被理解的”，并预告了未来关于 Blackwell GPUs、multi-GPU 设置等内容的文章。

这篇文章面向旨在实现峰值性能的高级 CUDA 程序员和 GPU kernel 开发者。

References:  

- [Original blog post](https://www.aleksagordic.com/blog/matmul)