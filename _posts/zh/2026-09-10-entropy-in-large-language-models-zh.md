---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型中的熵
translated: true
type: note
---

Question: 在大语言模型（LLMs）的语境中，熵（entropy）是什么？

Answer:

LLMs 中的熵指的是模型在可能的下一个 token 概率分布中**不确定性或随机性**的度量。它源自信息论（香农熵），定义如下：

**H(P) = −∑ P(x) · log P(x)**

其中 P(x) 是分配给每个 token x 的概率。

**实际意义：**

- **高熵** → 模型不确定，概率分散在多个 token 上（例如，开放式的创意任务）
- **低熵** → 模型自信，概率集中在少数 token 上（例如，事实性或确定性的补全）

**熵在 LLMs 中的体现：**

| 上下文 | 作用 |
|---|---|
| **温度采样** | 温度在 softmax 之前缩放 logits，直接控制输出熵——温度越高，熵越高 |
| **困惑度** | 困惑度 = exp(H)，是衡量模型对文本序列“惊讶程度”的标准指标 |
| **训练损失** | 交叉熵损失衡量模型分布与真实分布之间的差距 |
| **Top-p / Top-k 采样** | 这些方法通过隐式截断分布来控制有效熵 |

**直观理解：** 如果模型将 99% 的概率分配给一个 token，则熵 ≈ 0（非常确定）。如果模型将概率均匀分布在 10,000 个 token 上，则熵达到最大值（非常不确定）。

参考：
- [香农熵 – Wikipedia](https://en.wikipedia.org/wiki/Entropy_(information_theory))
- [语言模型的困惑度 – Hugging Face Docs](https://huggingface.co/docs/transformers/perplexity)
- [LLMs 中的温度与采样 – Lilian Weng's Blog](https://lilianweng.github.io/posts/2021-03-21-lm-bpe/)