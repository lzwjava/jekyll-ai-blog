---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-2分词器：确定性BPE处理
translated: true
type: note
---

在LLM分词器（如nanoGPT/GPT-2中使用的）中，标点符号、缩略词和非英语单词是如何处理的？同一个字符串在不同上下文中是否可能以不同方式分词？

答案：

**GPT-2使用字节对编码（BPE）**，通过`tiktoken`库（或原始`gpt2`分词器）实现。以下是它处理你提到的具体情形的方式：

---

**像`, . '`这样的标点符号**

这些标点会根据BPE合并规则被当作独立token，或与相邻字符合并。GPT-2的分词器还会应用一个**预分词正则表达式**，在BPE运行*之前*拆分文本，大致如下：

```
's|'t|'re|'ve|'m|'ll|'d| ?\w+| ?\d+| ?[^\s\w\d]+|\s+
```

因此标点符号会先被明确拆分出来，然后BPE合并会在每个片段内进行。

---

**像`I'm`这样的缩略词**

预分词正则表达式将常见的英语缩略词作为**固定模式**处理：

- `I'm` → 总是拆分为 `I` + `'m`（两个token）
- `don't` → `don` + `'t`
- `they're` → `they` + `'re`

所以**不会** — `I'm` **不会**有时是一个token，有时是两个。正则表达式保证了在BPE运行*之前*就有一致的拆分。分词是**确定性的且与上下文无关** — 相同的字符串总是产生相同的token。

---

**非英语单词**

BPE基于**字节**运行，因此任何Unicode字符都是有效的。不过：

- 常见的英语子词有学习到的合并规则（例如 `un` + `der` → `under`）
- 罕见或非英语的单词会被分割成小片段，甚至**单个UTF-8字节**
- 示例：像`你`这样的中文字符可能会变成3个字节级token：`\xe4`、`\xbd`、`\xa0`

GPT-2的50,257个token词表几乎完全是在英语文本上训练的，因此非英语语言的效率非常低 — 一个中文单词可能需要3–6个token，而一个英语单词只需要1个。

---

**分词是否可能依赖上下文？**

对于GPT-2/tiktoken：**不会。** 它是一个纯粹的确定性函数。相同的字节 → 始终生成相同的token。

一些较新的分词器（如T5或某些多语言模型中使用的）会应用带归一化的**sentencepiece**，其效果*可能*随上下文略有变化，但这是另一种设计。

---

参考资料：

- [OpenAI tiktoken](https://github.com/openai/tiktoken)
- [GPT-2 tokenizer (Hugging Face)](https://huggingface.co/docs/transformers/model_doc/gpt2#transformers.GPT2Tokenizer)
- [BPE explanation — Sennrich et al. 2016](https://arxiv.org/abs/1508.07909)
- [nanoGPT by Karpathy](https://github.com/karpathy/nanoGPT)
