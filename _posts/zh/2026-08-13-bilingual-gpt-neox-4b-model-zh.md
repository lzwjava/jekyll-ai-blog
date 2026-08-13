---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双语GPT-NeoX 4B模型
translated: true
type: note
---

问题：`rinna/bilingual-gpt-neox-4b` 简介

答案：

`rinna/bilingual-gpt-neox-4b` 是由 Rinna 发布的**日英双语 GPT-NeoX 解码器专用语言模型**。它是当前 Llama/Qwen 时代之前，一个经典的**从头预训练 Transformer 语言模型**的典型示例。([Hugging Face][1])

从高层次看：

```
文本
 ↓
SentencePiece 分词器
 ↓
token id
 ↓
嵌入层
 ↓
GPT-NeoX Transformer 模块 × 36
 ↓
语言模型头
 ↓
下一个 token 的概率
```

它基本上是：

```
GPT 风格的自回归语言模型：

P(x) = Π P(x_t | x_<t)
```

意思是它学习：

> 给定之前的 token，预测下一个 token。

示例：

```
输入：
今日は天気が

模型预测：
良い
```

---

## 模型大小 / 架构

关键数据：([Hugging Face][1])

| 项目         | 值                                 |
| ------------ | ---------------------------------- |
| 参数量       | 3.8B (~40亿)                       |
| 架构         | GPT-NeoX                           |
| 层数         | 36                                 |
| 隐藏层维度   | 2816                               |
| 上下文长度   | 基础模型（也存在 8K 变体）         |
| 精度         | FP16                               |
| 语言         | 日语 + 英语                        |
| 许可证       | MIT                                |

架构：

```
hidden = 2816

for layer in 36:
    x = x + Attention(LayerNorm(x))
    x = x + MLP(LayerNorm(x))
```

注意力机制：

```
Q = XWq
K = XWk
V = XWv

Attention(Q,K,V)
 = softmax(QKᵀ / sqrt(d))V
```

与你正在学习的 Transformer 机制相同。

---

## 为什么隐藏层维度是 2816？

对于 GPT-NeoX：

```
hidden_size = 2816

注意力头数 = ?
```

通常：

```
head_dim = hidden_size / num_heads
```

例如：

```
num_heads = 22

2816 / 22 = 128
```

因此每个注意力头在 128 维空间中运行。

模型内部有：

```
token 嵌入：

vocab_size × 2816
```

每个 token 变成：

```
token id
   |
嵌入查找
   |
2816 维向量
```

然后每个 Transformer 层都会转换这个向量。

---

## 训练数据

该模型在大约 **524B tokens** 的混合数据集上进行了预训练，包括：

* 日语 CC-100
* 日语 C4
* The Pile
* 其他语料库 ([Hugging Face][1])

这很有趣，因为：

一个 4B 模型使用 524B tokens 进行了大量训练。

比较 Chinchilla 缩放定律：

```
最佳 token 数 ≈ 20 × 参数量

4B × 20
= 80B tokens
```

他们使用了：

```
524B tokens
```

这远多于 Chinchilla 最优值。

所以这个模型在某种程度上是**数据丰富的**。

---

## 与 GPT-NeoX 的关系

GPT-NeoX 由 EleutherAI 创建。

架构演变：

```
GPT-2
 |
GPT-Neo
 |
GPT-NeoX
 |
rinna 双语 GPT-NeoX
```

主要改进：

* 并行注意力 + MLP 实现
* 旋转位置编码 (RoPE)
* 针对更大模型的更好扩展性

代码库基于 EleutherAI GPT-NeoX。([Hugging Face][1])

---

## 与您的 nanoGPT 实验对比

您的 GPT-2 124M：

```
层数        ~12
隐藏层维度   768
参数量       124M
```

rinna：

```
层数        36
隐藏层维度   2816
参数量       3.8B
```

近似比较：

```
嵌入维度：

768
 |
2816
（大 3.7 倍）

层数：

12
 |
36
（深 3 倍）

参数量：

124M
 |
3.8B
（大约大 30 倍）
```

前向传播在概念上是相同的。

您的 nanoGPT：

```python
x = embedding(tokens)

for block in blocks:
    x = block(x)

logits = lm_head(x)
```

rinna：

```python
x = embedding(tokens)

for block in 36 GPTNeoXBlocks:
    x = block(x)

logits = lm_head(x)
```

只是规模大得多。

---

## 可用变体

该系列包括：

```
bilingual-gpt-neox-4b
        |
        +-- 基础模型
        |
        +-- instruction-sft
        |
        +-- instruction-ppo
        |
        +-- minigpt4 (视觉)
```

SFT 版本增加了指令跟随能力：

```
基础模型
      |
      | 监督微调
      ↓
聊天模型
```

PPO 版本增加了 RLHF 对齐。([Hugging Face][2])

---

## 硬件要求

FP16 权重：

```
3.8B 参数 × 2 字节

≈ 7.6GB
```

加上运行时内存：

```
权重        7.6GB
KV 缓存     取决于上下文长度
激活值      取决于批次大小
CUDA 开销   ~1GB
```

推理：

* RTX 4070 12GB：小批次可行
* RTX 4090 24GB：轻松运行
* CPU：量化后可行

对于微调：

LoRA：

```
12GB GPU：可行
24GB GPU：轻松运行
```

完整训练：

```
3.8B × 优化器状态

FP32 Adam：

权重
+ 梯度
+ 动量
+ 二阶动量

≈ 16 字节/参数

3.8B × 16
≈ 60GB
```

需要分布式 GPU。

---

## 为什么这个模型在历史上很有趣

它代表了转型时期：

```
GPT-2 时代
(2019)
 |
GPT-NeoX 20B
(2022)
 |
rinna 双语 4B
(2023)
 |
Llama 2
 |
Qwen / DeepSeek 时代
```

今天一个 4B 模型看起来很小，但当时它是一个具有大规模预训练预算的重要开源双语模型。

对于学习 Transformer 内部机制，它实际上是一个非常好的规模：

* 足够小，易于理解
* 足够大，能展示真实的扩展行为
* 权重开放
* 纯解码器 Transformer

参考资料：

* [rinna/bilingual-gpt-neox-4b on Hugging Face](https://huggingface.co/rinna/bilingual-gpt-neox-4b?utm_source=chatgpt.com)
* [Release of Pre-Trained Models for the Japanese Language paper](https://huggingface.co/rinna/bilingual-gpt-neox-4b?utm_source=chatgpt.com)
* [rinna/bilingual-gpt-neox-4b-instruction-sft](https://huggingface.co/rinna/bilingual-gpt-neox-4b-instruction-sft?utm_source=chatgpt.com)

[1]: https://huggingface.co/rinna/bilingual-gpt-neox-4b?utm_source=chatgpt.com "rinna/bilingual-gpt-neox-4b · Hugging Face"
[2]: https://huggingface.co/rinna/bilingual-gpt-neox-4b-instruction-sft?utm_source=chatgpt.com "rinna/bilingual-gpt-neox-4b-instruction-sft · Hugging Face"