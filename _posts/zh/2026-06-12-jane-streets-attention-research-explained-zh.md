---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 简街注意力研究解析
translated: true
type: note
---

**问题：** Jane Street 如何发布其 Transformer/注意力机制研究，这些研究实际上说了什么？

**回答：**

## 他们如何发布

Jane Street 不像实验室那样在 NeurIPS/ICML 上发表论文——他们通过**技术博客**（blog.janestreet.com）发布，该博客设有专门的机器学习板块。这是一个内容不多但信号很强的渠道：机器学习类别目前只包含少量文章——"Using group theory to explore the space of positional encodings for attention"（2026年4月）、"Deep-Learning the Hardest Go Problem in the World"（2019年）、"Accelerating Self-Play Learning in Go"（2019年）、"L2 Regularization and Batch Norm"（2019年）以及"Does batch size matter?"（2017年）。他们还举办机器学习"夺旗"风格的谜题——最近的一篇文章以"你能逆向工程我们的神经网络吗？"为框架，使用理论可视化工具研究神经网络——此外还有 Signals & Threads 播客、YouTube 上的技术讲座以及 Kaggle 竞赛（他们发布了匿名化的市场数据预测数据集）。其模式是：他们发布*基础性/理论性*的机器学习见解和娱乐性研究，从不发布他们实际产生 Alpha 的模型。该博客在一定程度上是一个招聘渠道。

## 注意力机制文章实际说了什么

这篇旗舰级的注意力机制文章由 Alok Puranik（自2020年起在该公司担任机器学习研究员）撰写。核心问题：注意力机制的查询-键点积不包含任何序列位置信息，因此你需要用位置编码来扰动它——而该文章提出的问题是：有效位置编码的完整空间是什么？

推导过程浓缩如下：

**设定。** 通过使用时间依赖矩阵变换查询和键来编码位置：`q'(t) = F(t)q(t)`，`k'(s) = G(s)k(s)`，因此注意力分数变为 `qᵀ F(t)ᵀG(s) k`。三个公理：

1.  **线性**——F, G 是线性映射（矩阵）
2.  **平移不变性**——`F(t)ᵀG(s)` 仅依赖于 `t−s`（仅相对位置；这使你能够泛化到训练长度之外）
3.  **时间连续性**

**关键步骤。** 定义 `A(t−s) = F(t)ᵀG(s)`。这些公理强制要求 `A(0) = I` 且 `A(t₁)A(t₂) = A(t₁+t₂)`——即矩阵 A(t) 构成一个单参数群，这意味着每个有效编码都具有形式 A(t) = exp(tL)，其中 L 是某个固定的生成矩阵。现在枚举简化为对生成器进行分类：

-   **可对角化的 L，按子空间进行特征值分析：** 实特征值 α > 0 会指数级爆炸（舍弃）；α = 0 恢复 NoPE；α < 0 给出线性注意力变体中常见的指数衰减（并且像 Mamba 这样的门控模型应被视为学习时间推进的步长，而非改变衰减率）。复共轭特征值对给出二维旋转块——你推导出了 RoPE，并带有一个指数衰减因子；这种带阻尼的 RoPE 正是 RetNet 和 Mamba-3 所使用的。
-   **有缺陷的（不可对角化的）L：** Jordan 块产生时间上的**多项式**项——这是一个技术上合法但未被探索的类别，在现有文献中未发现，可能也没有实际应用。一篇附录显示，ALiBi 的 `−m(t−s)` 惩罚实际上可以通过一个带有增强 q/k 的有缺陷的 2×2 幂零生成器来实现。

**核心结论：** 只有少数几类有效的位置编码，并且所有合理的编码——NoPE、衰减、RoPE、带阻尼的 RoPE——都已被使用，因此不存在尚未发现的完美编码。注意他们工作中透露出的框架：他们处理序列模型（市场时间序列），并显式处理连续或不规则采样的时间，而不仅仅是整数 token 索引——这是量化金融在数学上的印记。

## 核心结论的最小实现（带阻尼的 RoPE）

整个分类体系归结为一个参数化——每个二维子空间，一个频率 ω 和一个衰减 α ≤ 0：

```python
import torch

def damped_rope(x, t, omega, alpha):
    """x: (..., T, d), t: (T,), omega/alpha: (d//2,)
    A(t) = exp(tL); L = block-diag of [[alpha, -omega],[omega, alpha]]
    => per-pair: e^{alpha*t} * rotation(omega*t)
    alpha = 0          -> vanilla RoPE
    omega = 0, alpha<0 -> RetNet/linear-attn decay
    both 0             -> NoPE
    """
    x1, x2 = x[..., 0::2], x[..., 1::2]
    theta = t[:, None] * omega[None, :]            # (T, d//2)
    scale = torch.exp(t[:, None] * alpha[None, :]) # 查询的衰减；键使用 -alpha
    cos, sin = torch.cos(theta), torch.sin(theta)
    out = torch.empty_like(x)
    out[..., 0::2] = scale * (x1 * cos - x2 * sin)
    out[..., 1::2] = scale * (x1 * sin + x2 * cos)
    return out
```

在查询上应用 `+alpha·t` 缩放，在键上应用 `−alpha·s` 缩放，这样点积就会得到 `e^{alpha(t−s)}`——仅在相对时间上衰减（需要因果掩码，否则远未来的键会爆炸）。

对于你的 nanoGPT/nanochat 工作，这直接有用：它告诉你 RoPE 对比 ALiBi 对比衰减的设计空间在合理的公理下是*封闭的*，因此编码实验应侧重于频率调度和学习/数据依赖的时间推进（Mamba 风格的门控视角），而不是寻找新颖的函数形式。

**参考文献：**

-   [Using group theory to explore the space of positional encodings for attention — Jane Street Blog](https://blog.janestreet.com/using-group-theory-to-explore-positional-encodings-attention/)
-   [Jane Street Blog — Machine Learning category](https://blog.janestreet.com/machine-learning/)
-   [RetNet paper (exponentially damped rotation)](https://arxiv.org/abs/2307.08621)
-   [GRAPE: Group Representational Positional Encoding (Zhang et al.) — the closely related paper the post acknowledges](https://arxiv.org/abs/2512.07805)