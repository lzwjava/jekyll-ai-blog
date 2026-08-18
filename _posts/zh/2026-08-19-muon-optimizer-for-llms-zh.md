---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型μ子优化器
translated: true
type: note
---

问题：在大型语言模型（LLM）中，Muon 优化器是什么？

答案：

**Muon 优化器** 是一种近期开发的基于梯度的优化器，旨在提升大型语言模型的训练效率和性能。以下是详细说明：

**核心思想**

Muon 代表 **MomentUm Orthogonalized by Newton-schulz**（通过牛顿-舒尔茨迭代正交化的动量）。它在将动量缓冲区用作梯度更新之前，先对其应用正交化步骤——这意味着权重更新被近似正交化，有助于保持稳定、条件良好的梯度步长。

**工作原理**

1. 计算动量（类似带动量的标准 SGD）
2. 应用 **牛顿-舒尔茨迭代** 对动量矩阵进行正交化
3. 将正交化后的更新作为有效梯度步长

这在数学上等价于在**谱范数**（而非 L2 范数）下的最速下降，使其能够更好地感知曲率，而无需计算或存储完整的 Hessian 矩阵。

**为何对 LLM 重要**

- **在某些场景下优于 AdamW**——多项实验表明，在相同计算预算下，Muon 能用更少的 token 或更低的损失达到或超越 AdamW 的性能
- **更新更稳定**——正交化更新避免了冗余或共线的梯度步长
- **节省内存**——无需像 Adam 那样存储二阶矩估计

**局限性**

- 最适合**矩阵形状的参数**（注意力/MLP 权重）；偏置和嵌入层通常仍需使用 Adam
- 相对较新——在极大规模训练中尚未充分验证
- 超参数敏感性仍在研究中

**谁在使用**

该优化器因 Keller Jordan 的工作而受到关注，并被多个实验室的团队探索作为 AdamW 的潜在替代方案，特别是在中等规模的 LLM 训练中。

参考文献：

- [Muon: An optimizer for hidden layers in neural networks (Keller Jordan)](https://kellerjordan.github.io/posts/muon/)
- [Muon Optimizer – GitHub](https://github.com/KellerJordan/Muon)
- [牛顿-舒尔茨迭代 – Wikipedia](https://en.wikipedia.org/wiki/Polar_decomposition#Algorithms)
