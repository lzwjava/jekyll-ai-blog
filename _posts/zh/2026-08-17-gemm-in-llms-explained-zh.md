---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM中的GEMM详解
translated: true
type: note
---

问题：在LLM（大语言模型）的上下文中，什么是GEMM？

答案：GEMM代表**通用矩阵乘法**（也写作GEMM：`C = αAB + βC`），是BLAS（基本线性代数子程序）库标准中的核心例程。

在LLM中，GEMM之所以重要，原因如下：

- **核心计算**：Transformer中的几乎所有重计算——线性层、注意力投影（Q/K/V）、前馈网络——都可以归结为矩阵乘法，即GEMM操作。
- **性能瓶颈**：由于GEMM占据了绝大部分计算量（FLOPs），它们在GPU/TPU上的运行效率在很大程度上决定了训练和推理的速度。cuBLAS、cuBLASLt和cuDNN等库提供了高度优化的GEMM内核。
- **批量GEMM**：LLM工作负载通常使用批量或跨步GEMM（同时将许多小矩阵相乘），尤其是在跨头和批次元素的注意力计算中。
- **精度变体**：你会看到诸如FP16 GEMM、INT8 GEMM或FP8 GEMM等术语——这些指的是所使用的数值精度，即在速度/内存与精度之间的权衡。
- **优化目标**：内核融合、张量核心（在NVIDIA GPU上）和量化等技术都旨在使GEMM操作更快或更便宜，因为它们是训练和推理中的主要成本驱动因素。

简而言之，当人们讨论LLM效率时——“每次前向传播有多少个GEMM”“GEMM受限与内存受限”或“张量核心利用率”——他们实际上是在讨论优化这些构成模型实际计算主体的矩阵乘法操作。