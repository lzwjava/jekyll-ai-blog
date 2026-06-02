---
audio: false
generated: true
lang: zh
layout: post
title: 线性变换的核
translated: true
type: note
---

线性变换的**核**（kernel）是指所有被该变换映射到零向量的输入向量构成的集合。

### 定义

若 \\( T: V \to W \\) 是两个向量空间 \\( V \\) 和 \\( W \\) 之间的线性变换，则 \\( T \\) 的**核**（或**零空间**）为：

\\[
\ker(T) = \{ v \in V \mid T(v) = 0 \}
\\]

### 主要性质

1. **子空间**：线性变换的核始终是定义域 \\( V \\) 的一个子空间。
2. **维度**：核的维度称为该变换的**零度**（nullity）。
3. **与单射性的关系**：
   - 若 \\( \ker(T) = \{0\} \\)，则 \\( T \\) 是**单射**（一一映射）。
   - 若 \\( \ker(T) \\) 的维度大于零，则 \\( T \\) 不是单射。

### 示例

考虑矩阵变换 \\( T: \mathbb{R}^3 \to \mathbb{R}^2 \\)，定义为：

\\[
T(x, y, z) = (x + y, y + z)
\\]

将其表示为矩阵形式：

<div>
$$
T \begin{bmatrix} x \\ y \\ z \end{bmatrix} =
\begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \end{bmatrix}
\begin{bmatrix} x \\ y \\ z \end{bmatrix}
$$
</div>

为求核，解方程：

\\[
\begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \end{bmatrix}
\begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
\\]

得到方程组：

\\[
x + y = 0
\\]
\\[
y + z = 0
\\]

解出 \\( x, y, z \\)：

\\[
x = -y, \quad z = -y
\\]

因此，核由所有形如以下的向量组成：

<div>
$$
\ker(T) = \text{span} \left\{ \begin{bmatrix} -1 \\ 1 \\ -1 \end{bmatrix} \right\}
$$
</div>

这是 \\( \mathbb{R}^3 \\) 中的一个一维子空间。

如有任何疑问，欢迎随时提出！
