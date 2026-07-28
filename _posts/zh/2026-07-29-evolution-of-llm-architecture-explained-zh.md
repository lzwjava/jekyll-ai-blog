---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM架构演变解析
translated: true
type: note
---

问题：附带的“22580: 从GPT-2到Kimi3，解释”这篇文章是什么意思？

回答：

这是对**现代LLM架构如何从GPT-2（2019年）演进到Kimi K3（2026年）**的技术解释。核心观点是：

> 现代LLM的进步不仅仅是“把模型做得更大”，而是关于改进**记忆、检索、效率和容量管理**。

作者从一个对比开始：

> “一个Kimi K3模型拥有约2.8万亿参数，大约相当于22,580个GPT-2模型的参数总量。”

这意味着：

* GPT-2：
  * 1.24亿参数
  * 12个Transformer层
  * 12个注意力头
  * 隐藏维度768
* Kimi K3：
  * 约2.8万亿参数

但有趣的部分不仅仅是规模。

---

## 1. GPT-2：纯Transformer

GPT-2是一个普通的仅解码器Transformer：

```
tokens
  |
embedding
  |
Transformer blocks
  |
linear head
  |
next token prediction
```

每个块：

```
x
 |
LayerNorm
 |
Attention
 |
+
 |
LayerNorm
 |
MLP
 |
+
 |
output
```

文章中的代码：

```python
x = x + self.attn(self.ln_1(x))
x = x + self.mlp(self.ln_2(x))
```

是核心GPT架构。

---

## 2. 问题：注意力内存随上下文长度增长

标准注意力：

```
Q × K^T
```

对于序列长度N：

```
注意力矩阵：

N × N
```

示例：

10,000个token：

```
10000 × 10000
= 1亿个注意力分数
```

文章解释说，如果没有KV缓存，生成时会反复重新计算旧token。

KV缓存解决了这个问题：

在生成过程中：

```
旧token
   |
存储K,V
   |
新token只计算新的Q
```

但是：

```
KV缓存大小 ∝ 序列长度
```

长上下文变成了内存带宽问题。

---

## 3. 线性注意力：替代增长的内存

传统注意力：

```
Attention(Q,K,V)

= softmax(QKᵀ)V
```

昂贵的部分：

```
QKᵀ

N × N
```

线性注意力改变了计算顺序：

不再使用：

```
(QKᵀ)V
```

而是：

```
Q(KᵀV)
```

现在：

```
KᵀV
```

变成了一个固定大小的状态。

内存：

```
Transformer注意力：
O(N)

KV缓存无限增长


线性注意力：
O(1)

固定内存
```

文章解释说：

> 线性注意力将不断增长的K/V向量折叠成一个固定的D×D状态。

---

## 4. 线性注意力的问题

问题：

固定内存的容量有限。

想象一下：

```
内存 = 1000个槽位

写入：
cat = animal
dog = animal
...

在数百万个事实之后：

cat?
dog?
```

信息重叠。

文章称之为：

> “信息干扰”

基本上：

```
旧知识
+
新知识
=
内存冲突
```

---

## 5. DeltaNet：学习覆盖什么内容

DeltaNet引入了更智能的内存更新。

不再使用：

```
内存 += 新信息
```

而是：

```
old_value = 内存[key]

error = new_value - old_value

内存 += error
```

类似于梯度下降。

示例：

之前：

```
内存：
Apple -> 水果
```

新信息：

```
Apple -> 公司
```

Delta更新：

```
移除旧关联
写入新关联
```

文章：

> “旧信息被移除，新信息被写入其位置。”

---

## 6. 门控DeltaNet：增加遗忘机制

人类记忆会遗忘。

纯DeltaNet：

```
更新特定记忆
```

但无法全局遗忘。

门控版本：

```
内存 = alpha * 旧内存 + 新信息
```

其中：

```
alpha = 0

遗忘所有内容

alpha = 1

保持记忆
```

文章将这个想法与Mamba风格的状态衰减联系起来。

---

## 7. Kimi Linear：混合架构

Kimi Linear结合了：

```
DeltaNet
+
MLA注意力
+
MoE
```

这意味着：

### DeltaNet

廉价的长时记忆：

```
恒定内存
```

### MLA（多头潜在注意力）

精确检索：

```
需要时进行全注意力
```

### MoE

更多参数，但无需全部激活。

示例：

```
898个专家

token选择16个专家
```

文章指出：

> Kimi K3有898个专家；每个token选择16个。

所以：

```
总模型：

898个专家

但每个token只使用：

16个专家
```

这节省了计算量。

---

## 8. Kimi K3架构直觉

简化视图：

```
输入

 |
 |
Delta Attention
（快速记忆）

 |
MoE
（专门知识）

 |
Delta Attention

 |
MLA
（昂贵检索）

 |
MoE

 |
输出
```

该模型有两种类型的记忆：

### 快速记忆

DeltaNet：

```
廉价
恒定大小
长上下文
```

### 精确记忆

MLA：

```
昂贵
精确检索
```

类似于计算机：

```
RAM + SSD

不是单一存储系统
```

---

## 核心思想

演进过程：

```
GPT-2
 |
 | 扩展参数
 v
GPT-3
 |
 | 更好训练
 v
GPT-4
 |
 | 高效记忆
 v
线性注意力
 |
 | 更好记忆更新
 v
DeltaNet
 |
 | 混合记忆
 v
Kimi Linear
 |
 | MoE + MLA + 扩展
 v
Kimi K3
```

作者的结论：

> 重要的变化不仅仅是规模。每一种架构都在改变模型存储什么、如何更新记忆，或如何检索信息。

对于使用nanoGPT训练GPT-2风格模型的人来说，关键要点是：**未来的LLM正在从“带更大KV缓存的巨型Transformer”转向“神经记忆系统”**。

GPT-2：

```
注意力 = 每次读取所有内容
```

Kimi K3：

```
快速学习记忆
+
选择性检索
+
稀疏专家
```

这就是架构上的转变。