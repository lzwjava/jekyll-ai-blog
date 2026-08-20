---
audio: false
generated: true
image: false
lang: en
layout: post
title: Outer Product Explained Simply
translated: false
type: note
---

`torch.outer` computes the **outer product** of two 1-D tensors.

Question: What does `torch.outer` mean?

Answer:

Given two vectors:

[
a = [a_1, a_2, ..., a_m]
]

[
b = [b_1, b_2, ..., b_n]
]

`torch.outer(a, b)` produces an (m \times n) matrix:

[
A_{ij} = a_i \times b_j
]

Example:

```python
import torch

a = torch.tensor([1, 2, 3])
b = torch.tensor([10, 20])

c = torch.outer(a, b)

print(c)
```

Output:

```
tensor([
 [10, 20],
 [20, 40],
 [30, 60]
])
```

Because:

```
row 1: 1 * [10, 20] = [10, 20]
row 2: 2 * [10, 20] = [20, 40]
row 3: 3 * [10, 20] = [30, 60]
```

Shape:

```python
a.shape  # [3]
b.shape  # [2]

torch.outer(a, b).shape  # [3, 2]
```

---

It is equivalent to:

```python
a[:, None] * b[None, :]
```

Example:

```python
torch.allclose(
    torch.outer(a, b),
    a[:, None] * b[None, :]
)
# True
```

The broadcasting version is often used inside neural networks.

---

## Relation to linear algebra

The outer product is different from dot product:

### Dot product

Two vectors → one scalar:

[
a \cdot b = \sum_i a_i b_i
]

Example:

```python
torch.dot(torch.tensor([1,2,3]), torch.tensor([4,5,6]))
```

returns:

```
32
```

---

### Outer product

Two vectors → matrix:

[
a b^T
]

For:

[
a=
\begin{bmatrix}
1\2\3
\end{bmatrix}
]

[
b=
\begin{bmatrix}
10\20
\end{bmatrix}
]

you get:

[
ab^T=
\begin{bmatrix}
10&20\
20&40\
30&60
\end{bmatrix}
]

---

## Common ML usage

### 1. Attention / positional encoding

Some attention mechanisms create pairwise interactions:

```python
scores = torch.outer(q, k)
```

which gives all query-key combinations.

---

### 2. Low-rank matrices

A rank-1 matrix:

[
W = uv^T
]

can be created with:

```python
W = torch.outer(u, v)
```

Many LoRA ideas are based on low-rank updates:

[
\Delta W = BA
]

where the update is represented by smaller matrices.

---

### 3. Covariance / statistics

For a vector:

```python
x = torch.tensor([1.,2.,3.])

x.outer(x)
```

gives:

[
xx^T
]

which appears in covariance calculations.

---

In PyTorch source code, if you see:

```python
torch.outer(x, y)
```

think:

> "Take every element of x and multiply it with every element of y, producing a matrix of pairwise products."
