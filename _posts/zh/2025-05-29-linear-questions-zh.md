---
audio: false
generated: true
lang: zh
layout: post
title: 线性代数问题
translated: true
type: note
---

**18. 设矩阵 X 和 A 满足关系式 XA = X + A。若 $A = \begin{pmatrix} 1 & -3 & 0 \\\ 2 & 1 & 0 \\\ 0 & 0 & 2 \end{pmatrix}$，求矩阵 X。**

**答案：**
已知方程 $XA = X + A$。
我们可以将其重写为 $XA - X = A$，所以 $X(A - I) = A$。
如果 $(A - I)$ 可逆，则 $X = A(A - I)^{-1}$。

首先，计算 $A - I$：

$A - I = \begin{pmatrix} 1 & -3 & 0 \\\ 2 & 1 & 0 \\\ 0 & 0 & 2 \end{pmatrix} - \begin{pmatrix} 1 & 0 & 0 \\\ 0 & 1 & 0 \\\ 0 & 0 & 1 \end{pmatrix} = \begin{pmatrix} 0 & -3 & 0 \\\ 2 & 0 & 0 \\\ 0 & 0 & 1 \end{pmatrix}$。

接下来，求 $(A - I)$ 的逆。令 $B = A - I$。
B 的行列式为 $\det(B) = 0(0 - 0) - (-3)(2 - 0) + 0(0 - 0) = 6$。
由于 $\det(B) \neq 0$，B 可逆。

B 的伴随矩阵为：
$adj(B) = \begin{pmatrix} C_{11} & C_{21} & C_{31} \\\ C_{12} & C_{22} & C_{32} \\\ C_{13} & C_{23} & C_{33} \end{pmatrix}$
$C_{11} = \begin{vmatrix} 0 & 0 \\\ 0 & 1 \end{vmatrix} = 0$
$C_{12} = -\begin{vmatrix} 2 & 0 \\\ 0 & 1 \end{vmatrix} = -2$
$C_{13} = \begin{vmatrix} 2 & 0 \\\ 0 & 0 \end{vmatrix} = 0$
$C_{21} = -\begin{vmatrix} -3 & 0 \\\ 0 & 1 \end{vmatrix} = 3$
$C_{22} = \begin{vmatrix} 0 & 0 \\\ 0 & 1 \end{vmatrix} = 0$
$C_{23} = -\begin{vmatrix} 0 & -3 \\\ 0 & 0 \end{vmatrix} = 0$
$C_{31} = \begin{vmatrix} -3 & 0 \\\ 0 & 0 \end{vmatrix} = 0$
$C_{32} = -\begin{vmatrix} 0 & 0 \\\ 2 & 0 \end{vmatrix} = 0$
$C_{33} = \begin{vmatrix} 0 & -3 \\\ 2 & 0 \end{vmatrix} = 6$

余子矩阵为 $C = \begin{pmatrix} 0 & -2 & 0 \\\ 3 & 0 & 0 \\\ 0 & 0 & 6 \end{pmatrix}$。
伴随矩阵为 $adj(B) = C^T = \begin{pmatrix} 0 & 3 & 0 \\\ -2 & 0 & 0 \\\ 0 & 0 & 6 \end{pmatrix}$。

于是，$(A - I)^{-1} = \frac{1}{\det(B)} adj(B) = \frac{1}{6} \begin{pmatrix} 0 & 3 & 0 \\\ -2 & 0 & 0 \\\ 0 & 0 & 6 \end{pmatrix} = \begin{pmatrix} 0 & 1/2 & 0 \\\ -1/3 & 0 & 0 \\\ 0 & 0 & 1 \end{pmatrix}$。

现在计算 $X = A(A - I)^{-1}$：
$X = \begin{pmatrix} 1 & -3 & 0 \\\ 2 & 1 & 0 \\\ 0 & 0 & 2 \end{pmatrix} \begin{pmatrix} 0 & 1/2 & 0 \\\ -1/3 & 0 & 0 \\\ 0 & 0 & 1 \end{pmatrix}$
$X = \begin{pmatrix} (1)(0) + (-3)(-1/3) + (0)(0) & (1)(1/2) + (-3)(0) + (0)(0) & (1)(0) + (-3)(0) + (0)(1) \\\ (2)(0) + (1)(-1/3) + (0)(0) & (2)(1/2) + (1)(0) + (0)(0) & (2)(0) + (1)(0) + (0)(1) \\\ (0)(0) + (0)(-1/3) + (2)(0) & (0)(1/2) + (0)(0) + (2)(0) & (0)(0) + (0)(0) + (2)(1) \end{pmatrix}$
$X = \begin{pmatrix} 0+1+0 & 1/2+0+0 & 0+0+0 \\\ 0-1/3+0 & 1+0+0 & 0+0+0 \\\ 0+0+0 & 0+0+0 & 0+0+2 \end{pmatrix}$
$X = \begin{pmatrix} 1 & 1/2 & 0 \\\ -1/3 & 1 & 0 \\\ 0 & 0 & 2 \end{pmatrix}$。

**19. 确定 k 的值，使得向量 $\alpha_1 = (1, 1, k)^T$, $\alpha_2 = (1, k, 1)^T$, $\alpha_3 = (k, 1, 1)^T$ 线性相关。找出一个极大线性无关组，并用该组表示其余向量。**

**答案：**
向量 $\alpha_1, \alpha_2, \alpha_3$ 线性相关当且仅当由这些向量构成的矩阵的行列式为零。
令 $A = \begin{pmatrix} 1 & 1 & k \\\ 1 & k & 1 \\\ k & 1 & 1 \end{pmatrix}$。
$\det(A) = 1(k - 1) - 1(1 - k) + k(1 - k^2)$
$= k - 1 - 1 + k + k - k^3$
$= -k^3 + 3k - 2$。
我们需要找到 k 使得 $-k^3 + 3k - 2 = 0$，即 $k^3 - 3k + 2 = 0$。
我们可以测试 2 的整数因子（即 $\pm 1, \pm 2$）。
如果 $k=1$，$1^3 - 3(1) + 2 = 1 - 3 + 2 = 0$。所以 $(k-1)$ 是一个因子。
如果 $k=-2$，$(-2)^3 - 3(-2) + 2 = -8 + 6 + 2 = 0$。所以 $(k+2)$ 是一个因子。
使用多项式除法或综合除法计算 $(k^3 - 3k + 2) / (k-1)$：
$(k-1)(k^2+k-2) = 0$
$(k-1)(k+2)(k-1) = 0$
所以，根为 $k=1$（重根）和 $k=-2$。
当 $k=1$ 或 $k=-2$ 时，向量线性相关。

情况 1：$k=1$
$\alpha_1 = (1, 1, 1)^T$, $\alpha_2 = (1, 1, 1)^T$, $\alpha_3 = (1, 1, 1)^T$。
在这种情况下，所有三个向量都相同。
一个极大线性无关组可以是 $\{\alpha_1\}$。
那么 $\alpha_2 = 1 \cdot \alpha_1$ 且 $\alpha_3 = 1 \cdot \alpha_1$。

情况 2：$k=-2$
$\alpha_1 = (1, 1, -2)^T$, $\alpha_2 = (1, -2, 1)^T$, $\alpha_3 = (-2, 1, 1)^T$。
检查 $\alpha_1$ 和 $\alpha_2$ 是否线性无关。它们不是彼此的标量倍数，所以它们线性无关。因此，一个极大线性无关组可以是 $\{\alpha_1, \alpha_2\}$。
我们希望将 $\alpha_3$ 表示为 $\alpha_1$ 和 $\alpha_2$ 的线性组合：
$\alpha_3 = c_1 \alpha_1 + c_2 \alpha_2$
$(-2, 1, 1)^T = c_1 (1, 1, -2)^T + c_2 (1, -2, 1)^T$
这给出方程组：
1) $c_1 + c_2 = -2$
2) $c_1 - 2c_2 = 1$
3) $-2c_1 + c_2 = 1$
(1) 减去 (2)：$(c_1 + c_2) - (c_1 - 2c_2) = -2 - 1 \Rightarrow 3c_2 = -3 \Rightarrow c_2 = -1$。
将 $c_2 = -1$ 代入 (1)：$c_1 - 1 = -2 \Rightarrow c_1 = -1$。
用 (3) 检查：$-2(-1) + (-1) = 2 - 1 = 1$。这是一致的。
所以，$\alpha_3 = -1 \cdot \alpha_1 - 1 \cdot \alpha_2$。

**20. 求解线性方程组 { $x_1 - x_2 - 3x_4 = -2$ ; $x_1 + 2x_3 - 2x_4 = -1$ ; $2x_1 - 2x_2 + x_3 - 6x_4 = -5$ ; $-x_1 + 2x_2 + 3x_3 + 4x_4 = 2$ }（求一个特解和对应齐次方程组的基础解系）。**

**答案：**
增广矩阵为：
$\begin{pmatrix} 1 & -1 & 0 & -3 & | & -2 \\\ 1 & 0 & 2 & -2 & | & -1 \\\ 2 & -2 & 1 & -6 & | & -5 \\\ -1 & 2 & 3 & 4 & | & 2 \end{pmatrix}$

$R_2 \leftarrow R_2 - R_1$
$R_3 \leftarrow R_3 - 2R_1$
$R_4 \leftarrow R_4 + R_1$
$\begin{pmatrix} 1 & -1 & 0 & -3 & | & -2 \\\ 0 & 1 & 2 & 1 & | & 1 \\\ 0 & 0 & 1 & 0 & | & -1 \\\ 0 & 1 & 3 & 1 & | & 0 \end{pmatrix}$

$R_1 \leftarrow R_1 + R_2$
$R_4 \leftarrow R_4 - R_2$
$\begin{pmatrix} 1 & 0 & 2 & -2 & | & -1 \\\ 0 & 1 & 2 & 1 & | & 1 \\\ 0 & 0 & 1 & 0 & | & -1 \\\ 0 & 0 & 1 & 0 & | & -1 \end{pmatrix}$

$R_1 \leftarrow R_1 - 2R_3$
$R_2 \leftarrow R_2 - 2R_3$
$R_4 \leftarrow R_4 - R_3$
$\begin{pmatrix} 1 & 0 & 0 & -2 & | & 1 \\\ 0 & 1 & 0 & 1 & | & 3 \\\ 0 & 0 & 1 & 0 & | & -1 \\\ 0 & 0 & 0 & 0 & | & 0 \end{pmatrix}$

方程组等价于：
$x_1 - 2x_4 = 1 \Rightarrow x_1 = 1 + 2x_4$
$x_2 + x_4 = 3 \Rightarrow x_2 = 3 - x_4$
$x_3 = -1$
令 $x_4 = t$（自由变量）。
通解为：
$x_1 = 1 + 2t$
$x_2 = 3 - t$
$x_3 = -1$
$x_4 = t$
向量形式：$X = \begin{pmatrix} 1 \\\ 3 \\\ -1 \\\ 0 \end{pmatrix} + t \begin{pmatrix} 2 \\\ -1 \\\ 0 \\\ 1 \end{pmatrix}$。

令 $t=0$ 得到一个特解：$X_p = \begin{pmatrix} 1 \\\ 3 \\\ -1 \\\ 0 \end{pmatrix}$。

对应齐次方程组的解为 $X_h = t \begin{pmatrix} 2 \\\ -1 \\\ 0 \\\ 1 \end{pmatrix}$。
齐次方程组的基础解系为 $\{\begin{pmatrix} 2 \\\ -1 \\\ 0 \\\ 1 \end{pmatrix}\}$。

**21. 设矩阵 A = \begin{pmatrix} x & 0 & y \\\ 0 & 2 & 0 \\\ y & 0 & -2 \end{pmatrix} 有一个特征值为 -3，且 |A| = -12。求 x 和 y 的值。**

**答案：**
特征方程为 $\det(A - \lambda I) = 0$。
$A - \lambda I = \begin{pmatrix} x-\lambda & 0 & y \\\ 0 & 2-\lambda & 0 \\\ y & 0 & -2-\lambda \end{pmatrix}$。
$\det(A - \lambda I) = (x-\lambda)[(2-\lambda)(-2-\lambda) - 0] - 0 + y[0 - y(2-\lambda)]$
$= (x-\lambda)(2-\lambda)(-2-\lambda) - y^2(2-\lambda)$
$= (2-\lambda)[(x-\lambda)(-2-\lambda) - y^2]$
$= (2-\lambda)[-2x - x\lambda + 2\lambda + \lambda^2 - y^2] = 0$。
特征值为 $\lambda_1 = 2$，以及方程 $\lambda^2 + (2-x)\lambda - (2x+y^2) = 0$ 的根。
已知一个特征值为 -3。
如果 $2 = -3$，这是错误的。所以，-3 必须是 $\lambda^2 + (2-x)\lambda - (2x+y^2) = 0$ 的一个根。
代入 $\lambda = -3$：
$(-3)^2 + (2-x)(-3) - (2x+y^2) = 0$
$9 - 6 + 3x - 2x - y^2 = 0$
$3 + x - y^2 = 0 \Rightarrow x - y^2 = -3$（方程 1）

同时已知 $\det(A) = -12$。
$\det(A) = x(2(-2) - 0) - 0 + y(0 - 2y)$
$= -4x - 2y^2 = -12$
除以 -2：$2x + y^2 = 6$（方程 2）

现在我们得到关于 x 和 y 的方程组：
1) $x - y^2 = -3$
2) $2x + y^2 = 6$
方程 1 加方程 2：
$(x - y^2) + (2x + y^2) = -3 + 6$
$3x = 3 \Rightarrow x = 1$。
将 $x=1$ 代入方程 1：
$1 - y^2 = -3$
$-y^2 = -4$
$y^2 = 4 \Rightarrow y = \pm 2$。

所以值为 $x=1$ 和 $y=2$，或 $x=1$ 和 $y=-2$。

检查两种情况下的特征值。
特征多项式分解为 $(2-\lambda)[\lambda^2 + (2-x)\lambda - (2x+y^2)] = 0$。
如果 $x=1, y=2$：
$(2-\lambda)[\lambda^2 + (2-1)\lambda - (2(1)+2^2)] = 0$
$(2-\lambda)[\lambda^2 + \lambda - (2+4)] = 0$
$(2-\lambda)(\lambda^2 + \lambda - 6) = 0$
$(2-\lambda)(\lambda+3)(\lambda-2) = 0$。
特征值为 $\lambda = 2, -3, 2$。这与有一个特征值为 -3 一致。

如果 $x=1, y=-2$：
$(2-\lambda)[\lambda^2 + (2-1)\lambda - (2(1)+(-2)^2)] = 0$
$(2-\lambda)[\lambda^2 + \lambda - (2+4)] = 0$
$(2-\lambda)(\lambda^2 + \lambda - 6) = 0$
$(2-\lambda)(\lambda+3)(\lambda-2) = 0$。
特征值为 $\lambda = 2, -3, 2$。这也一致。

两对 $(x,y) = (1,2)$ 和 $(x,y) = (1,-2)$ 都满足条件。

**22. 设三元二次型 $f(x_1, x_2, x_3) = t(x_1^2 + x_2^2 + x_3^2) + 2x_1x_2 + 2x_1x_3 - 2x_2x_3$。确定 t 取何值时该二次型是正定的。**

**答案：**
该二次型的矩阵 A 为：
$A = \begin{pmatrix} t & 1 & 1 \\\ 1 & t & -1 \\\ 1 & -1 & t \end{pmatrix}$。
要使二次型正定，A 的所有顺序主子式必须为正。

1. 第一个顺序主子式为 $M_1 = t$。
正定性要求 $t > 0$。

2. 第二个顺序主子式为 $M_2 = \det \begin{pmatrix} t & 1 \\\ 1 & t \end{pmatrix} = t^2 - 1$。
正定性要求 $t^2 - 1 > 0 \Rightarrow t^2 > 1$。
由于已有 $t > 0$，这意味着 $t > 1$。

3. 第三个顺序主子式为 $M_3 = \det(A)$。
$M_3 = t(t^2 - 1) - 1(t - (-1)) + 1(-1 - t)$
$= t(t^2 - 1) - (t + 1) - (1 + t)$
$= t^3 - t - t - 1 - 1 - t$
$= t^3 - 3t - 2$。
正定性要求 $t^3 - 3t - 2 > 0$。

从第 19 题可知 $k^3 - 3k - 2 = (k+1)^2(k-2)$。（这里 $k$ 是 $t$）
所以，$t^3 - 3t - 2 = (t+1)^2(t-2)$。
我们需要 $(t+1)^2(t-2) > 0$。
由于 $(t+1)^2 \ge 0$，且为了不为零，$t \neq -1$。
所以我们需要 $t-2 > 0$，即 $t > 2$。

综合条件：
1) $t > 0$
2) $t > 1$
3) $t > 2$

这些条件的交集是 $t > 2$。
因此，当 $t > 2$ 时，该二次型是正定的。
