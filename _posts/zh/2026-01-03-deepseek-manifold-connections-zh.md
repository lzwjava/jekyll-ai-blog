---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DeepSeek流形超连接简介
translated: true
type: note
---

Question: What is a comprehensive introduction to mHC (Manifold Hyper Connection) from DeepSeek, recently?

Answer:

### Overview of mHC

Manifold-Constrained Hyper-Connections (mHC) 是 DeepSeek-AI 在 2025 年 12 月 31 日发表的研究论文 (arXiv:2512.24880) 中提出的一种新型神经网络架构创新。它代表了 Large Language Models (LLMs) 及其他深度神经网络中 Residual Connection 设计的重大进展，旨在提高模型容量扩展时的训练稳定性、Scalability 和效率。

mHC 基于近期提出的 **Hyper-Connections (HC)** 范式。HC 通过将 Residual Stream 拓宽为多个并行“通道”（使用 Expansion Factor，例如 n=4）并在这些通道之间引入可学习的 Mixing Matrices，扩展了传统的 Residual Connection。与标准单流 Residual Connection（如 ResNet 或 Transformers 中所见）相比，这种多样化允许更丰富的信息流和更好的性能。

然而，无约束的 HC 会引入关键问题：

- **Identity Mapping 属性丢失**：标准 Residual 能够保留一条“恒等”路径，确保信号和梯度在深层网络中稳定传播。HC 的混合机制破坏了这一点，导致信号爆炸/消失以及训练不稳定（例如梯度范数剧烈飙升）。
- **Scalability 限制**：模型在大规模扩展时容易出现发散（Divergence）。
- **效率开销**：在分布式训练中增加了内存访问和通信成本。

mHC 通过**将 Residual Mixing Matrices 约束在特定的数学流形（Manifold）上**——具体为双双随机矩阵（Doubly Stochastic Matrices）的 Birkhoff Polytope——来解决这些问题。这是通过使用 Sinkhorn-Knopp Algorithm 进行投影实现的。

### Key Mechanisms in mHC

- **Manifold Projection**：在计算动态混合后，矩阵被投影为双双随机矩阵。这恢复了保守的（类似于凸组合的）混合，在保留 HC 性能增益的同时，维持了跨层的类恒等稳定性。
- **Infrastructure Optimizations**：为了将开销保持在较低水平（约 6-7% 的训练时间增加）：
  - Kernel Fusion 和混合精度实现。
  - 与 Pipeline 阶段对齐的 Recomputation 策略。
  - 通信与计算的重叠（例如通过 DualPipe 扩展）。
- **Compatibility**：mHC 是 Transformer 架构型模型的即插即用增强方案，已在类似于 DeepSeek-V3 的 MoE 架构上进行了测试。

### Empirical Results

DeepSeek 研究人员在 3B、9B 和 27B 参数规模的模型上测试了 mHC：

- **Stability**：消除了 HC 的训练发散问题；梯度范数保持在接近基线 Residual 的水平。
- **Performance**：在 Benchmark 测试中（如 BBH、DROP、GSM8K、MMLU 的更高得分）优于标准 Residual 和无约束 HC。
- **Scalability**：随着模型尺寸和训练 Token 数量的增加，表现出更好的 Loss 曲线和下游任务收益。
- **Efficiency**：在 Expansion Factor 为 4 的情况下仅有约 6.7% 的开销，使其在大规模训练中具有实用价值。

### Significance

mHC 为 LLMs 引入了一个新的“缩放旋钮”：在不通过单纯增加模型宽度/深度带来不稳定性或全额计算成本的情况下，富化 Residual Topology（更宽、混合的流）。它强调了架构中的拓扑设计，可能会影响未来的 Foundational Models。作为 HC 的灵活扩展，它支持具有卓越稳定性的更深/更宽的模型，对于资源受限的训练（例如在硬件出口限制下）特别有价值。

这项由 DeepSeek 创始人梁文锋共同署名的工作，标志着该公司继 DeepSeek-V3 和 R1 等突破后的持续创新。它可能成为即将推出的模型（可能是 V4 或 R2 变体）的基础。

References:

- [arXiv: mHC: Manifold-Constrained Hyper-Connections](https://arxiv.org/abs/2512.24880)
- [Hugging Face Paper Page](https://huggingface.co/papers/2512.24880)
- [South China Morning Post Article](https://www.scmp.com/tech/big-tech/article/3338427/deepseek-kicks-2026-paper-signalling-push-train-bigger-models-less)
- [SiliconANGLE Coverage](https://siliconangle.com/2026/01/01/deepseek-develops-mhc-ai-architecture-boost-model-performance/)
