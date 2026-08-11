---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Transformer注意力中的隐藏大小
translated: true
type: note
---

问题：我朋友在解释Wq/Wk和MLA时提到的`hidden_size`是什么意思？

答案：

`hidden_size`指的是**Transformer内部隐藏状态向量`x`的维度**。

在以下代码中：

```python
q = x Wq
```

`x`的尺寸为：

```
x ∈ R^(hidden_size)
```

因此如果：

```
hidden_size = 4096
```

那么一个token表示为：

```
x =
[
 0.12,
-0.31,
 0.55,
 ...
 0.88
]

length = 4096
```

这个4096维向量就是该token在模型内部的表示。

---

以类似Llama的模型为例：

假设：

```
hidden_size = 4096
num_heads = 32
head_dim = 128
```

因为：

```
32 heads × 128 dimensions/head = 4096
```

模型在各层之间保持相同的隐藏维度：

```
Token
 |
Embedding
 |
4096维隐藏状态
 |
Transformer块
 |
4096维隐藏状态
 |
Transformer块
 |
4096维隐藏状态
```

这个维度并不表示"4096个单词"或"4096个人类可理解的特征"，它只是一个学习得到的向量空间。

---

现在联系你朋友的话：

> Wq、Wk 都是降维运算，你合并后就是将维度升回到 hidden_size，各方面都爆增

他这里讨论的是**head维度与hidden_size的关系**。

通常情况下：

```
hidden_size = 4096
```

注意力机制分为多个head：

```
Q,K,V

4096
 |
 split
 |
32 heads

每个head:
128 dimensions
```

因此：

```
head_dim = hidden_size / num_heads

= 4096 / 32

= 128
```

对于每个head：

```
q_head = x Wq_head

4096 → 128
```

这就是"降维"的含义。

矩阵形式：

```
x:

[1 × 4096]


Wq_head:

[4096 × 128]


结果:

[1 × 128]
```

---

但如果要合并所有head：

```
32 heads × 128

= 4096
```

你会进行拼接：

```
[q1,q2,q3,...q32]

        |
        v

[1 × 4096]
```

然后通过输出投影：

```
Wo:

4096 × 4096
```

这样便恢复了hidden_size。

---

MLA（Multi-head Latent Attention，多头潜在注意力）改变了这一思路。

传统KV缓存：

```
K:

hidden_size

V:

hidden_size
```

每个token需要存储：

```
4096 + 4096

= 8192个数值/token
```

对于长上下文：

```
128k tokens × 8192

≈ 10亿个数值
```

内存爆炸。

MLA的做法：

不是：

```
x
 |
 +--> K 4096
 |
 +--> V 4096
```

而是：

```
x

↓

潜在向量

512维
```

存储：

```
512个数值/token
```

后续再重建K/V。

所以你朋友的意思是：

```
先降低维度（latent），然后才考虑合并
```

即：先压缩：

```
4096 → 512
```

再进行注意力相关操作。

而不是：

```
4096 → 多个head → 合并回4096
```

后者会产生巨大的KV缓存。

---

一个直观的理解模型：

```
hidden_size
=
模型"大脑状态"的宽度

对于GPT-3：
hidden_size = 12288

对于Llama 3 8B：
hidden_size = 4096

对于更大模型：
hidden_size可能为8192、16384等
```

Transformer内部的一切都围绕这个维度展开：

```
x:

[hidden_size]


Wq/Wk/Wv:

hidden_size → attention维度


MLP:

hidden_size → 更大的中间维度 → hidden_size
```

因此当你朋友说"升回hidden_size"时，他的意思是**将压缩后的注意力表示恢复为模型的主要内部向量宽度（例如4096维）。**
