---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 理解 Transformer 中的自注意力机制
translated: true
type: note
---

Question: 视频是如何评论并扩充对 Self-Attention Mechanism 的解释的？

Answer: 

该视频投入了大量篇幅详细讲解 Self-Attention 机制，特别是从 14:06 时间点（“Attention is Cheap!”）开始，并持续到 37:52（“Attention: a weighted average”）等章节。

### 视频中的关键评论与扩充：

- **动机与优势**：讲者（Ashish Vaswani 和 Anna Huang）强调，Seq2Seq 模型中的传统 Attention 成本很高，因为它是作用在 RNN 隐藏状态上的串行操作。相比之下，Self-Attention 是“廉价”的，因为它允许输入序列中所有位置之间进行直接、并行的交互。与 RNN（按顺序处理，限制了并行性）或 Convolutions（需要堆叠多层才能获得长距离依赖）不同，Self-Attention 为依赖关系提供了常数长度的路径，并实现了全序列的并行化。

- **核心机制**：Self-Attention 被描述为计算值的 **weighted average**（加权平均），其中的权重由输入位置本身的 Query 和 Key 之间的兼容性（相似度）决定。每个位置都以基于内容的方式关注其他所有位置，而不依赖于距离。

- **通过矩阵运算实现效率**：计算过程非常高效，因为它使用了矩阵乘法：Query (Q)、Key (K) 和 Value (V) 从输入 embedding 中投影出来，然后 Attention 分数计算为 Q · K^T（点积），经过 Scaled、Softmax，最后乘以 V。这使得在 GPU 上并行处理整个序列成为可能。

- **Multi-Head Attention**：他们通过引入 Multi-Head Self-Attention（约 16:35 时间点）扩充了这一解释，即多个独立的 Attention Head 并行运行，每个 Head 学习关系的不同维度（例如，一个 Head 关注“谁”，另一个 Head 关注“做了什么”）。最后将输出拼接并进行投影。

- **Positional Encodings**：为了保留序列顺序（因为 Self-Attention 具有置换不变性），他们使用了添加的 Positional Encodings。原始 Transformer 使用固定的正弦编码，但讲座中提到了替代方案，如 Relative Position Representations（在 40:08 和 45:12 左右讨论），它们提供了平移等变性（Translational Equivariance）——这是一种对序列很有利的归纳偏置（Inductive Bias）。

- **更广泛的背景**：Attention 被框架化为一种对输入计算加权平均的通用方法，不仅可以扩展到文本，还可以扩展到图像（Non-local means）和音乐（通过 Relative Attention 更好地捕获主题句/Motifs）。

这些解释紧贴《Attention Is All You Need》论文，但包含了现场演示、示例（如 Attention 可视化）以及在其他领域生成模型中的扩展。

References:  

- [Lecture Video](https://www.youtube.com/watch?v=5vcj8kSwBCY)  
- [Lecture Slides (2019 Lecture 14 - Transformers)](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1194/slides/cs224n-2019-lecture14-transformers.pdf)  
- [Original Transformer Paper: Attention Is All You Need](https://arxiv.org/abs/1706.03762)