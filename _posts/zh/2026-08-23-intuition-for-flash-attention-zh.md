---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flash Attention 的直觉
translated: true
type: note
---

**问题：Flash Attention 的直觉是什么？**

**答案：** Flash Attention 是一种算法，通过改变*如何*计算注意力机制——而不是*计算什么*——来显著加速 Transformer 中的注意力并节省内存。其核心见解如下：

**标准注意力存在内存瓶颈。** 朴素方法会计算完整的 N×N 注意力矩阵（其中 N 是序列长度），将其写入 GPU 内存（HBM——慢速、远距离），然后为了 softmax 读回，再为了乘以值而再次读取。这种反复往返于慢速内存的过程才是真正的瓶颈。

**Flash Attention 停留在快速内存（SRAM）中。** 它不会一次性计算整个矩阵，而是将计算分成适合 GPU 快速片上 SRAM（缓存）的小块。它处理一个块，维护一个运行中的 softmax 修正因子，并将所有步骤融合在一起——永远不会将大的 N×N 矩阵写入 HBM。

关键技巧是**在线 softmax 修正**：softmax 需要知道所有分数才能进行归一化，但 Flash Attention 使用一个运行中的最大值和一个运行中的总和，这些值会逐块更新。最终结果在数学上与标准注意力完全相同——这是一种纯粹的实现优化。

**一句话总结心智模型：** 标准注意力就像做作业时，把每一步中间计算都写在房间后面的一块白板上（HBM），每步都要来回走；Flash Attention 则在书桌上的草稿纸（SRAM）上完成所有工作，只在最后走到后面一次。

需要内化的关键点：
- N×N 矩阵从未在慢速内存中具体化——这是核心优势
- **在线 softmax 技巧**使得分块成为可能：你不需要在归一化之前看到所有分数，只需跟踪一个运行中的修正因子
- Flash Attention 2 和 3 通过更好的注意力头和序列位置的并行性扩展了这一点