---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RoPE：分离旋转产生相对位置
translated: true
type: note
---

让我们深入探讨。最令人困惑的部分是**为什么分别旋转 Q 和 K 能让注意力分数变成相对位置**。

这是 RoPE 的核心数学技巧。

---

# 1. 从普通注意力开始

Transformer 注意力：

\[
\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt d}\right)V
\]

关键部分：

\[
QK^T
\]

实际上就是一个点积。

示例：

```
Query token:
Q = [0.8, 0.2]

Key token:
K = [0.5, 0.9]

分数：
Q · K
= 0.8*0.5 + 0.2*0.9
= 0.58
```

点积越大，注意力越多。

---

# 2. 问题所在

假设：

```
"The cat eats fish"
```

位置：

```
The     cat     eats     fish
 0       1        2        3
```

当 `eats` 关注 `cat` 时：

```
query 位置：
m = 2

key 位置：
n = 1
```

模型应该知道：

```
cat 在 eats 前一个 token
距离 = -1
```

但普通注意力只看到：

```
Q 向量
K 向量
```

没有任何位置信息。

---

# 3. 思路：将位置编码到向量本身

不再使用：

```
Q

K
```

而是创建：

```
位置 2：
Q 旋转角度 2θ

位置 1：
K 旋转角度 1θ
```

于是：

\[
Q' = R(2\theta) Q
\]
\[
K' = R(1\theta) K
\]

注意力变为：

\[
Q'^T K'
\]

即：

\[
(R(2\theta) Q)^T (R(\theta) K)
\]

---

# 4. 理解旋转

一个二维向量：

```
        y
        |
        |
        *
       /
      /
-----*---------- x
```

假设：

\[
q = [1, 0]
\]

它指向右方。

角度：

```
0 度
```

---

旋转 90 度：

\[
R(90^\circ)
\]

现在：

```
        *
        |
        |
        |
--------+--------
```

向量变为：

\[
[0, 1]

```

---

旋转矩阵：

\[
R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}
\]

乘法：

\[
R(\theta) \begin{bmatrix} x \\ y \end{bmatrix}
\]

示例：

\[
\theta = 90^\circ
\]

因为：

\[
\cos 90 = 0, \quad \sin 90 = 1
\]

我们得到：

\[
\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}
\]

---

# 5. 神奇的性质

现在进入关键部分。

假设：

Query 位置：

\[
m
\]

Key 位置：

\[
n
\]

RoPE 的做法：

\[
Q' = R(m\theta) q
\]
\[
K' = R(n\theta) k
\]

注意力：

\[
Q'^T K'
\]

代入：

\[
(R(m\theta) q)^T (R(n\theta) k)
\]

转置规则：

\[
(AB)^T = B^T A^T
\]

所以：

\[
q^T R(m\theta)^T R(n\theta) k
\]

对于旋转矩阵：

\[
R(\theta)^T = R(-\theta)
\]

因此：

\[
q^T R(-m\theta) R(n\theta) k
\]

旋转复合：

\[
R(a) R(b) = R(a+b)
\]

因此：

\[
q^T R((n-m)\theta) k
\]

这就是神奇之处。

---

# 6. 什么消失了？

之前：

\[
R(m\theta), \quad R(n\theta)
\]

我们有：

```

query 位置 = m
key 位置 = n

```

两个绝对位置。

简化之后：

\[
R((n-m)\theta)
\]

只剩下：

```

距离 = n - m

```

---

示例：

句子：

```

I love machine learning

```

位置：

```

I       love       machine      learning
 0        1            2            3

```

Query：

```

learning
m = 3

```

Key：

```

machine
n = 2

```

相对距离：

\[
n - m = 2 - 3 = -1
\]

RoPE 注意力看到：

```

-1

```

而不是：

```

位置 3
位置 2

```

---

# 7. 为什么用旋转而不是加向量？

对比：

## 旧的位置嵌入

```

token 向量
[0.3, 0.7]
+
位置向量
[0.1, 0.2]
=

[0.4, 0.9]

```

位置和语义混在一起。

---

## RoPE

原始：

```

语义向量：
空间方向

```

位置：

```

旋转方向

```

示例：

```

相同单词："cat"

```

不同位置：

```

cat 在位置 1：
   /

cat 在位置 100：
       \

```

相同的语义向量，不同的角度。

---

# 8. 扩展到 4096 维

一个真实 LLM 的向量：

```

hidden state：
[
x0,
x1,
x2,
x3,
...
x4095
]

```

RoPE 对维度进行分组：

```

(x0, x1)
(x2, x3)
(x4, x5)
...
(x4094, x4095)

```

每一对是一个二维向量。

示例：

```

pair 0：
[x0, x1]
旋转 θ0

pair 1：
[x2, x3]
旋转 θ1

pair 2：
[x4, x5]
旋转 θ2

```

不同频率：

```

pair 0：
快速旋转

pair 100：
慢速旋转

```

类似于傅里叶变换。

---

# 9. 为什么需要多个频率？

想象一个时钟。

快速时钟：

```

0 1 2 3 4 5 ...

```

对附近位置有用。

慢速时钟：

```

0 ........ 100 ........ 200

```

对长距离有用。

LLM 两者都需要：

示例：

```

"The cat sat on the mat"

cat -> sat
距离 1

"The cat ......... animal"

cat -> animal
距离 20

```

不同维度捕捉不同尺度。

---

# 10. 完整心智模型

把 RoPE 想象成这样：

```

Token 含义
      |
      v
向量方向

位置
      |
      v
旋转角度

Q：
含义 + 位置旋转

K：
含义 + 位置旋转

注意力：
比较两个旋转后的向量

角度差：
n - m

因此：
相对位置

```

整个 RoPE 论文基本上就是这一个数学发现：

\[
\boxed{
(R_m q)^T (R_n k) = q^T R_{n-m} k
}
\]

对注意力来说是一个非常小的改变，但它解决了现代长上下文 LLM 的位置编码问题。
