---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA GPU SM 解析
translated: true
type: note
---

Question: 在NVIDIA GPU中，“SM”代表什么？

Answer:

**SM = Streaming Multiprocessor（流式多处理器）。**

它是NVIDIA GPU的基本计算单元。一个GPU本质上由多个SM组成（例如，H100有132个SM，RTX 4070有46个SM）。每个SM包含：

- **CUDA核心**（FP32/INT32 ALU）—— 标量运算通道
- **张量核心** —— 矩阵乘累加单元（深度学习GEMM的主力）
- **线程束调度器** —— 将线程束（32个线程为一组）分配到执行单元
- **寄存器文件** —— 每个SM通常有64K个32位寄存器
- **共享内存 / L1缓存** —— 快速片上暂存器（可配置分割，如Hopper上为228 KB）
- **加载/存储单元、SFU**（特殊函数单元，用于超越函数）

执行模型直接映射到这一层次结构：当你启动一个CUDA内核时，**线程块**被分配到SM上。线程块在其生命周期内驻留在单个SM上，SM以**32线程的线程束**为单位执行线程。占用率——你在性能分析中会频繁看到的数值——是活跃线程束与SM最大线程束数的比值，受寄存器和共享内存压力的限制。

因此实际中：更多的SM + 更高频率 + 每个SM更优的张量核心 = 更高的吞吐量。当你调优内核（分块大小、共享内存使用量、寄存器数量）时，实际上是在调优每个SM内的工作打包效率。

参考资料：

- [NVIDIA CUDA C Programming Guide — Hardware Implementation](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#hardware-implementation)
- [NVIDIA H100 Architecture Whitepaper](https://resources.nvidia.com/en-us-tensor-core)
