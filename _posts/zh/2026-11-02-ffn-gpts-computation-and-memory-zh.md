---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'FFN: GPT的计算与存储'
translated: true
type: note
---

**问题：** 在 GPT 中，前馈网络（Feed-Forward Network, FFN）的作用是什么？

**回答：**

在 GPT（以及一般 Transformer）中，每一层包含两个子组件：

1. **多头自注意力（Multi-Head Self-Attention）** — 确定*哪些* token 需要关注
2. **前馈网络（Feed-Forward Network, FFN）** — 处理*如何*利用这些信息

---

### FFN 的结构

一个标准的 FFN 仅由两个线性层加上中间的非线性激活构成：

```
FFN(x) = ReLU(x · W₁ + b₁) · W₂ + b₂
```

在 GPT 风格的模型中，隐藏维度通常是 **模型维度的 4 倍**：

- 若模型维度 = 768，则 FFN 隐藏维度 = 3072

---

### FFN 的关键作用

| 角色 | 解释 |
| --- | --- |
| **Non-linearity** | Attention 在很大程度上是线性的；FFN 引入了模型学习复杂函数所需的非线性能力 |
| **Per-token processing** | FFN **独立**作用于每个 token（与混合 token 的 attention 不同）。它单独精炼每个 token 的表示 |
| **Knowledge storage** | 研究（Geva 等人，2021，《Transformer FFN Are Key-Value Memories》）表明 FFN 层起到**事实记忆**的作用 — 在其权重中存储世界知识 |
| **Feature transformation** | 在 attention 聚合上下文后，FFN 将该上下文*转换*为对下一层有用的更高层次特征 |

---

### 直观理解

可以这样理解：

- **Attention** = “四处观察并收集来自其他 token 的相关上下文”
- **FFN** = “现在*思考*你收集到的信息，并更新自己的表示”

FFN 是模型**参数化知识**的主要存储地点——研究表明，事实回忆（例如“Paris is the capital of France”）很大程度上是通过 FFN 权重存储和检索的。

---

### FFN 作为键值记忆

第一层中的每个 FFN 神经元充当一个检测模式的 **“key”**，第二层提供要发射的 **“value”**。这使得 FFN 层类似于所学关联上的软查找表。

```
Key layer (W₁):  检测输入模式
Value layer (W₂): 当模式匹配时发射存储的“知识”
```

---

总之，FFN 是每个 Transformer 块的**计算和记忆引擎**——attention 在 token 之间路由信息，而 FFN 是实际“思考”和知识检索发生的地方。

**参考文献：**

- [Geva et al. (2021) — Transformer Feed-Forward Layers Are Key-Value Memories](https://arxiv.org/abs/2012.14913)
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)
