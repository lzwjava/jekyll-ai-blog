---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 曼巴：用于大语言模型的选择性状态空间模型
translated: true
type: note
---

问题：**在大型语言模型中，Mamba 是什么意思？**

回答：

**Mamba 是一种用于序列建模的神经网络架构，它用一种更高效的机制——*选择性状态空间模型（SSM）*——取代了 Transformer 的自注意力机制。**

其核心思想是：

> **Mamba 不是让每个词元都关注其他所有词元，而是维护一个紧凑的隐藏状态，并在词元到达时进行更新。**

### 1. Transformer 与 Mamba 的对比

一个 Transformer 层大致做的事情是：

```text
x₁ ─┐
x₂ ─┤
x₃ ─┤──> 自注意力 ──> y₁,y₂,y₃,...
x₄ ─┤
... ┘
```

对于每个词元，注意力计算：

[
\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V
]

因此，当序列长度为 (L) 时，注意力矩阵大致为：

```text
L × L
```

这就是为什么普通的注意力机制具有 **O(L²)** 的交互成本。

而 Mamba 则更像这样：

```text
x₁ ──> state₁ ──> y₁
          │
x₂ ──────>state₂ ──> y₂
             │
x₃ ─────────>state₃ ──> y₃
                │
x₄ ────────────>state₄ ──> y₄
```

它有一个循环状态：

[
h_t = f(h_{t-1}, x_t)
]

以及输出：

[
y_t = g(h_t, x_t)
]

因此，该模型不需要显式地构建一个 (L\times L) 的注意力矩阵。

---

### 2. SSM 中的“S”代表什么？

经典的状态空间模型大致是这样：

[
h_t = Ah_{t-1} + Bx_t
]

[
y_t = Ch_t
]

可以理解为：

* (x_t)：当前词元
* (h_t)：模型的记忆
* (A)：先前的记忆如何被保留/转换
* (B)：新输入如何进入记忆
* (C)：记忆如何产生输出

这本质上是一种 **可学习的循环记忆**。

早期 SSM 的问题在于它们的参数是相对固定的。

Mamba 的一个重要技巧是：

> **让状态空间参数依赖于当前输入。**

概念上：

```python
B_t = f_B(x_t)
C_t = f_C(x_t)
Δ_t = f_Δ(x_t)

h_t = A(Δ_t) @ h_{t-1} + B_t @ x_t
y_t = C_t @ h_t
```

因此，模型可以学会：

```text
“这个词元很重要 → 记住它”

“这个词元无关 → 忘记它”

“这个词元改变了含义 → 大力更新状态”
```

这也就是为什么它被称为 **选择性** 状态空间。

---

### 3. 这对大语言模型为什么有趣？

根本的权衡在于：

|                               | Transformer        | Mamba                    |
| ----------------------------- | ------------------ | ------------------------ |
| 核心机制                      | 注意力机制         | SSM                      |
| 训练时的序列交互              | O(L²) 注意力       | ~O(L)                    |
| 生成时的 KV 缓存              | 随上下文增长       | 更小/固定的状态          |
| 长上下文                      | 成本高昂           | 可能更便宜               |
| 对旧词元的随机访问            | 优秀               | 较弱                     |
| 成熟的生态                    | 优秀               | 较新                     |

真正有趣的部分是推理。

对于生成第 (t) 个词元的 Transformer，通常需要维护一个 **KV 缓存**：

```text
K₁ V₁
K₂ V₂
K₃ V₃
...
Kₜ Vₜ
```

缓存随着序列长度增长。

而 Mamba 可以维护一个概念上类似的东西：

```text
状态
  ↓
固定大小的记忆
  ↓
下一个词元
```

因此，它的循环状态不会随着上下文长度线性增长。

---

### 4. 为什么叫“Mamba”？

这个名字来源于 **黑曼巴蛇**。该架构在以下论文中提出：

**《Mamba: Linear-Time Sequence Modeling with Selective State Spaces》** 作者：Albert Gu 和 Tri Dao，2023年。

重要的概念贡献不在于名字，而在于：

```text
SSM
 ↓
输入依赖/选择性参数
 ↓
高效的循环状态
 ↓
线性时间序列建模
```

---

### 5. Mamba 并不仅仅是“RNN 2.0”

这是有趣的一点。

一个简单的 RNN：

```python
h = RNN(h, x)
```

在以下方面存在问题：

* 长距离依赖
* 梯度消失/爆炸
* 高效的并行训练

Mamba/SSM 的设计使得循环结构具有数学特性，允许 **训练时进行并行计算**，同时在推理时仍表现为循环模型。

因此你得到了一个有趣的混合体：

```text
训练时：

x₁ x₂ x₃ x₄ x₅ x₆
 └──── 并行硬件友好计算 ────┘


推理时：

x₁ → 状态 → x₂ → 状态 → x₃ → 状态 → ...
```

这也是 Mamba 从系统角度看起来有趣的原因之一。

---

### 6. 更深层的思考

我会这样概括 Transformer 与 Mamba 的区别：

**Transformer：**

> “给定这个词元，从整个序列中检索相关信息。”

**Mamba：**

> “在阅读序列的过程中，不断判断哪些信息值得留在我的状态里。”

因此，它们代表了两种不同的 **记忆** 方法。

```text
Transformer
    │
    └── 外部记忆 = 所有先前的 K/V
             ↓
       通过注意力检索


Mamba
    │
    └── 压缩记忆 = 隐藏状态
             ↓
       选择性更新状态
```

这也解释了 Mamba 的根本弱点：

**压缩可能会导致信息丢失。**

如果 20,000 个词元前的一个重要事实被错误地压缩到状态中，Mamba 就无法像 Transformer 那样简单地返回并检索原始词元。

注意力机制实际上是这样说的：

```text
“我会保留整个数据库并进行搜索。”
```

Mamba 是这样说的：

```text
“我会持续总结出重要内容。”
```

这可能是最有用的思维模型。

### 参考资料

* [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752?utm_source=chatgpt.com)
* [Mamba 官方 GitHub 仓库](https://github.com/state-spaces/mamba?utm_source=chatgpt.com)
* [Transformers: Attention Is All You Need](https://arxiv.org/abs/1706.03762?utm_source=chatgpt.com)
