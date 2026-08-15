---
audio: false
generated: true
image: false
lang: zh
layout: post
title: XLNet：克服BERT的局限性
translated: true
type: note
---

## 问题：杨志麟及其工作 XLNet 简介

杨志麟是 **XLNet: Generalized Autoregressive Pretraining for Language Understanding**（2019 年）的主要作者之一，这是一个重要的 NLP 模型，与 Google 的 BERT 竞争并影响了后来的 Transformer 模型。

论文：
**XLNet: Generalized Autoregressive Pretraining for Language Understanding**
作者：Zhilin Yang, Zihang Dai, Yiming Yang, Jaime Carbonell, Ruslan Salakhutdinov, Quoc V. Le

---

## 1. XLNet 存在的原因：BERT 的局限性

在 XLNet 之前：

### GPT（2018 年）

自回归：

```
x1 → x2 → x3 → x4
```

训练目标：

[
P(x)=\prod_t P(x_t|x_{<t})
]

它预测下一个 token。

问题：

* 只学习从左到右的依赖关系
* 无法看到未来的 token

---

### BERT（2018 年）

BERT 引入了 **掩码语言建模（MLM）**：

输入：

```
The cat [MASK] on the mat.
```

预测：

```
sat
```

BERT 看到两侧：

```
The cat <MASK> on the mat
          ↑
     左侧 + 右侧上下文
```

优势：

* 双向表示

问题：

训练目标与真实生成不匹配。

训练时：

```
The cat [MASK] on the mat
```

推理时：

```
The cat sat on the mat
```

模型在推理时从未见过 `[MASK]`。

这造成了 **预训练-微调不一致**。

---

# 2. XLNet 的关键思想：排列语言建模

XLNet 结合了：

* GPT 的自回归目标
* BERT 的双向上下文

技巧：

不再按固定顺序预测 token：

```
1 → 2 → 3 → 4
```

而是随机选择一个顺序。

示例：

原始句子：

```
A B C D
```

排列：

```
C A D B
```

训练：

预测：

```
C
给定无

A
给定 C

D
给定 C, A

B
给定 C, A, D
```

数学上：

[
P(x)=
\prod_t P(x_{z_t}|x_{z_{<t}})
]

其中：

* z 是一个随机排列

---

## 3. 为什么这能提供双向上下文

示例：

句子：

```
I love machine learning
```

预测：

```
machine
```

普通 GPT：

```
I love → machine
```

仅看到：

```
I love
```

XLNet 可以采样：

```
learning → machine
```

因此当预测 "machine" 时：

```
I love
+
learning
```

两侧都能贡献。

它学习：

```
左侧上下文 + 右侧上下文
```

而不使用 `[MASK]`。

---

# 4. Transformer-XL 的联系

XLNet 建立在 Transformer-XL 之上。

Transformer-XL 引入了：

## 段循环

普通 Transformer：

```
tokens
 ↓
attention
 ↓
遗忘所有
```

Transformer-XL：

```
段 1
    ↓
memory
    ↓
段 2
```

它保留之前的隐藏状态：

[
h_{t-1}
]

作为记忆。

优点：

* 更长的上下文
* 更快的训练
* 更好的长文档理解

XLNet 使用它是因为语言建模需要长距离依赖。

---

# 5. XLNet 架构

高层次：

```
文本
 |
分词器
 |
Transformer-XL 主干
 |
排列 attention
 |
语言建模头
 |
下一个 token 预测
```

它仍然是解码器风格的 Transformer。

与 BERT 不同：

```
BERT：
编码器 Transformer
```

XLNet：

```
自回归 Transformer
```

---

# 6. 双流注意力

一个非常重要的技术细节。

问题：

如果预测 token x3，模型不能直接知道 x3 本身。

XLNet 使用：

## 内容流

普通的隐藏表示：

[
h_t
]

包含 token 信息。

## 查询流

预测表示：

[
g_t
]

不包含目标 token。

示例：

预测：

```
C
```

查询：

```
A B ?
```

内容：

```
A B C
```

查询关注内容但不关注自身。

这防止了信息泄露。

---

# 7. XLNet 与 BERT 与 GPT 对比

| 模型               | 目标             | 上下文      |
| ------------------ | ---------------- | ---------- |
| GPT                | 下一个 token     | 仅左侧     |
| BERT               | 掩码 token       | 两侧       |
| XLNet              | 排列自回归       | 两侧       |
| GPT-4 风格模型     | 自回归缩放       | 仅左侧     |

---

# 8. 为什么 XLNet 后来没有主导

XLNet 在 2019 年非常强大：

* 在许多基准测试上击败了 BERT
* 引入了更好的目标

但后来，规模改变了一切。

行业转向了：

```
简单目标
+
海量数据
+
海量计算
```

GPT 风格的目标胜出是因为：

1. 它天然具有生成性
2. 更容易扩展
3. 直接适用于对话
4. 更好的工程生态系统

如今：

```
GPT-3
GPT-4
Llama
Qwen
DeepSeek
```

都使用因果自回归训练。

---

# 9. 历史重要性

演变过程：

```
RNN/LSTM
    |
    v
Transformer (2017)
    |
    +---- GPT（自回归）
    |
    +---- BERT（掩码建模）
    |
    +---- Transformer-XL（长记忆）
              |
              v
            XLNet
              |
              v
       现代大型语言模型
```

XLNet 是在该领域发现以下事实之前，最后一次改进预训练目标的重要尝试之一：

> 扩展一个简单的自回归 Transformer 比设计一个更巧妙的目标更好。

---

# 10. 杨志麟的更广泛贡献

杨志麟研究过几个重要的 NLP 主题：

* XLNet
* Transformer-XL
* 语言建模
* 表示学习

他的工作帮助连接了：

```
小型 NLP 模型
      ↓
大规模预训练语言模型
```

XLNet 的核心洞察是：

> 你可以保持数学上干净的自回归目标，同时恢复使 BERT 强大的双向信息流。

这一思想影响了研究人员对现代 LLM 中 **注意力、信息流和训练目标** 的思考方式。

参考文献：

* Yang et al., "XLNet: Generalized Autoregressive Pretraining for Language Understanding" (2019): [https://arxiv.org/abs/1906.08237](https://arxiv.org/abs/1906.08237)
* Dai et al., "Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context" (2019): [https://arxiv.org/abs/1901.02860](https://arxiv.org/abs/1901.02860)
* Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" (2018): [https://arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805)
