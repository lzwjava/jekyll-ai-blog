---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 词嵌入与位置编码详解
translated: true
type: note
---

问题：在 Decoder-only Transformer 中，Positional Encoding 和 Word Embedding（如 word2vec）有什么区别？为什么位置信息很重要 —— 例如，在序列“刚想到了”中，Bigram“刚想”出现在“想到”之前，它们的位置映射在训练期间非常重要。

回答：

你的理解非常正确，直觉很敏锐。让我深入解析一下两者的区别。

---

## 1. Word Embedding vs. Positional Encoding —— 它们本质上是不同的东西

### Word Embedding (例如 word2vec)
Word Embedding 将 **Token 映射到一个表示其语义含义的 Vector**。例如：

- `"cat"` → `[0.21, -0.45, 0.87, ...]`
- `"dog"` → `[0.19, -0.42, 0.85, ...]` *(数值接近，因为处于相同的语义空间)*

Word Embeddings 在高维空间中捕捉单词的语义 —— 基本上，相似的单词具有相似的 Embedding。这些 Embedding 是从数据中学习到的，是 Neural Network 不可或缺的一部分。

重要的是，Embedding 本身**不包含该单词在句子中位置的信息**。无论 `"cat"` 出现在位置 1 还是位置 50，它的 Embedding 都是相同的。

---

### Positional Encoding
仅凭语义 Vector 无法告诉我们单词在句子中的位置。Positional Encoding 添加了第二个 Vector —— 一个用于编码位置索引（如“第一个词”或“第二个词”等）的 Vector。

原始论文将 Positional Encoding **叠加**（即相加）在实际的 Embedding 之上。Transformer 的最终输入为：`input = word_embedding + positional_encoding`。

这是**合并为一个 Vector 的两个独立关注点**：

| | Word Embedding | Positional Encoding |
|---|---|---|
| 编码内容 | 语义含义 (Semantic meaning) | 在序列中的位置 (Position in sequence) |
| 是否固定？ | 在训练期间学习 (Learned) | 固定 (Sinusoidal) 或学习所得 |
| 示例来源 | word2vec, BPE embedding | sin/cos 函数, 或 RoPE |
| 随位置变化？ | 否 | 是 |

---

## 2. 为什么位置很重要 —— 你举的“刚想到了”例子非常完美

你提供了一个极好的例子。在序列中：

> 刚 → 想 → 到 → 了

Bigram `"刚想"` 与 `"想到"` 携带不同的含义/关系，关键在于，**它们的顺序和相对位置是信号的一部分**。在训练期间：

- 模型看到 `"刚"` 在位置 `t`，`"想"` 在位置 `t+1`，`"到"` 在位置 `t+2`
- Positional Encoding 编码了每个 Token 的*所在位置*
- Attention 机制学习在不同位置之间分配权重 —— 因此 `"想"` 对 `"刚"`（紧随其后的 Token）产生的 Attention 与对远处某个 Token 产生的 Attention 是不同的

Self-attention 机制本身并不会按顺序处理序列数据 —— 它将输入视为一组独立于位置的 Token 集合。因此，Positional Embedding 对于整合序列顺序至关重要。

如果没有 Positional Encoding，Transformer 会将 `"刚想到了"` 和 `"了到想刚"` 视为**完全相同的词袋 (Bag of tokens)** —— 它无法分辨哪个词在前。

---

## 3. 正弦公式 (Original Transformer)

原始论文使用正弦 (Sine) 和余弦 (Cosine) 函数来为每个输入 Vector 计算一个值：

`PE(pos, 2i) = sin(pos / 10000^(2i/d_model))`
`PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))`

不同的维度以不同的频率振荡，为每个位置提供了一个**独一无二的指纹向量 (Fingerprint vector)**，模型可以学习并读取它。

---

## 4. 现代改进：RoPE (Rotary Position Embedding) —— Kimi 使用的技术

你提到了 Kimi 将 Attention 旋转 90 度 —— 这正是 RoPE。

RoPE 采用了一种本质上不同的方法：RoPE 不再添加独立的 Positional Encoding Vector，而是**对现有的 Token Embeddings 应用旋转 (Rotation)**。这种旋转在编码位置信息的同时保持了 Embedding 的范数 (Norm)。

RoPE 和 ALiBi 的运行原理都是**不对 Word Embedding 添加 Positional Encoding**；相反，它们专注于修改每一层计算出的 Attention Weights。这符合这样一种观点：位置信息和语义信息代表不同的事物，不应混合在一起。

---

## 5. Decoder-Only Transformer —— 为什么 Masking + Position 协同工作

在 Decoder-only 模型（如 GPT）中：
- Attention 是 **因果性的 (Causal/Masked)** —— 位置 `t` 的 Token 只能关注位置 `≤ t` 的 Token
- Positional Encoding 确保模型知道顺序 —— 因此 `"想"` 知道它在 `"刚"` 之后，并可以利用这一点

你观察到的 `"刚想 → 想到"` 顺序正是 **Positional Encoding + Causal Masking** 结合设计所要捕捉的。模型在训练过程中了解到，位置 `(t, t+1)` 的转换 `刚→想` 在统计上不同于位置 `(t+1, t+2)` 的 `想→到` —— 而位置信息正是使这两个 Bigram 在 Context 中可区分的关键。

---

## 总结

- **Embedding** = 单词的*含义*（语义空间，word2vec 风格）
- **Positional encoding** = 单词在序列中的*位置*
- 它们在进入 Attention 层之前**相加合在一起**
- 在 Decoder-only Transformer 中，Causal Masking + Positional Encoding 共同允许模型学习序列依赖关系（如 `"刚想"` 在 `"想到"` 之前）
- 现代变体如 RoPE 将位置编码在 **Attention 旋转内部**，而不是添加到输入中 —— 这样更优雅且具备更好的长度泛化性能力

参考文献：

- [Transformer Architecture: The Positional Encoding](https://kazemnejad.com/blog/transformer_architecture_positional_encoding/)
- [Positional Encoding Explained (Medium / The Deep Hub)](https://medium.com/thedeephub/positional-encoding-explained-a-deep-dive-into-transformer-pe-65cfe8cfe10b)
- [Positional Encoding in Transformers — IBM](https://www.ibm.com/think/topics/positional-encoding)
- [Positional Embeddings: Evolution from Text to Vision (ICLR 2025)](https://iclr-blogposts.github.io/2025/blog/positional-embedding/)
- [Understanding Positional Encoding in Transformers — Kemal Erdem](https://erdem.pl/2021/05/understanding-positional-encoding-in-transformers/)
