---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Softmax注意力机制详解
translated: true
type: note
---

**问题：**什么是 Softmax Attention？

**答案：**

Softmax Attention 是 Transformer 模型使用的核心注意力机制，由 2017 年里程碑式论文 *"Attention Is All You Need"* 提出。它允许模型在生成输出时动态关注输入序列的相关部分。

---

## 核心公式

给定三个从输入中得到的矩阵——**Query (Q)**、**Key (K)** 和 **Value (V)**——注意力输出为：

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

---

## 逐步分解

**1. 计算原始分数（点积）**
每个查询向量通过点积与所有键向量进行比较：

$$\text{score}_{ij} = Q_i \cdot K_j$$

这衡量了位置 *j* 对位置 *i* 的“相关性”。

**2. 缩放**
分数除以 $\sqrt{d_k}$（键向量的维度）。否则，较大的点积会将 softmax 推入梯度接近零的区域，导致训练不稳定。

**3. 应用 Softmax**
将原始分数转换为位置上的概率分布：

$$\alpha_{ij} = \frac{e^{\text{score}_{ij}}}{\sum_k e^{\text{score}_{ik}}}$$

每一行现在总和为 1——这就是“注意力权重”向量。

**4. 值的加权求和**
使用注意力权重对值向量进行加权组合：

$$\text{output}_i = \sum_j \alpha_{ij} \cdot V_j$$

---

## 为什么是“Softmax”？

Softmax 函数使注意力变得“软”（可微、对梯度友好），而不是“硬”（argmax、不可微）。它为所有位置分配非零权重，让模型同时混合来自多个位置的信息。

---

## 关键特性

| 特性 | 详情 |
| --- | --- |
| **二次复杂度** | 序列长度上为 $O(n^2)$ —— 主要瓶颈 |
| **置换等变性** | 没有固有的顺序概念（位置编码单独添加） |
| **多头** | 并行运行 $h$ 个注意力头，然后拼接 |
| **掩码** | 对于自回归模型，使用因果掩码（在 softmax 之前将未来位置设为 $-\infty$） |

---

## 局限性（以及为何在探索替代方案）

- 序列长度 $n$ 上的**二次内存/计算**使得长上下文代价高昂
- 这推动了替代方案的出现，例如 **Linear Attention**、**Flash Attention**（一种高效实现）、**GQA**（Grouped Query Attention）和 **MLA**（DeepSeek 使用的 Multi-head Latent Attention）

---

**参考：**

- [Attention Is All You Need — Vaswani et al., 2017](https://arxiv.org/abs/1706.03762)
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [Flash Attention — Efficient Exact Attention](https://arxiv.org/abs/2205.14135)
- [Lilian Weng — Attention? Attention!](https://lilianweng.github.io/posts/2018-06-24-attention/)
