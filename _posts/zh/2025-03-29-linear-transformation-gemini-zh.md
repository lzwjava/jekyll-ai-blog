---
audio: false
generated: true
lang: zh
layout: post
title: 线性变换 - Gemini
translated: true
type: note
---

好的，让我们深入探讨线性变换的详细教程，涵盖定义、示例、矩阵表示、核、像以及单射和满射等性质。这是线性代数中的一个基础主题。

## 6. 线性变换：详细教程

**线性变换** 是两个向量空间之间的一种函数，它保持向量加法和标量乘法运算。设 \\(V\\) 和 \\(W\\) 是同一域 \\(F\\)（通常是实数集 \\(\mathbb{R}\\) 或复数集 \\(\mathbb{C}\\)）上的向量空间。

**定义：** 函数 \\(T: V \rightarrow W\\) 是一个线性变换，如果它满足以下两个性质，对于所有向量 \\(\mathbf{u}, \mathbf{v} \in V\\) 和所有标量 \\(c \in F\\)：

1. **可加性：** \\(T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})\\)
2. **齐次性（标量乘法）：** \\(T(c\mathbf{u}) = cT(\mathbf{u})\\)

这两个性质可以合并为一个条件：
对于所有 \\(\mathbf{u}, \mathbf{v} \in V\\) 和所有标量 \\(c, d \in F\\)，有 \\(T(c\mathbf{u} + d\mathbf{v}) = cT(\mathbf{u}) + dT(\mathbf{v})\\)。

**线性的关键推论：**

* \\(T(\mathbf{0}_V) = \mathbf{0}_W\\)，其中 \\(\mathbf{0}_V\\) 是 \\(V\\) 中的零向量，\\(\mathbf{0}_W\\) 是 \\(W\\) 中的零向量。（证明：对于任意 \\(\mathbf{u} \in V\\)，有 \\(T(\mathbf{0}_V) = T(0\mathbf{u}) = 0T(\mathbf{u}) = \mathbf{0}_W\\)）。
* \\(T(-\mathbf{u}) = -T(\mathbf{u})\\)。（证明：\\(T(-\mathbf{u}) = T((-1)\mathbf{u}) = (-1)T(\mathbf{u}) = -T(\mathbf{u})\\)）。

### 线性变换示例

让我们看一些例子来更好地理解这个概念。

**示例 1：\\(\mathbb{R}^2\\) 中的变换（旋转）**

考虑一个变换 \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^2\\)，它将 \\(\mathbb{R}^2\\) 中的每个向量绕原点逆时针旋转一个角度 \\(\theta\\)。如果 \\(\mathbf{v} = \begin{pmatrix} x \\ y \end{pmatrix}\\)，那么 \\(T(\mathbf{v}) = \begin{pmatrix} x\cos\theta - y\sin\theta \\ x\sin\theta + y\cos\theta \end{pmatrix}\\)。

让我们检查这是否是线性变换。设 \\(\mathbf{u} = \begin{pmatrix} x_1 \\ y_1 \end{pmatrix}\\) 和 \\(\mathbf{v} = \begin{pmatrix} x_2 \\ y_2 \end{pmatrix}\\)，并设 \\(c\\) 为一个标量。

* **可加性：**
    \\(T(\mathbf{u} + \mathbf{v}) = T\left(\begin{pmatrix} x_1 + x_2 \\ y_1 + y_2 \end{pmatrix}\right) = \begin{pmatrix} (x_1 + x_2)\cos\theta - (y_1 + y_2)\sin\theta \\ (x_1 + x_2)\sin\theta + (y_1 + y_2)\cos\theta \end{pmatrix}\\)
    \\(= \begin{pmatrix} (x_1\cos\theta - y_1\sin\theta) + (x_2\cos\theta - y_2\sin\theta) \\ (x_1\sin\theta + y_1\cos\theta) + (x_2\sin\theta + y_2\cos\theta) \end{pmatrix} = T(\mathbf{u}) + T(\mathbf{v})\\)

* **齐次性：**
    \\(T(c\mathbf{u}) = T\left(\begin{pmatrix} cx_1 \\ cy_1 \end{pmatrix}\right) = \begin{pmatrix} (cx_1)\cos\theta - (cy_1)\sin\theta \\ (cx_1)\sin\theta + (cy_1)\cos\theta \end{pmatrix}\\)
    \\(= \begin{pmatrix} c(x_1\cos\theta - y_1\sin\theta) \\ c(x_1\sin\theta + y_1\cos\theta) \end{pmatrix} = c \begin{pmatrix} x_1\cos\theta - y_1\sin\theta \\ x_1\sin\theta + y_1\cos\theta \end{pmatrix} = cT(\mathbf{u})\\)

因此，旋转是一个线性变换。

**示例 2：\\(\mathbb{R}^2\\) 中的变换（投影到 x 轴）**

考虑 \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^2\\) 定义为 \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x \\ 0 \end{pmatrix}\\)。这个变换将每个向量投影到 x 轴上。您可以使用定义验证这也是一个线性变换。

**示例 3：\\(\mathbb{R}^2\\) 中的变换（平移）**

考虑 \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^2\\) 定义为 \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + a \\ y + b \end{pmatrix}\\)，其中 \\(a\\) 和 \\(b\\) 是常数（不同时为零）。

让我们检查第一个性质：
\\(T(\mathbf{u} + \mathbf{v}) = T\left(\begin{pmatrix} x_1 + x_2 \\ y_1 + y_2 \end{pmatrix}\right) = \begin{pmatrix} (x_1 + x_2) + a \\ (y_1 + y_2) + b \end{pmatrix} = \begin{pmatrix} x_1 + a + x_2 + a \\ y_1 + b + y_2 + b \end{pmatrix}\\)
\\(T(\mathbf{u}) + T(\mathbf{v}) = \begin{pmatrix} x_1 + a \\ y_1 + b \end{pmatrix} + \begin{pmatrix} x_2 + a \\ y_2 + b \end{pmatrix} = \begin{pmatrix} x_1 + a + x_2 + a \\ y_1 + b + y_2 + b \end{pmatrix}\\)

这看起来正确，让我们重新检查。
\\(T(\mathbf{u} + \mathbf{v}) = \begin{pmatrix} x_1 + x_2 + a \\ y_1 + y_2 + b \end{pmatrix}\\)
\\(T(\mathbf{u}) + T(\mathbf{v}) = \begin{pmatrix} x_1 + a \\ y_1 + b \end{pmatrix} + \begin{pmatrix} x_2 + a \\ y_2 + b \end{pmatrix} = \begin{pmatrix} x_1 + x_2 + 2a \\ y_1 + y_2 + 2b \end{pmatrix}\\)

如果 \\(a \neq 0\\) 或 \\(b \neq 0\\)，那么 \\(T(\mathbf{u} + \mathbf{v}) \neq T(\mathbf{u}) + T(\mathbf{v})\\)。此外，\\(T(\mathbf{0}) = T\left(\begin{pmatrix} 0 \\ 0 \end{pmatrix}\right) = \begin{pmatrix} a \\ b \end{pmatrix} \neq \begin{pmatrix} 0 \\ 0 \end{pmatrix}\\) 如果 \\(a\\) 或 \\(b\\) 非零。因此，平移通常**不是**线性变换。

**示例 4：由矩阵定义的从 \\(\mathbb{R}^n\\) 到 \\(\mathbb{R}^m\\) 的变换**

设 \\(A\\) 是一个 \\(m \times n\\) 矩阵。变换 \\(T: \mathbb{R}^n \rightarrow \mathbb{R}^m\\) 定义为 \\(T(\mathbf{x}) = A\mathbf{x}\\)（其中 \\(\mathbf{x}\\) 是一个 \\(n \times 1\\) 列向量）是一个线性变换。这是因为矩阵乘法满足可加性和齐次性：
\\(A(\mathbf{u} + \mathbf{v}) = A\mathbf{u} + A\mathbf{v}\\)
\\(A(c\mathbf{u}) = c(A\mathbf{u})\\)

**示例 5：多项式的微分**

设 \\(P_n\\) 是次数最多为 \\(n\\) 的多项式向量空间。变换 \\(D: P_n \rightarrow P_{n-1}\\) 定义为 \\(D(p(x)) = p'(x)\\)（\\(p(x)\\) 的导数）是一个线性变换。
如果 \\(p(x)\\) 和 \\(q(x)\\) 是多项式，\\(c\\) 是一个标量：
\\(D(p(x) + q(x)) = (p(x) + q(x))' = p'(x) + q'(x) = D(p(x)) + D(q(x))\\)
\\(D(cp(x)) = (cp(x))' = cp'(x) = cD(p(x))\\)

**示例 6：函数的积分**

设 \\(C[a, b]\\) 是区间 \\([a, b]\\) 上连续函数的向量空间。变换 \\(I: C[a, b] \rightarrow \mathbb{R}\\) 定义为 \\(I(f) = \int_a^b f(x) dx\\) 是一个线性变换。
\\(I(f + g) = \int_a^b (f(x) + g(x)) dx = \int_a^b f(x) dx + \int_a^b g(x) dx = I(f) + I(g)\\)
\\(I(cf) = \int_a^b cf(x) dx = c \int_a^b f(x) dx = cI(f)\\)

### 线性变换的矩阵表示

线性代数的一个基本结果是，任何有限维向量空间之间的线性变换都可以用矩阵表示。

设 \\(V\\) 是一个 \\(n\\) 维向量空间，基为 \\(\mathcal{B} = \{\mathbf{b}_1, \mathbf{b}_2, ..., \mathbf{b}_n\}\\)，\\(W\\) 是一个 \\(m\\) 维向量空间，基为 \\(\mathcal{C} = \{\mathbf{c}_1, \mathbf{c}_2, ..., \mathbf{c}_m\}\\)。设 \\(T: V \rightarrow W\\) 是一个线性变换。

为了找到 \\(T\\) 关于基 \\(\mathcal{B}\\) 和 \\(\mathcal{C}\\) 的矩阵表示（记为 \\([T]_{\mathcal{B}}^{\mathcal{C}}\\)，或者当基明确时简记为 \\([T]\\)），我们需要确定 \\(V\\) 的基向量在 \\(T\\) 下的像，并将这些像表示为 \\(W\\) 的基向量的线性组合。

对于每个 \\(\mathbf{b}_j \in \mathcal{B}\\)，\\(T(\mathbf{b}_j)\\) 是 \\(W\\) 中的一个向量，因此它可以唯一地写成 \\(\mathcal{C}\\) 中基向量的线性组合：
\\(T(\mathbf{b}_j) = a_{1j}\mathbf{c}_1 + a_{2j}\mathbf{c}_2 + ... + a_{mj}\mathbf{c}_m = \sum_{i=1}^{m} a_{ij}\mathbf{c}_i\\)

这个线性组合的系数构成了矩阵表示 \\([T]_{\mathcal{B}}^{\mathcal{C}}\\) 的第 \\(j\\) 列：
$[T]_{\mathcal{B}}^{\mathcal{C}} = \begin{pmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{pmatrix}$

如果 \\(\mathbf{v} \in V\\) 关于基 \\(\mathcal{B}\\) 的坐标向量为 \\([\mathbf{v}]_{\mathcal{B}} = \begin{pmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{pmatrix}\\)，那么 \\(T(\mathbf{v})\\) 关于基 \\(\mathcal{C}\\) 的坐标向量，记为 \\([T(\mathbf{v})]_{\mathcal{C}}\\)，由矩阵乘积给出：
\\([T(\mathbf{v})]_{\mathcal{C}} = [T]_{\mathcal{B}}^{\mathcal{C}} [\mathbf{v}]_{\mathcal{B}}\\)

**示例：矩阵表示**

设 \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^3\\) 是一个线性变换，定义为 \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\)。设 \\(\mathbb{R}^2\\) 和 \\(\mathbb{R}^3\\) 的标准基分别为 \\(\mathcal{B} = \{\mathbf{e}_1, \mathbf{e}_2\} = \left\{ \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \begin{pmatrix} 0 \\ 1 \end{pmatrix} \right\}\\) 和 \\(\mathcal{C} = \{\mathbf{f}_1, \mathbf{f}_2, \mathbf{f}_3\} = \left\{ \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix}, \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}, \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix} \right\}\\)。

我们找到 \\(\mathbb{R}^2\\) 的基向量在 \\(T\\) 下的像：
\\(T(\mathbf{e}_1) = T\left(\begin{pmatrix} 1 \\ 0 \end{pmatrix}\right) = \begin{pmatrix} 1 + 0 \\ 2(1) - 0 \\ 3(0) \end{pmatrix} = \begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix} = 1\mathbf{f}_1 + 2\mathbf{f}_2 + 0\mathbf{f}_3\\)
\\(T(\mathbf{e}_2) = T\left(\begin{pmatrix} 0 \\ 1 \end{pmatrix}\right) = \begin{pmatrix} 0 + 1 \\ 2(0) - 1 \\ 3(1) \end{pmatrix} = \begin{pmatrix} 1 \\ -1 \\ 3 \end{pmatrix} = 1\mathbf{f}_1 - 1\mathbf{f}_2 + 3\mathbf{f}_3\\)

\\(T\\) 关于标准基的矩阵表示为：
\\([T]_{\mathcal{B}}^{\mathcal{C}} = \begin{pmatrix} 1 & 1 \\ 2 & -1 \\ 0 & 3 \end{pmatrix}\\)

现在，取 \\(\mathbb{R}^2\\) 中的任意向量 \\(\mathbf{v} = \begin{pmatrix} x \\ y \end{pmatrix}\\)。它关于 \\(\mathcal{B}\\) 的坐标向量是 \\([\mathbf{v}]_{\mathcal{B}} = \begin{pmatrix} x \\ y \end{pmatrix}\\)。
\\([T(\mathbf{v})]_{\mathcal{C}} = [T]_{\mathcal{B}}^{\mathcal{C}} [\mathbf{v}]_{\mathcal{B}} = \begin{pmatrix} 1 & 1 \\ 2 & -1 \\ 0 & 3 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\)
关于 \\(\mathcal{C}\\) 的坐标向量确实是 \\(\begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\)，这对应于我们之前定义的向量 \\(T(\mathbf{v})\\)。

### 线性变换的核（零空间）

线性变换 \\(T: V \rightarrow W\\) 的**核**（或零空间），记为 \\(\text{ker}(T)\\) 或 \\(N(T)\\)，是 \\(V\\) 中所有被映射到 \\(W\\) 中零向量的向量的集合：
\\(\text{ker}(T) = \{\mathbf{v} \in V \mid T(\mathbf{v}) = \mathbf{0}_W\}\\)

**核的性质：**

* 线性变换的核始终是定义域 \\(V\\) 的一个子空间。
  * **包含零向量：** \\(T(\mathbf{0}_V) = \mathbf{0}_W\\)，所以 \\(\mathbf{0}_V \in \text{ker}(T)\\)。
  * **对加法封闭：** 如果 \\(\mathbf{u}, \mathbf{v} \in \text{ker}(T)\\)，那么 \\(T(\mathbf{u}) = \mathbf{0}_W\\) 且 \\(T(\mathbf{v}) = \mathbf{0}_W\\)。因此，\\(T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v}) = \mathbf{0}_W + \mathbf{0}_W = \mathbf{0}_W\\)，所以 \\(\mathbf{u} + \mathbf{v} \in \text{ker}(T)\\)。
  * **对标量乘法封闭：** 如果 \\(\mathbf{u} \in \text{ker}(T)\\) 且 \\(c\\) 是一个标量，那么 \\(T(c\mathbf{u}) = cT(\mathbf{u}) = c\mathbf{0}_W = \mathbf{0}_W\\)，所以 \\(c\mathbf{u} \in \text{ker}(T)\\)。

**示例：求核**

考虑线性变换 \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^3\\) 定义为 \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\)。
为了求核，我们需要解 \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}\\)：
\\(\begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}\\)

这给出线性方程组：
\\(x + y = 0\\)
\\(2x - y = 0\\)
\\(3y = 0\\)

从第三个方程，\\(y = 0\\)。将其代入第一个方程，\\(x + 0 = 0\\)，所以 \\(x = 0\\)。第二个方程也满足：\\(2(0) - 0 = 0\\)。
唯一解是 \\(x = 0\\) 和 \\(y = 0\\)。因此，\\(\text{ker}(T) = \left\{ \begin{pmatrix} 0 \\ 0 \end{pmatrix} \right\}\\)，即 \\(\mathbb{R}^2\\) 的零子空间。

### 线性变换的像（值域）

线性变换 \\(T: V \rightarrow W\\) 的**像**（或值域），记为 \\(\text{im}(T)\\) 或 \\(R(T)\\)，是 \\(W\\) 中所有是 \\(V\\) 中某个向量的像的向量的集合：
\\(\text{im}(T) = \{\mathbf{w} \in W \mid \mathbf{w} = T(\mathbf{v}) \text{ 对于某个 } \mathbf{v} \in V\}\\)

**像的性质：**

* 线性变换的像始终是陪域 \\(W\\) 的一个子空间。
  * **包含零向量：** \\(T(\mathbf{0}_V) = \mathbf{0}_W\\)，所以 \\(\mathbf{0}_W \in \text{im}(T)\\)。
  * **对加法封闭：** 如果 \\(\mathbf{w}_1, \mathbf{w}_2 \in \text{im}(T)\\)，那么存在 \\(\mathbf{v}_1, \mathbf{v}_2 \in V\\) 使得 \\(T(\mathbf{v}_1) = \mathbf{w}_1\\) 和 \\(T(\mathbf{v}_2) = \mathbf{w}_2\\)。那么 \\(\mathbf{w}_1 + \mathbf{w}_2 = T(\mathbf{v}_1) + T(\mathbf{v}_2) = T(\mathbf{v}_1 + \mathbf{v}_2)\\)。由于 \\(\mathbf{v}_1 + \mathbf{v}_2 \in V\\)，所以 \\(\mathbf{w}_1 + \mathbf{w}_2 \in \text{im}(T)\\)。
  * **对标量乘法封闭：** 如果 \\(\mathbf{w} \in \text{im}(T)\\) 且 \\(c\\) 是一个标量，那么存在 \\(\mathbf{v} \in V\\) 使得 \\(T(\mathbf{v}) = \mathbf{w}\\)。那么 \\(c\mathbf{w} = cT(\mathbf{v}) = T(c\mathbf{v})\\)。由于 \\(c\mathbf{v} \in V\\)，所以 \\(c\mathbf{w} \in \text{im}(T)\\)。

* 如果 \\(V\\) 是有限维的，且有一组基 \\(\{\mathbf{b}_1, \mathbf{b}_2, ..., \mathbf{b}_n\}\\)，那么 \\(T\\) 的像是基向量像的张成空间：
    \\(\text{im}(T) = \text{span}\{T(\mathbf{b}_1), T(\mathbf{b}_2), ..., T(\mathbf{b}_n)\}\\)

**示例：求像**

考虑线性变换 \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^3\\) 定义为 \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\)。
使用 \\(\mathbb{R}^2\\) 的标准基 \\(\{\begin{pmatrix} 1 \\ 0 \end{pmatrix}, \begin{pmatrix} 0 \\ 1 \end{pmatrix}\}\\)，我们有：
\\(T\left(\begin{pmatrix} 1 \\ 0 \end{pmatrix}\right) = \begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix}\\)
\\(T\left(\begin{pmatrix} 0 \\ 1 \end{pmatrix}\right) = \begin{pmatrix} 1 \\ -1 \\ 3 \end{pmatrix}\\)

\\(T\\) 的像是这两个向量的张成空间：
\\(\text{im}(T) = \text{span}\left\{ \begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix}, \begin{pmatrix} 1 \\ -1 \\ 3 \end{pmatrix} \right\}\\)
这是 \\(\mathbb{R}^3\\) 的一个子空间。由于这两个向量线性无关（一个不是另一个的标量倍数），该像是 \\(\mathbb{R}^3\\) 中通过原点的平面。

**矩阵表示与像之间的关系：**

如果 \\(T: \mathbb{R}^n \rightarrow \mathbb{R}^m\\) 由 \\(T(\mathbf{x}) = A\mathbf{x}\\) 给出，其中 \\(A\\) 是一个 \\(m \times n\\) 矩阵，那么 \\(T\\) 的像是矩阵 \\(A\\) 的列空间，即 \\(A\\) 的列向量的张成空间。

### 线性变换的性质：单射性和满射性

**单射性（一对一）**

线性变换 \\(T: V \rightarrow W\\) 是**单射**（或一对一的），如果对于每个 \\(\mathbf{w} \in W\\)，至多存在一个 \\(\mathbf{v} \in V\\) 使得 \\(T(\mathbf{v}) = \mathbf{w}\\)。等价地，如果 \\(T(\mathbf{u}) = T(\mathbf{v})\\)，那么 \\(\mathbf{u} = \mathbf{v}\\)。

**定理：** 线性变换 \\(T: V \rightarrow W\\) 是单射的，当且仅当其核是零子空间，即 \\(\text{ker}(T) = \{\mathbf{0}_V\}\\)。

**证明：**

* **(\\(\Rightarrow\\)) 假设 \\(T\\) 是单射。** 如果 \\(\mathbf{v} \in \text{ker}(T)\\)，那么 \\(T(\mathbf{v}) = \mathbf{0}_W\\)。我们也知道 \\(T(\mathbf{0}_V) = \mathbf{0}_W\\)。由于 \\(T\\) 是单射且 \\(T(\mathbf{v}) = T(\mathbf{0}_V)\\)，必须有 \\(\mathbf{v} = \mathbf{0}_V\\)。因此，\\(\text{ker}(T) = \{\mathbf{0}_V\}\\)。
* **(\\(\Leftarrow\\)) 假设 \\(\text{ker}(T) = \{\mathbf{0}_V\}\\)。** 假设对于某个 \\(\mathbf{u}, \mathbf{v} \in V\\)，有 \\(T(\mathbf{u}) = T(\mathbf{v})\\)。那么 \\(T(\mathbf{u}) - T(\mathbf{v}) = \mathbf{0}_W\\)。由线性性，\\(T(\mathbf{u} - \mathbf{v}) = \mathbf{0}_W\\)。这意味着 \\(\mathbf{u} - \mathbf{v} \in \text{ker}(T)\\)。由于 \\(\text{ker}(T) = \{\mathbf{0}_V\}\\)，我们有 \\(\mathbf{u} - \mathbf{v} = \mathbf{0}_V\\)，这意味着 \\(\mathbf{u} = \mathbf{v}\\)。因此，\\(T\\) 是单射。

**示例：检查单射性**

对于变换 \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^3\\) 定义为 \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\)，我们发现 \\(\text{ker}(T) = \left\{ \begin{pmatrix} 0 \\ 0 \end{pmatrix} \right\}\\)。因此，这个变换是单射。

**满射性（映上）**

线性变换 \\(T: V \rightarrow W\\) 是**满射**（或映上的），如果对于每个 \\(\mathbf{w} \in W\\)，存在至少一个 \\(\mathbf{v} \in V\\) 使得 \\(T(\mathbf{v}) = \mathbf{w}\\)。换句话说，\\(T\\) 的像等于陪域 \\(W\\)，即 \\(\text{im}(T) = W\\)。

**定理（秩-零化度定理）：** 对于线性变换 \\(T: V \rightarrow W\\)，其中 \\(V\\) 是有限维向量空间，
\\(\text{dim}(\text{ker}(T)) + \text{dim}(\text{im}(T)) = \text{dim}(V)\\)
这里，\\(\text{dim}(\text{ker}(T))\\) 称为 \\(T\\) 的**零化度**，\\(\text{dim}(\text{im}(T))\\) 称为 \\(T\\) 的**秩**。

**满射性与维数之间的关系：**

如果 \\(T: V \rightarrow W\\) 是有限维向量空间之间的线性变换，那么：

* 如果 \\(\text{dim}(V) < \text{dim}(W)\\)，则 \\(T\\) 不可能是满射。（根据秩-零化度定理，\\(\text{dim}(\text{im}(T)) \leq \text{dim}(V) < \text{dim}(W)\\)）。
* 如果 \\(\text{dim}(V) > \text{dim}(W)\\)，则 \\(T\\) 不可能是单射（因为 \\(\text{dim}(\text{ker}(T)) = \text{dim}(V) - \text{dim}(\text{im}(T)) \geq \text{dim}(V) - \text{dim}(W) > 0\\)，所以核不仅仅是零向量）。
* 如果 \\(\text{dim}(V) = \text{dim}(W)\\)，则 \\(T\\) 是单射当且仅当它是满射。（如果 \\(T\\) 是单射，则 \\(\text{dim}(\text{ker}(T)) = 0\\)，所以 \\(\text{dim}(\text{im}(T)) = \text{dim}(V) = \text{dim}(W)\\)，意味着 \\(\text{im}(T) = W\\)，所以 \\(T\\) 是满射。反之，如果 \\(T\\) 是满射，则 \\(\text{dim}(\text{im}(T)) = \text{dim}(W) = \text{dim}(V)\\)，所以 \\(\text{dim}(\text{ker}(T)) = 0\\)，意味着 \\(T\\) 是单射）。

**示例：检查满射性**

对于变换 \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^3\\) 定义为 \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\)，我们发现 \\(\text{im}(T) = \text{span}\left\{ \begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix}, \begin{pmatrix} 1 \\ -1 \\ 3 \end{pmatrix} \right\}\\)。像的维数（\\(T\\) 的秩）是 2，因为这两个生成向量线性无关。定义域的维数是 \\(\text{dim}(\mathbb{R}^2) = 2\\)。根据秩-零化度定理，\\(\text{dim}(\text{ker}(T)) + \text{dim}(\text{im}(T)) = 2\\)，所以 \\(\text{dim}(\text{ker}(T)) + 2 = 2\\)，得出 \\(\text{dim}(\text{ker}(T)) = 0\\)，与我们之前的发现一致。

由于像的维数 (2) 小于陪域的维数 (3)，该像是陪域的一个真子空间，因此该变换不是满射。在 \\(\mathbb{R}^3\\) 中存在不在 \\(T\\) 的像中的向量。例如，\\(\begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}\\) 不能表示为 \\(\begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix}\\) 和 \\(\begin{pmatrix} 1 \\ -1 \\ 3 \end{pmatrix}\\) 的线性组合。

**同构**

线性变换 \\(T: V \rightarrow W\\) 被称为**同构**，如果它既是单射又是满射。如果两个向量空间 \\(V\\) 和 \\(W\\) 之间存在一个同构，则称 \\(V\\) 和 \\(W\\) 是**同构的**，记为 \\(V \cong W\\)。同构的向量空间具有本质上相同的代数结构。

对于有限维向量空间，两个向量空间是同构的当且仅当它们具有相同的维数。如果 \\(\text{dim}(V) = \text{dim}(W) = n\\)，那么线性变换 \\(T: V \rightarrow W\\) 是同构当且仅当它是单射或满射。

**关键概念总结：**

* **线性变换：** 向量空间之间保持向量加法和标量乘法的函数。
* **矩阵表示：** 将有限维向量空间之间的线性变换表示为矩阵的一种方式。
* **核（零空间）：** 定义域中被映射到陪域中零向量的向量集合。它是定义域的一个子空间。
* **像（值域）：** 陪域中是定义域中某个向量的像的向量集合。它是陪域的一个子空间。
* **单射性（一对一）：** 线性变换是单射的当且仅当其核是零子空间。
* **满射性（映上）：** 线性变换是满射的当且仅当其像等于陪域。
* **秩-零化度定理：** 对于线性变换 \\(T: V \rightarrow W\\) 且 \\(V\\) 是有限维的，有 \\(\text{dim}(\text{ker}(T)) + \text{dim}(\text{im}(T)) = \text{dim}(V)\\)。
* **同构：** 既是单射又是满射的线性变换。

这个详细的教程应该为理解线性变换提供了坚实的基础。记得练习各种例子来巩固你对这些概念的理解。祝您学习顺利！
