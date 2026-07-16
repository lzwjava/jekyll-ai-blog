---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过LU分解计算NumPy行列式
translated: true
type: note
---

问题：numpy 如何计算矩阵的行列式，其底层算法是什么？

答案：`np.linalg.det` 并不使用余子式展开（那是 O(n!)）。它使用的是 **LU 分解**——将 A 分解为 PLU，然后 det(A) = det(P) *det(L)* det(U)。由于 L 是单位下三角矩阵（det=1），U 是上三角矩阵，det(U) 等于对角线元素的乘积。det(P) 根据置换的奇偶性为 ±1。

```python
import numpy as np
from scipy.linalg import lu

A = np.array([[4., 3., 2.],
              [1., 5., 6.],
              [7., 8., 9.]])

print(np.linalg.det(A))  # -55.0000...

# 底层发生了什么
P, L, U = lu(A)
print(np.diag(U))                     # U 的对角线
sign = np.linalg.det(P)               # ±1，置换奇偶性
det = sign * np.prod(np.diag(U))
print(det)
```

在底层，numpy 调用 LAPACK 的 `dgetrf`（双精度）或 `sgetrf`（单精度）进行带部分主元的 LU 分解，计算复杂度为 O(n³)，而余子式展开是 O(n!)。这就是为什么 1000x1000 的行列式可以瞬间算出。

实际中你会遇到的一个陷阱：浮点数。LU 主元选择会导致微小数值误差累积，因此对一个真正奇异的矩阵，`det` 可能返回 `1e-14` 而不是精确的 `0`。请使用容差判断，而非 `== 0`：

```python
if abs(np.linalg.det(A)) < 1e-10:
    print("singular")
```

对于对数行列式（常见于 GMMs、Gaussian processes、normalizing flows——避免大矩阵下溢/溢出），请改用 `np.linalg.slogdet`，它会分别跟踪符号和 log|det|：

```python
sign, logdet = np.linalg.slogdet(A)
```

参考：

- [numpy.linalg.det 文档](https://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html)
- [LAPACK dgetrf](https://netlib.org/lapack/explore-html/dd/d9a/group__getrf.html)
