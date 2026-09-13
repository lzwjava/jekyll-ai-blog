---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AdaGrad：自适应次梯度方法论文
translated: true
type: note
---

**问题：** 来自 https://jmlr.org/papers/volume12/duchi11a/duchi11a.pdf 的论文是什么？

**答案：** 这是原始的 **AdaGrad** 论文——机器学习优化领域最具影响力的论文之一。该论文于2011年发表在《机器学习研究期刊》（Journal of Machine Learning Research）上，提出了**自适应次梯度**方法，即广为人知的 **AdaGrad**（自适应梯度算法）。

**作者：** John Duchi（加州大学伯克利分校）、Elad Hazan（以色列理工学院）和 Yoram Singer（谷歌）。

**核心思想：**
标准梯度下降对每个参数使用相同的学习率。而 AdaGrad 则根据每个特征的历史梯度幅度，*为每个特征*自适应地调整学习率：

- **频繁更新的特征**获得*更小*的学习率
- **较少更新的特征**获得*更大*的学习率

这对于稀疏、高维数据（例如 NLP 任务）尤为强大，其中某些特征出现频率低但携带很强的预测信号——即作者所描述的“大海捞针”问题。

**主要贡献：**

1. **对角 AdaGrad**——将每个坐标的学习率缩放为该坐标过去梯度平方和的反平方根。在高维空间中高效且实用。
2. **全矩阵 AdaGrad**——使用梯度的完整外积矩阵以获得更丰富的几何结构，但计算成本更高。
3. **理论遗憾界**——证明该算法能够实现可证明的、良好的遗憾保证，与事后选择的最佳固定近端函数相竞争。
4. **实用算法**——推导出适用于常见正则化项（ℓ₁、ℓ₂、ℓ∞）和域约束的具体更新规则。

**为何重要：** AdaGrad 是现代自适应优化器的基础性步骤。它直接启发了 **RMSProp**、**Adam** 和 **AMSGrad**，这些优化器如今广泛用于训练深度神经网络。

**参考文献：**
- [AdaGrad 论文 — JMLR](https://jmlr.org/papers/volume12/duchi11a/duchi11a.pdf)