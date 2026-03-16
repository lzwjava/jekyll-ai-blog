---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 月之暗面的动态层注意力
translated: true
type: note
---

**问题：** Kimi 的 Attention Residual（来自 Moonshot AI）的全面介绍是什么？

**答案：**

**Attention Residuals (AttnRes)** 是 Moonshot AI（Kimi 背后的团队）在 2026 年 3 月引入的一种新型架构创新。它用 **learned, input-dependent attention mechanism over previous layers** 取代了 transformer 模型中传统的固定 residual connections。

这一变化解决了深度网络在深度上聚合信息时的长期局限性。

### Traditional Residual Connections – The Baseline

在标准的 transformer（post-LN 或 pre-LN）中，每一层像这样更新隐藏状态：

```
x_{l} = x_{l-1} + F_l(x_{l-1})
```

（或在 pre-LN 中：LayerNorm → sub-layer → add）

- Skip connection 总是以权重 **1.0** 添加前一层的输出。
- 这是 **fixed**、**uniform** 和 **input-independent** 的。
- 随着深度增加 → 信号稀释、爆炸/消失幅度、不均匀的梯度流动。

### Core Idea of Attention Residuals

不是盲目添加紧邻的前一层，而是每一层使用 softmax attention 关注 **所有（或许多）前一层**。

简化的数学视图：

设前几层的输出为 {h₁, h₂, ..., h_{l-1}}

对于第 l 层：

- 学习一个 **pseudo-query vector** qₗ（每层一个向量，通常维度较小或共享）
- 计算对先前隐藏状态的 attention scores：  
  α_{l,i} = softmax( qₗ · h_i ) 对于 i = 1…l-1
- 第 l 层的新的输入变为 **weighted sum**：

```
x_l^{pre} = ∑_{i=1}^{l-1} α_{l,i} ⋅ h_i
```

- 然后应用正常的 sub-layer（attention + FFN）→ add & norm 如常。

关键洞见：深度被类比为序列模型中的 **time** → 关注深度而不是固定 recurrence。

### Main Benefits

- **Selective retrieval** — 层可以关注有用的早期表示（绕过稀释的中间层）。
- **Mitigates representational dilution** — 在非常深的模型中，隐藏状态在幅度上更稳定。
- **More uniform gradient flow** — 梯度在层间分布更好（消失更少）。
- **Better scaling behavior** — 尤其在推动模型深度或使用 PreNorm（更易受稀释影响）时有帮助。

### Practical Implementation: Block Attention Residuals

对每一前一层进行 full attention 将在深度上呈二次方（在 100+ 层时非常昂贵）。

Moonshot 使用 **block-wise** 分组：

- 将层分组为 blocks（例如，每 4–8 层）
- 只对 block summaries（或 block outputs）进行 attention
- 保持内存和计算大致线性于深度
- 推理开销很小（~1–2%）

报告的结果显示：

- 预训练期间 ~1.25× 有效计算优势
- 推理几乎无减速
- 在多种设置下下游性能更好

### Integration Example: Kimi Linear

Moonshot 将 Attention Residuals 集成到他们的 **Kimi Linear** 模型中（hybrid linear-attention + MLA 架构，总 48B / 活跃 3B params，在 1.4T tokens 上训练）。

它有助于缓解 PreNorm 问题，并贡献于强大的 scaling behavior。

### Summary – Why It Matters

Attention Residuals 是自原始 “Attention is All You Need” 论文（2017）以来对 **core transformer block** 最干净、最优雅的更新之一。

它完成了 “attention-ification” 转型：

- Tokens 已经关注其他 tokens（self-attention）
- 现在层关注其他层（depth-wise）

许多研究者视其为一种自然演进，却令人惊讶地被忽略了近十年。

有关完整技术细节，请参阅 Moonshot AI 发布的官方论文。

**参考文献：**

- [Moonshot AI Attention Residuals announcement](https://www.linkedin.com/posts/kimi-ai-linkedin_introducing-%F0%9D%91%A8%F0%9D%92%95%F0%9D%92%95%F0%9D%92%86%F0%9D%92%8F%F0%9D%92%95%F0%9D%92%8A%F0%9D%92%90%F0%9D%92%8F-%F0%9D%91%B9%F0%9D%92%86%F0%9D%92%94%F0%9D%92%8A%F0%9D%92%85-activity-7439188677697679360-p-gw)
- [MarkTechPost coverage of Attention Residuals](https://www.marktechpost.com/2026/03/15/moonshot-ai-releases-%F0%9D%91%A8%F0%9D%92%95%F0%9D%92%95%F0%9D%92%86%F0%9D%92%8F%F0%9D%92%95%F0%9D%92%8A%F0%9D%92%90%F0%9D%92%8F-%F0%9D%91%B9%F0%9D%92%86%F0%9D%92%94%F0%9D%92%8A%F0%9D%92%85)
- [GitHub repo with paper (Attention_Residuals.pdf)](https://github.com/MoonshotAI/Attention-Residuals/blob/master/Attention_Residuals.pdf)
- [Reddit discussion on replacing residuals with attention](https://www.reddit.com/r/LocalLLaMA/comments/1rv7ige/residual_connections_havent_changed_for_10_years)