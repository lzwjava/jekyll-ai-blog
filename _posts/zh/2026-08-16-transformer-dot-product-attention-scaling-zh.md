---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Transformer点积注意力缩放
translated: true
type: note
---

**问题：如何理解Transformer在点积注意力中为什么要使用`1 / sqrt(d_k)`缩放？**

**答案：**

核心思想是：

**点积值会随着维度`d_k`增大而增长。大的点积值会使softmax变得过于“自信”，导致梯度消失。除以`sqrt(d_k)`可以将数值保持在一个合理的范围内。**（[NeurIPS论文][1]）

让我们推导一下。

## 1. 未缩放的注意力

Transformer注意力机制：

[
Attention(Q,K,V)=softmax(QK^T)V
]

单个查询和单个键之间的分数为：

[
score=q\cdot k
]

其中：

[
q,k \in R^{d_k}
]

示例：

```
q = [0.2, -0.5, 0.1]
k = [0.8,  0.3, -0.4]

q·k = 0.2*0.8 + (-0.5)*0.3 + 0.1*(-0.4)
    = -0.19
```

这只是一个相似度分数。

---

## 2. 为什么维度会使其爆炸？

点积为：

[
q\cdot k=\sum_{i=1}^{d_k}q_i k_i
]

假设：

[
q_i,k_i \sim N(0,1)
]

每次乘法：

[
q_i k_i
]

具有：

* 均值 = 0
* 方差 = 1

点积累加`d_k`个独立项：

[
Var(q\cdot k)=d_k
]

因此：

[
std(q\cdot k)=\sqrt{d_k}

```

这是关键部分。

典型量级增长为：

[
|q\cdot k|\approx \sqrt{d_k}
]

论文中明确提到了这个方差论证。（[NeurIPS论文][1]）

---

## 3. 示例：`d_k`改变一切

假设：

```

d_k = 16

std(score) ≈ sqrt(16)=4

```

分数可能如下：

```

[2.1, 1.8, -3.0, 0.5]

```

Softmax：

```

[0.55, 0.41, 0.02, 0.02]

```

没问题。

---

现在：

```

d_k = 1024

std(score)=sqrt(1024)=32

```

分数：

```

[25, 18, -30, 5]

```

Softmax：

[
softmax([25,18,-30,5])
]

几乎变成：

```

[0.999, 0.001, 0, 0]

```

模型会说：

> “这个键肯定是正确的。忽略其他所有内容。”

为时过早。

---

## 4. 为什么这对训练不利？

Softmax：

[
softmax(x_i)=\frac{e^{x_i}}{\sum e^{x_j}}
]

梯度：

[
\frac{\partial softmax_i}{\partial x_j}
=======================================

p_i(\delta_{ij}-p_j)
]

如果：

```

p = [0.999,0.001,0,0]

```

那么：

```

p(1-p)
≈ 0.999 * 0.001
≈ 0.001

```

梯度几乎为零。

意思是：

```

loss
 |
softmax
 |
attention score

```

无法向后传递有用的学习信号。

这正是论文中所说的：

> “将softmax函数推至梯度极小的区域。” （[NeurIPS论文][1]）

---

## 5. 为什么除以`sqrt(d_k)`？

因为：

[
std(q\cdot k)=\sqrt{d_k}
]

所以进行归一化：

[
score=\frac{q\cdot k}{\sqrt{d_k}}
]

现在：

[
Var(\frac{q\cdot k}{\sqrt{d_k}})
================================

\frac{d_k}{d_k}
=1
]

分数分布变得稳定：

```

之前：

d_k=64:
scores std ≈ 8

d_k=1024:
scores std ≈ 32

之后：

d_k=64:
scores std ≈ 1

d_k=1024:
scores std ≈ 1

```

维度不再改变量级。

---

## 6. 直觉类比

想象一下对文档进行排序。

无缩放：

```

小模型：

文档 A: 5
文档 B: 4
文档 C: 3

大模型：

文档 A: 500
文档 B: 400
文档 C: 300

```

Softmax 看到：

```

小模型：
[0.66,0.24,0.09]

大模型：
[1.0,0,0]

```

第二个失去了所有细微差别。

缩放就像是在应用 softmax 之前将：

```

500,400,300

转换为

5,4,3

```

---

## 7. 为什么加性注意力没有这个问题？

加性注意力计算：

[
score=W^T tanh(W_q q + W_k k)
]

神经网络通过学习到的权重和`tanh`来控制量级。

点积注意力要快得多，因为它只是：

```python
scores = Q @ K.T
```

这完美地映射到 GPU 矩阵乘法上。

Transformer 论文选择了：

```python
scores = Q @ K.T / sqrt(d_k)
attention = softmax(scores) @ V
```

因为它既获得了点积的速度，又避免了 softmax 饱和。（[哈佛 NLP][2]）

---

一个小的 PyTorch 演示：

```python
import torch
import torch.nn.functional as F

for dk in [16, 64, 512, 1024]:
    q = torch.randn(dk)
    k = torch.randn(dk)

    raw = q @ k
    scaled = raw / dk**0.5

    print(
        dk,
        "raw:", round(raw.item(),2),
        "scaled:", round(scaled.item(),2)
    )
```

典型输出：

```
16    raw: -3.5     scaled: -0.9
64    raw: 12.8     scaled: 1.6
512   raw: -35.2    scaled: -1.6
1024  raw: 44.7     scaled: 1.4
```

缩放使注意力对数保持在相似的数值范围内。

参考文献：

* （[NeurIPS论文][1]）
* （[哈佛 NLP][2]）

[1]: https://papers.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf?utm_source=chatgpt.com "Attention Is All You Need"
[2]: https://nlp.seas.harvard.edu/2018/04/01/attention.html?utm_source=chatgpt.com "The Annotated Transformer"
