---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: NumPy线性代数速查指南
translated: true
type: note
---

作为你专注于工程实践的辅导指南，本文在先前显式索引公式的基础上，通过整合实用的NumPy演示（使用`import numpy as np`和`np.linalg`）进行扩展。所有数学内容仍可通过索引验证（例如，\\( A = [a_{ij}]_{i=1}^2, j=1^2 \\)）；代码使用显式数组以确保清晰度。输出结果均来自已验证的执行（例如，对于\\( A = \begin{pmatrix} a_{11}=1 & a_{12}=2 \\ a_{21}=3 & a_{22}=4 \end{pmatrix} \\)，\\( B = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix} \\)）。在备考时，可利用这些进行快速计算——重点在于对照公式解读输出结果。

## 1. 矩阵运算

数学公式如前：\\( (AB)_{ij} = \sum_{k=1}^2 a_{ik} b_{kj} \\)，等等。

**NumPy 演示**：

```python
import numpy as np
A = np.array([[1, 2], [3, 4]], dtype=float)
B = np.array([[5, 6], [7, 8]], dtype=float)
```

- 加法：`A + B` 得到 \\( \begin{pmatrix} 6 & 8 \\ 10 & 12 \end{pmatrix} \\)（逐元素 \\( a_{ij} + b_{ij} \\)）。
- 标量乘法：`2 * A` 得到 \\( \begin{pmatrix} 2 & 4 \\ 6 & 8 \end{pmatrix} \\)（\\( c a_{ij} \\)）。
- 矩阵乘法：`A @ B`（或 `np.dot(A, B)`）得到 \\( \begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix} \\)（验证：第1行第1列求和 \\( 1\cdot5 + 2\cdot7 = 19 \\)）。注意不可交换性：`np.allclose(A @ B, B @ A)` 为 `False`。
- 转置：`A.T` 得到 \\( \begin{pmatrix} 1 & 3 \\ 2 & 4 \end{pmatrix} \\)（\\( (A^T)_{ij} = a_{ji} \\)）。
- 逆矩阵：`np.linalg.inv(A)` 得到 \\( \begin{pmatrix} -2 & 1 \\ 1.5 & -0.5 \end{pmatrix} \\)（验证：`A @ inv_A` ≈ \\( I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} \\)，存在微小的浮点数误差 ~1e-16）。

## 2. 行列式

数学公式：\\( \det A = \sum_{j=1}^2 a_{1j} C_{1j} \\)，\\( C_{1j} = (-1)^{1+j} \det(M_{1j}) \\)（例如，\\( M_{11} = [4] \\)，所以 \\( C_{11} = 4 \\)；完整的 \\( \det A = 1\cdot4 - 2\cdot3 = -2 \\)）。

**NumPy 演示**（续上）：

- `np.linalg.det(A)`: -2.0（与公式匹配；浮点精度为 -2.0000000000000004）。
- 乘积：`np.linalg.det(A @ B)` = 4.0；`det_A * np.linalg.det(B)` ≈ 4.0（验证 \\( \det(AB) = \det A \cdot \det B \\)）。
- 转置：`np.linalg.det(A.T)` = -2.0（验证 \\( \det(A^T) = \det A \\)）。

关于伴随矩阵/逆矩阵的联系：逆矩阵在分母中使用行列式，如公式 \\( A^{-1} = \frac{1}{\det A} \adj A \\) 所示。

## 3. 线性方程组与高斯消元法

数学公式：增广矩阵 \\( [A | b] \\)，其中 \\( b = [b_i]_{i=1}^2 = [5, 11]^T \\)；在化为行阶梯形式后通过回代求解。

**NumPy 演示**：

- `np.linalg.solve(A, b)` 得到 [1. 2.]（精确解：\\( x_1 = \frac{\det A_1}{\det A} \\)，其中 \\( A_1 \\) 是将第1列替换为 b 的矩阵，行列式 = -2 相同；验证了克莱姆法则）。
- 检查：`A @ x` = [5. 11.]（残差为 0）。
- 秩：`np.linalg.matrix_rank(A)` = 2（满秩；对于奇异矩阵，秩 < 2 意味着无穷多解或无解）。

NumPy 的 `solve` 在内部执行类似 LU 分解的运算（无需显式编写高斯消元代码；如需自定义，可使用 `scipy.linalg.lu`，但此处建议坚持使用 np.linalg）。

## 4. 向量空间

数学公式：秩 A = 主元数量 = Col(A) 的维数；零度 = 2 - 秩 A。

**NumPy 演示**：

- 秩如上所述：2。
- 通过 SVD 估计零度：`U, S, Vt = np.linalg.svd(A)`；计数大于 1e-10 的奇异值：2，所以零度 = 2 - 2 = 0（Nul(A) = {0}）。对于基，零空间向量来自具有小奇异值 S 的 Vt 行。

## 5. 线性变换

数学公式：T(x)_i = \\( \sum_j a_{ij} x_j \\)；矩阵表示是 A。

**NumPy 关联**：与矩阵运算相同；例如，`T_x = A @ x` 应用了变换（向量化）。

## 6. 特征值

数学公式：求解 det(A - λ I) = 0，(A - λ I)_{ij} = a_{ij} - λ δ_{ij}；然后求解 (A - λ I) v = 0 得到 v_j。

**NumPy 演示**：

- `eigvals, eigvecs = np.linalg.eig(A)`：特征值 eigvals ≈ [-0.372, 5.372]（方程 λ² - tr(A)λ + det A = λ² - 5λ -2 =0 的根）。
- 特征向量列：例如，col0 ≈ [-0.825, 0.566]^T 对应 λ≈-0.372。
- 检查：`A @ eigvecs[:,0]` ≈ λ eigvecs[:,0]（缩放验证：`A @ eigvecs[:,0] / eigvals[0]` 匹配 eigvecs[:,0]）。

对于可对角化：满秩特征向量（det ≠0）。

## 7. 内积与正交化

数学公式：<u,v> = \\( \sum_i u_i v_i \\)；投影 proj = (<v,w>/<w,w>) w（对 w_i 进行标量乘法）。

**NumPy 演示**（u=[1,2], v=[3,4]）：

- `np.dot(u, v)` = 11（或 `u @ v`）。
- `np.linalg.norm(u)` ≈ 2.236（√<u,u>）。

格拉姆-施密特正交化：对矩阵 V（列作为基向量）使用 `np.linalg.qr(V)`；Q 是标准正交基。

- 示例 V = \\( \begin{pmatrix} 3 & 0 & 0 \\ 1 & 2 & 0 \\ 0 & 0 & 3 \end{pmatrix} \\)（列 v^{(1)}=[3,1,0]^T 等）。
- `ortho = np.linalg.qr(V)[0]` 得到 ≈ \\( \begin{pmatrix} -0.949 & -0.316 & 0 \\ -0.316 & 0.949 & 0 \\ 0 & 0 & 1 \end{pmatrix} \\)（符号翻转无妨）。
- 检查：`np.allclose(ortho.T @ ortho, np.eye(3))` = True（δ_{ij}）。

二次型：`u @ A @ u` = 27.0（x^T A x，其中 x_i = u_i；对于正定，所有特征值 >0——此处特征值符号混合）。

**快速验证提示**：对于浮点数，始终使用 `np.allclose`；对于小的 n，手动进行行化简，然后与 `solve` 或 `eig` 的结果匹配。练习：代入你自己的 3×3 矩阵。

[NumPy linalg 文档](https://numpy.org/doc/stable/reference/routines.linalg.html)
[NumPy 中的线性代数 - SciPy 讲义笔记](https://scipy-lectures.org/intro/numpy/auto_examples/plot_linear_algebra.html)
