---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 雅各布·斯坦哈特简介
translated: true
type: note
---

## 问题：介绍加州大学伯克利分校的 Jacob Steinhardt

### 回答：

![Image](https://images.openai.com/static-rsc-4/DW20xZas1fXU_6qkC6l8TV7hoBy6NZC8YNt-7TYE4a8-GecojD8BaXhZs5oxK-jgfb_oaT7G2JfwnBj1rGCX2hrO8NyNLjETpqMqIY8q_c-4ln1JPR3L5T9_goG8GFwHlyyJALWH8VXWawliY-MmTplKHI6Jefp5-iegcw8UZ73uNZNTrUjFnELc5E9Ra5tI?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ueugMlAfM3LiRdh0hDoo0hJDc8-3RWnSBn4bi3cahO2zf-j2LvX6-eQmiBgn3tEbeS6BYWmb9hdkzp37kGW8XdszzwUmQzQ7W5OZSFj6Qci5kePKmWSlUMfwrPLBp9GCOmDoMBg-FUpu_FTPhj0mS-mXevSbb9nCxvBqqhriLEY0TZEF1OhV9AFJPbX0HhEZ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dEJDet9jNI7Zd8bwbviC9xyTr41rUpZO9BrgiA24kTRZHChBw0bAvaeCXuGcfYqCpyt8RMoMQrs1ha4IV-kvgYjwizop-rz2AWZorJgdBAiflEujE4TIZ91ZEaVS66hrgqBkYe0n9vCorH5GVOTx68nHo49LOl4m-BFT3JYlJG_o9EsqBh8imeOVAdx3MF8Y?purpose=fullsize)

Jacob Steinhardt 是**加州大学伯克利分校统计系 + EECS 教授**，研究方向为**mechanistic interpretability、LLMs、AI alignment/safety、robustness 和 reward hacking**。如果你正在研究前沿模型内部究竟如何计算，他当前的研究尤其相关。（[Department of Statistics][1]）

理解他学术生涯的一个有用线索是：

> **theory → robust ML → AI safety → understanding the internals of frontier LLMs**

### 背景

* **麻省理工学院数学学士 — 2012**
* **斯坦福大学计算机科学博士 — 2018**，导师为 **Percy Liang**
* 2019 年加入**加州大学伯克利分校统计系**
* 同时隶属于 **EECS、BAIR 和 CLIMB**。（[Simons Institute][2]）

在伯克利学术生涯开始之前/前后，他还曾在 **OpenAI** 和 **Open Philanthropy Project** 工作过。

### 他的研究演化尤其有趣

早期工作更偏理论：

```text
probability / statistics
        ↓
robust statistics
        ↓
robust ML + adversarial/data poisoning
        ↓
AI alignment / reward hacking
        ↓
LLM behavior
        ↓
mechanistic interpretability
```

例如，他 2017 年与 Pang Wei Koh 和 Percy Liang 合作的论文是：

**“Certified Defenses for Data Poisoning Attacks”**

其基本问题是：*当攻击者操纵训练数据时，我们能否在数学上保证 ML 模型仍然可靠？*（[Jacob Steinhardt][3]）

这最终自然地联系到今天的安全对齐问题：**我们如何知道一个 ML 系统实际上在优化什么，当我们的目标函数不完美时会发生什么？**

---

## 他当前的工作可能是你最关心的部分

Steinhardt 在伯克利的个人主页现在列出的研究方向是：

> **mechanistic interpretability、large language models、alignment and safety**。（[Department of Statistics][1]）

他的实验室正在研究如下内容：

### 1. LLM 如何表示概念

例如：

**语言模型如何在上下文中绑定实体？**

假设：

```text
Alice went to the kitchen.
Bob went to the library.

Alice picked up the apple.
```

Transformer 如何在内部追踪 **Alice → kitchen → apple** 之间的关系？

这比简单衡量模型是否回答正确要深入得多。

目标是理解**内部计算**。

---

### 2. 神经元/电路如何实现计算

他团队近期的工作包括：

**“Language Model Circuits Are Sparse in the Neuron Basis”**

以及

**“ADAG: Automatically Describing Attribution Graphs.”**（[Jacob Steinhardt][3]）

这与现代 mechanistic interpretability 方向非常接近：

```text
input tokens
     ↓
embedding
     ↓
attention / MLP layers
     ↓
hidden activations
     ↓
specific neurons / features
     ↓
circuits
     ↓
output
```

不再只问：

```python
model(x) == y
```

而是问：

```python
"model(x) 内部发生了什么计算，
  导致 y？"
```

这是重要的概念转变。

---

### 3. Reward hacking

他特别有意思的研究方向之一是 **reward hacking**。

简化版本：

```text
human objective
      ↓
approximate reward R(x)
      ↓
agent optimizes R(x)
      ↓
agent discovers loophole
      ↓
high reward
but bad behavior
```

他与 Alexander Pan、Erik Jones 和 Meena Jagadeesan 合作的 2024 年 ICML 论文 **“Feedback Loops With Language Models Drive In-Context Reward Hacking”** 研究了反馈循环如何导致越来越有问题的行为。（[Jacob Steinhardt][3]）

这很重要，因为前沿 agent 越来越多地在循环中运行：

```text
LLM
 ↓
action
 ↓
environment
 ↓
feedback
 ↓
LLM
 ↓
action
...
```

所以问题不只是“这个模型对齐了吗？”

还包括：

> **当一个未完美对齐的模型反复与环境交互并通过反馈进行优化时，会发生什么？**

---

## 他也与一些非常有趣的人有联系

他的学术网络很强。

他的博士导师是斯坦福大学的 **Percy Liang**。（[Simons Institute][2]）

他的学生和合作者包括从事以下方向的人：

* mechanistic interpretability
* AI safety
* LLM evaluation
* forecasting
* robust ML
* alignment

例如，后来成为主要 AI 安全研究者的 **Dan Hendrycks** 曾是他的学生之一。（[EECS at UC Berkeley][4]）

他近期的合作者包括 **Alec Radford**、Trevor Darrell、Sarah Schwettmann、Arvind Narayanan、Percy Liang、Jacob Andreas 等。（[Jacob Steinhardt][3]）

---

## 还有一个新动向：Transluce

Steinhardt 目前的网站显示，他还是 **Transluce 的创始人兼 CEO**，这是一个非营利研究实验室，专注于构建开放、可扩展的技术，用于理解前沿 AI 系统。（[Jacob Steinhardt][5]）

这一点很重要。

方向基本上是这样的：

```text
Frontier models are becoming enormous
              ↓
Humans cannot inspect them manually
              ↓
Need automated interpretability
              ↓
AI systems help humans understand AI systems
```

这与新兴的 **AI-assisted mechanistic interpretability** 理念非常接近。

例如，不再由人类手动检查成千上万的激活值：

```text
LLM
 ↓
activation traces
 ↓
attribution / causal analysis
 ↓
AI interpretability assistant
 ↓
human-readable explanation
```

他近期的论文如 **“Predictive Concept Decoders”** 和 **“Training Language Models to Explain Their Own Computations”** 正好契合这一方向。（[Jacob Steinhardt][3]）

---

### 为什么我认为他特别值得你研究

鉴于你已经在沿着 **Transformer internals → Q/K/V → MLA → model training → mechanistic understanding** 这条路前进，Steinhardt 是一个非常值得关注的研究者。

我会把他的工作分成三层来看：

```text
Layer 1 — ML theory
    robustness
    statistics
    adversarial examples
        ↓
Layer 2 — alignment
    reward specification
    reward hacking
    reliable ML
        ↓
Layer 3 — mechanistic interpretability
    neurons
    features
    circuits
    attribution
    latent representations
```

有趣的哲学要点在于，**Layer 3 试图把“alignment”从纯粹的行为评估转变为更接近理解实际计算的东西。**

这是一个非常深刻的方向。

### 我会从这些论文开始读

大致按此顺序：

1. **How do Language Models Bind Entities in Context?** — 理解 Transformer 表示。（[Jacob Steinhardt][3]）
2. **Overthinking the Truth** — LM 如何处理虚假示例。（[Jacob Steinhardt][3]）
3. **Feedback Loops With Language Models Drive In-Context Reward Hacking** — agentic/reward 动态。（[Jacob Steinhardt][3]）
4. **Training Language Models to Explain Their Own Computations** — AI 辅助的可解释性。（[Jacob Steinhardt][3]）
5. **Language Model Circuits Are Sparse in the Neuron Basis** — 与 mechanistic interpretability 直接相关。（[Jacob Steinhardt][3]）
6. **Learning a Generative Meta-Model of LLM Activations** — 如果你想理解下一代可解释性工具，尤其有趣。（[Jacob Steinhardt][3]）

[Jacob Steinhardt 的研究/出版物](https://jsteinhardt.stat.berkeley.edu/publications/?utm_source=chatgpt.com)

[Jacob Steinhardt 的伯克利主页](https://jsteinhardt.stat.berkeley.edu/?utm_source=chatgpt.com)

### 参考资料：

* [UC Berkeley Statistics — Jacob Steinhardt](https://statistics.berkeley.edu/people/jacob-steinhardt?utm_source=chatgpt.com)
* [Jacob Steinhardt — Publications](https://jsteinhardt.stat.berkeley.edu/publications/?utm_source=chatgpt.com)
* [UC Berkeley Research — Jacob Steinhardt](https://vcresearch.berkeley.edu/faculty/jacob-steinhardt?utm_source=chatgpt.com)
* [Simons Institute — Jacob Steinhardt](https://simons.berkeley.edu/people/jacob-steinhardt?utm_source=chatgpt.com)

[1]: https://statistics.berkeley.edu/people/jacob-steinhardt?utm_source=chatgpt.com "Jacob Steinhardt | Department of Statistics"
[2]: https://simons.berkeley.edu/people/jacob-steinhardt?utm_source=chatgpt.com "Jacob Steinhardt"
[3]: https://jsteinhardt.stat.berkeley.edu/publications/?utm_source=chatgpt.com "Publications - Jacob Steinhardt"
[4]: https://www2.eecs.berkeley.edu/Pubs/Dissertations/Faculty/jsteinhardt.html?utm_source=chatgpt.com "Ph.D. Dissertations | EECS at UC Berkeley"
[5]: https://jsteinhardt.stat.berkeley.edu/?utm_source=chatgpt.com "Jacob Steinhardt"