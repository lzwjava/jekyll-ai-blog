---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KV缓存：以内存换速度
translated: true
type: note
---

**KV缓存（Key-Value缓存）** 是一种在大语言模型（LLM）推理过程中使用的技术，用于避免对模型已处理过的token进行重复计算。它能显著加快文本生成速度。

### 直观理解

假设你正在逐词写一个句子：

> "The cat sat on the..."

为了预测下一个词，模型需要考虑之前所有的词：

* The
* cat
* sat
* on
* the

如果没有KV缓存，每当生成一个新词时，模型都会从头开始重新处理整个序列。

有了KV缓存，模型会记住之前token的重要中间计算结果，并且只对新生成的token进行计算。

---

## 为什么是“Key”和“Value”？

LLM使用**自注意力机制**。对于每个token，模型会计算三个向量：

* **查询（Query，Q）** – 当前token在寻找什么
* **键（Key，K）** – 每个之前token代表什么
* **值（Value，V）** – 每个token包含的信息

注意力公式大致如下：

$$
\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V
$$

在生成过程中：

* 旧token的键和值从不改变。
* 只有最新的token需要新的K和V向量。

因此，不是重新计算每个之前token的K和V，而是将它们**缓存**起来。

---

## 没有KV缓存的情况

假设提示词有1000个token。

生成第1001个token：

* 计算token 1–1000的K/V
* 计算token 1001的Q
* 执行注意力计算

生成第1002个token：

* 再次计算token 1–1001的K/V
* 计算token 1002的Q
* 执行注意力计算

如此反复。

---

## 有KV缓存的情况

在提示词处理一次之后：

```
KV缓存

Token 1  -> K1, V1
Token 2  -> K2, V2
...
Token1000 -> K1000, V1000
```

生成token 1001时：

* 只计算：

  * Q1001
  * K1001
  * V1001
* 使用缓存的K1...K1000和V1...V1000。

然后追加：

```
Token1001 -> K1001, V1001
```

对下一个token重复此过程。

---

## 可视化

没有缓存：

```
提示词
  ↓
Transformer
  ↓
生成token 1

提示词 + token1
      ↓
Transformer
      ↓
生成token2

提示词 + token1 + token2
           ↓
Transformer
```

所有内容都被重新计算。

有缓存：

```
提示词
   ↓
一次性计算K,V
存入缓存

生成token1
只计算token1的K,V
追加到缓存

生成token2
只计算token2的K,V
追加到缓存
```

只进行增量计算。

---

## 性能优势

KV缓存：

* 🚀 大幅减少自回归解码过程中的计算量。
* ⚡ 降低每个生成token的延迟。
* 📈 提高每秒生成的token数量。

这就是为什么几乎所有生产环境中的LLM服务系统（例如vLLM、TensorRT-LLM和Hugging Face Text Generation Inference）都使用KV缓存。

---

## 内存代价

代价是内存。

每生成一个token，都会为**每个Transformer层**存储K和V张量。

缓存大小大致成正比：

$$
\text{缓存大小} \propto
\text{序列长度}
\times
\text{层数}
\times
\text{隐藏层大小}
$$

对于长上下文（例如128K或1M个token），KV缓存可能消耗数十甚至数百GB的GPU内存，这就是为什么现代推理系统中会使用**KV缓存量化**、**分页KV缓存**和**缓存驱逐**等技术。

---

## 训练阶段与推理阶段的对比

* **训练阶段：** 通常**不使用**KV缓存，因为所有token是并行处理的，并且梯度必须流经完整的计算图。
* **推理阶段：** KV缓存是必不可少的，因为token是逐个顺序生成的。

---

## 一个简单的类比

想象一下，你在读一本书，每读完一章就做笔记。

* **没有KV缓存：** 每次有人问下一章的内容时，你都要从第1页重新读完整本书。
* **有KV缓存：** 你保留之前章节的笔记，只读新的一章，然后更新笔记。

笔记类似于缓存的**键**和**值**，让模型避免重复工作，同时仍然能够关注完整的历史。