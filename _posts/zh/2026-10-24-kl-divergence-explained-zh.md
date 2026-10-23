---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KL散度详解
translated: true
type: note
---

问题：什么是 KL divergence？

答案：

**KL divergence**（Kullback–Leibler divergence，即 KL 散度）是衡量一个概率分布与另一个概率分布之间差异程度的度量。它也被称为**relative entropy（相对熵）**。

---

### 定义

对于两个分布 **P**（真实/参考）和 **Q**（近似）：

$$D_{KL}(P \| Q) = \sum_{x} P(x) \log \frac{P(x)}{Q(x)}$$

对于连续分布，求和变为积分。

---

### 关键性质

| 性质 | 说明 |
| --- | --- |
| **非负** | $D_{KL}(P \| Q) \geq 0$ 始终成立 |
| **当且仅当相同时为零** | 只有当 $P = Q$ 时，$D_{KL}(P \| Q) = 0$ |
| **非对称** | $D_{KL}(P \| Q) \neq D_{KL}(Q \| P)$ — 它**不是**一个真正的距离度量 |

---

### 直觉理解

可以把它理解为：使用针对 **Q** 优化的编码来编码来自 **P** 的样本所需的**额外 bits**。如果 Q 对 P 的近似很差，就会浪费更多 bits → KL divergence 更高。

---

### 为什么它很重要

- **Machine Learning**：最小化 $D_{KL}(P \| Q)$ 等价于最大化 log-likelihood —— 用于训练语言模型、VAE 等。
- **Variational Inference**：通过最小化近似后验与真实后验之间的 KL divergence 来近似难以处理的后验分布。
- **Reinforcement Learning from Human Feedback（RLHF）**：KL penalty 项使微调后的模型保持接近基础模型（例如 ChatGPT/Claude 的训练方式）。
- **Information Theory**：量化使用错误分布时造成的信息损失。

---

### 前向 KL 与反向 KL

| | $D_{KL}(P \| Q)$ | $D_{KL}(Q \| P)$ |
| --- | --- | --- |
| 名称 | 前向 KL（Forward KL） | 反向 KL（Reverse KL） |
| 行为 | **Mean-seeking**（Q 扩展以覆盖 P 的所有部分） | **Mode-seeking**（Q 集中于 P 的某个模式） |
| 用于 | MLE、扩散模型 | Variational inference |

---

### 简单示例

假设 P = [0.9, 0.1]，Q = [0.5, 0.5]：

$$D_{KL}(P \| Q) = 0.9\log\frac{0.9}{0.5} + 0.1\log\frac{0.1}{0.5} \approx 0.531 \text{ nats}$$

Q 是一个均匀分布——对于偏斜的 P 来说，它是一个很差的模型，因此 KL 明显大于 0。

---

参考：

- [KL Divergence — Wikipedia](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)
- [KL Divergence for Machine Learning — Towards Data Science](https://towardsdatascience.com/light-on-math-machine-learning-intuitive-guide-to-understanding-kl-divergence-2b382ca2b2a8)
- [Understanding KL Divergence (Lilian Weng's Blog)](https://lilianweng.github.io/posts/2017-08-20-flow-based-deep-generative-models/)
