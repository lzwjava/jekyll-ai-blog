---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: NVIDIA GPU 中的关键计算单元
translated: true
type: note
---

Question: 请对 NVIDIA GPU 中的计算单元进行全面介绍：Tensor Cores、CUDA cores、load/store units 以及 warp schedulers。

Answer:

NVIDIA GPU 专为大规模并行处理设计，特别是在图形处理、科学计算和 AI 工作负载方面。其核心构建模块是 **Streaming Multiprocessor (SM)**，其中包含负责执行指令的各种计算单元。这些单元在 SIMT (Single Instruction, Multiple Thread) 模型下协同工作，在该模型中，线程被分组为包含 32 个线程的 **warps**，并同时执行相同的指令。

### CUDA Cores
CUDA cores（也称为 Streaming Processors 或 SPs）是 SM 中的通用算术单元。它们处理标量操作，包括：
- 浮点运算（FP32、FP16 等）
- 整数运算（INT32）
- 基础逻辑和控制指令

每个 CUDA core 每个时钟周期执行一个线程的一个操作（或在某些情况下跨周期共享）。现代 SM（例如 Ampere 或更晚的架构）通常每个 SM 拥有 64–128 个 CUDA cores，分为 FP32 和 INT32 路径。它们用途广泛，用于大多数非专门化的计算，如游戏中的通用数学计算、模拟或非矩阵 AI 操作。

CUDA cores 遵循 SIMT 模型：一个 warp 中的所有 32 个线程执行相同的指令，但处理不同的数据。如果线程发生分歧（例如通过分支），不活跃的线程会被屏蔽（masked off），从而降低效率。

### Tensor Cores
Tensor Cores 于 Volta 架构（2017年）引入，并在后续代际（Turing、Ampere、Hopper、Blackwell）中不断改进，是专门用于矩阵乘累加 (MMA) 操作的加速器，这类操作是深度学习（如神经网络训练和推理）的基础。

核心特性：
- 它们通过在单个周期内处理小矩阵碎片（例如 4x4 或更大的 tiles），执行密集矩阵运算的速度远快于 CUDA cores。
- 支持混合精度：例如，FP16 或 BF16 输入与 FP32 累加，以获得更高的准确度。
- 在后续架构中，它们支持更多格式，如 INT8、TF32 或 FP8，以实现更高的吞吐量。

单个 Tensor Core 每个周期可以提供数百到数千次操作，在矩阵工作负载方面远超 CUDA cores。它们通过 warp 级原语（如 CUDA 中的 WMMA 或 MMA 指令）进行编程。Tensor Cores 在 AI 性能中占据主导地位，但仅限于特定操作；通用任务则回退到 CUDA cores。

### Load/Store Units (LD/ST)
Load/Store units 处理内存操作：将数据从内存加载到寄存器中，并将结果存回。它们对于访问 global memory、shared memory、constant memory 等至关重要。

特征：
- 通常每个 SM 有 16–32 个 LD/ST units（随架构而异）。
- 每个单元为一个或多个线程处理内存请求（在合并访问中通常是 half-warp 或按线程处理）。
- 它们计算地址，处理合并（coalescing，即合并来自 warp 中线程的请求以减少内存事务），并管理与缓存（L1 和 L2）的交互。

高效使用需要合并访问（线程访问连续内存），以最大化带宽并避免串行化。LD/ST units 是 memory-bound kernels 中常见的瓶颈。

### Warp Schedulers
Warp schedulers 管理 SM 内 warps 的执行。它们对于隐藏延迟和最大化吞吐量至关重要。

角色与运作：
- 每个 SM 拥有多个 warp schedulers（在 Turing、Ampere、Hopper 等现代架构中通常为 4 个）。
- 每个调度器选择符合条件的 warps（那些指令已就绪、未阻塞在内存或依赖关系上的 warp），并在每个周期向相应的执行单元（CUDA cores、Tensor Cores、LD/ST 等）分派一条指令。
- 当一个 warp 发生阻塞（例如等待内存）时，调度器会切换到另一个就绪的 warp——这种“延迟隐藏”使 SM 保持繁忙。

调度策略（如轮询 round-robin 或基于优先级）确保了公平性和利用率。高 warp 占用率（每个 SM 驻留多个 warps）通过提供更多调度选项来提高性能。

### 它们在 SM 中如何交互
一个典型的现代 SM（如 Ampere）被划分为 4 个处理块，每个块包含：
- 一部分 CUDA cores
- Tensor Cores
- LD/ST units
- 一个 warp scheduler 和 dispatch unit

来自选中 warps 的指令被分派到相关单元。这种设计允许不同指令类型并发执行，并实现高效的资源利用。

总结来说，CUDA cores 提供通用计算，Tensor Cores 加速 AI 特有的矩阵运算，LD/ST units 管理内存流量，而 warp schedulers 编排一切以隐藏延迟并实现高并行性。了解这些单元有助于针对特定工作负载优化 CUDA kernels。

References:

- [NVIDIA Volta Architecture Whitepaper](https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf)
- [NVIDIA Turing Architecture In-Depth](https://developer.nvidia.com/blog/nvidia-turing-architecture-in-depth/)
- [Inside NVIDIA GPUs: Anatomy of high performance matmul kernels](https://www.aleksagordic.com/blog/matmul)
- [A Beginner's Guide to NVIDIA GPUs in 2025](https://www.cudocompute.com/blog/a-beginners-guide-to-nvidia-gpus)
- [CUDA Cores vs Tensor Cores](https://acecloud.ai/blog/cuda-cores-vs-tensor-cores/)
