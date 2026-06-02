---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT 模型中的共享令牌嵌入
translated: true
type: note
---

Question: 在 GPT 系列中，每个 token 是否都有一个固定的、共享的 embedding？模型中是否存在一个通用的 embedding table？

Answer:

是的——也不全是。让我仔细说明其中的细微差别，因为这个问题有两个层面的答案。

---

## 1. 是的：每个 Token 在共享查找表中都有一行

在 Transformer architecture 中，第一层通过使用一个 **lookup table** 来对 token ID 进行 embedding，该表包含每个可能 token 的 embedding。一个 token embedding 是一个具有特定长度的 vector，代表了该 token 的含义。

具体来说，以拥有约 50,000 个 token 的 GPT-2 为例：

对于小型模型，embedding matrix 的大小为 `(50,000 × 768)`，即有 50,000 个 token 和 768 个维度。

这意味着每个 token ID（例如，token #1234 = `" cat"`）**精确对应于该矩阵中的一行**。这是一个简单的 lookup 操作——无需计算，只需检索该行。这就是你所想到的“固定”部分：一旦训练完成，表中每个 token 对应的行就是冻结的。

---

## 2. 但“固定”仅限于训练后——它们是学习得来的，而非预定义的

这里是关键点：这些 embedding **不是手工制作或预先设定的**。它们是在训练过程中从零开始学习得到的。

这些 embedding 是在整个 Transformer 模型的 **training 过程中学习到的**。它们 **不是预先定义或提前固定的**——它们作为模型训练过程的一部分被学习。它们以随机值初始化，是模型 learnable parameters 的一部分。在训练期间，它们通过 backpropagation 进行更新。

在模型训练（如 GPT 中的 next-word prediction）期间，embedding 通过 backpropagation 进行更新。只有对应于当前 batch 中 token 的行会被调整。经过多次迭代，模型学会调整这些 vector，使得出现在相似上下文中的词（如 "cat" 和 "dog"）具有相似的 embedding，而无关的词在 vector space 中则相距较远。

因此其生命周期如下：

| Phase | State of Embedding |
|---|---|
| Before training | Random noise vectors |
| During training | Continuously updated via backprop |
| After training (inference) | Frozen — 每个 token 对应一个固定 vector |

---

## 3. 这与 Word2Vec 不同

Word2Vec 将 embedding 作为独立步骤进行 **单独训练**，然后将其插入模型中。而 GPT 将 embedding table 与所有 transformer weights **端到端地共同训练**——embedding 只是完整模型中的另一个 weight matrix。

GPT 风格的 Transformer 中的 embedding **不是一个需要单独训练的独立特征**——它们与模型的其余部分一起训练。每当网络进行 backpropagation 时，它都会更新 embedding vectors，以便更好地通过捕捉词项关系来进行准确预测。在 inference 时，每个 token 学习到的 vector 通过一次 lookup 即可检索，供 self-attention 机制使用。

---

## 4. 一个重要的现代细节：Input Embedding ≠ Output Embedding

在 GPT-2 时代，input embedding 和 output unembedding 是相同的。而现在，embedding 和 unembedding 矩阵通常是 **分开学习的**。

这意味着：

- **Input side**: token ID → embedding vector（输入到 attention layers）
- **Output side**: 最终的 hidden state → 投影回 vocabulary logits（一个独立的矩阵）

它们曾经是被绑定在一起的（共享权重），但现代模型为了获得更好的性能将它们分开了。

---

## Summary

- 是的，存在 **一个共享的 embedding table** —— 词汇表中的每个 token 对应一行
- 每个 token 总是映射到 **同一个 vector**（训练后），因此在 inference 阶段它是“固定”的
- 但这些 vector **并非预先固定** —— 它们像其他 weight 一样，在训练期间端到端地学习得到
- embedding table 在 PyTorch 中本质上是 `nn.Embedding(vocab_size, d_model)` —— 一个随机初始化的 learnable matrix

References:

- [Token Embeddings and Positional Embeddings Explained – Cloud-ML](https://cloud-ml.de/llm-token-embeddings/)
- [From One-Hot to Learned Representations: GPT-Style Embeddings](https://medium.com/@nsimaria_83213/from-one-hot-to-learned-representations-understanding-gpt-style-embeddings-ec096f47270d)
- [LLM Basics: Embedding Spaces – LessWrong](https://www.lesswrong.com/posts/pHPmMGEMYefk9jLeh/llm-basics-embedding-spaces-transformer-token-vectors-are)
- [Token Embeddings – Angel Vyas](https://angelvyas.com/posts/llm/token_embeddings/)
