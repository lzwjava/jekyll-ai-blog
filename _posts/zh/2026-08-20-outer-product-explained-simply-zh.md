---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 外积通俗解释
translated: true
type: note
---

`torch.outer` 用于计算两个一维张量的**外积**。

问题：`torch.outer` 的含义是什么？

答案：

给定两个向量：

[
a = [a_1, a_2, ..., a_m]
]

[
b = [b_1, b_2, ..., b_n]
]

`torch.outer(a, b)` 会生成一个 (m \times n) 的矩阵：

[
A_{ij} = a_i \times b_j
]

示例：

```python
import torch

a = torch.tensor([1, 2, 3])
b = torch.tensor([10, 20])

c = torch.outer(a, b)

print(c)
```

输出：

```
tensor([
 [10, 20],
 [20, 40],
 [30, 60]
])
```

计算原理：

```
第1行: 1 * [10, 20] = [10, 20]
第2行: 2 * [10, 20] = [20, 40]
第3行: 3 * [10, 20] = [30, 60]
```

形状：

```python
a.shape  # [3]
b.shape  # [2]

torch.outer(a, b).shape  # [3, 2]
```

---

等价于以下写法：

```python
a[:, None] * b[None, :]
```

示例：

```python
torch.allclose(
    torch.outer(a, b),
    a[:, None] * b[None, :]
)
# True
```

这种广播机制的写法常用于神经网络中。

---

## 与线性代数的关系

外积与点积不同：

### 点积

两个向量 → 一个标量：

[
a \cdot b = \sum_i a_i b_i
]

示例：

```python
torch.dot(torch.tensor([1,2,3]), torch.tensor([4,5,6]))
```

返回：

```
32
```

---

### 外积

两个向量 → 矩阵：

[
a b^T
]

对于：

[
a=
\begin{bmatrix}
1\\2\\3
\end{bmatrix}
]

[
b=
\begin{bmatrix}
10\\20
\end{bmatrix}
]

得到：

[
ab^T=
\begin{bmatrix}
10&20\\
20&40\\
30&60
\end{bmatrix}
]

---

## 机器学习中的常见用途

### 1. 注意力机制 / 位置编码

某些注意力机制会创建成对交互：

```python
scores = torch.outer(q, k)
```

这将生成所有查询-键的组合。

---

### 2. 低秩矩阵

一个秩为1的矩阵：

[
W = uv^T
]

可以通过以下方式创建：

```python
W = torch.outer(u, v)
```

许多LoRA思想基于低秩更新：

[
\Delta W = BA
]

其中更新由较小的矩阵表示。

---

### 3. 协方差 / 统计

对于向量：

```python
x = torch.tensor([1.,2.,3.])

x.outer(x)
```

得到：

[
xx^T
]

这出现在协方差计算中。

---

在PyTorch源码中，如果看到：

```python
torch.outer(x, y)
```

可以理解为：

> "将x的每个元素与y的每个元素相乘，生成一个包含所有成对乘积的矩阵。"