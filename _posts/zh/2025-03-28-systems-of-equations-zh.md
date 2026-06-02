---
audio: false
generated: true
lang: zh
layout: post
title: 方程组与高斯消元法
translated: true
type: note
---

本教程详细讲解**方程组**的表示方法、解法以及用于求解的**高斯消元法**。

---

## **1. 方程组：定义与表示**

**线性方程组**由多个共享变量的线性方程组成。包含 \\( n \\) 个变量和 \\( m \\) 个方程的一般方程组可表示为：

\\[
\begin{aligned}
a_{11}x_1 + a_{12}x_2 + \dots + a_{1n}x_n &= b_1 \\
a_{21}x_1 + a_{22}x_2 + \dots + a_{2n}x_n &= b_2 \\
\vdots & \\
a_{m1}x_1 + a_{m2}x_2 + \dots + a_{mn}x_n &= b_m
\end{aligned}
\\]

其中：
- \\( x_1, x_2, \dots, x_n \\) 是未知变量
- \\( a_{ij} \\) 是系数
- \\( b_1, b_2, \dots, b_m \\) 是右侧常数项

### **矩阵表示**

方程组可用**矩阵**形式表示：

\\[
A \mathbf{x} = \mathbf{b}
\\]

其中：

- \\( A \\) 是**系数矩阵**：

  \\[
  A =
  \begin{bmatrix}
  a_{11} & a_{12} & \dots & a_{1n} \\
  a_{21} & a_{22} & \dots & a_{2n} \\
  \vdots & \vdots & \ddots & \vdots \\
  a_{m1} & a_{m2} & \dots & a_{mn}
  \end{bmatrix}
  \\]

- \\( \mathbf{x} \\) 是**变量列向量**：

  \\[
  \mathbf{x} =
  \begin{bmatrix}
  x_1 \\
  x_2 \\
  \vdots \\
  x_n
  \end{bmatrix}
  \\]

- \\( \mathbf{b} \\) 是**常数项列向量**：

  \\[
  \mathbf{b} =
  \begin{bmatrix}
  b_1 \\
  b_2 \\
  \vdots \\
  b_m
  \end{bmatrix}
  \\]

**增广矩阵**表示为：

\\[
[A | \mathbf{b}]
\\]

示例：
\\[
\begin{aligned}
2x + 3y &= 8 \\
5x - y &= 3
\end{aligned}
\\]

矩阵表示：
\\[
\begin{bmatrix}
2 & 3 \\
5 & -1
\end{bmatrix}
\begin{bmatrix}
x \\
y
\end{bmatrix}
=
\begin{bmatrix}
8 \\
3
\end{bmatrix}
\\]

增广矩阵：
\\[
\left[
\begin{array}{cc|c}
2 & 3 & 8 \\
5 & -1 & 3
\end{array}
\right]
\\]

---

## **2. 高斯消元法**

高斯消元法是通过将增广矩阵转化为**行阶梯形式（REF）**，再通过**回代法**求解变量的系统方法。

### **高斯消元步骤**
1. 通过行变换将增广矩阵转换为**上三角矩阵（行阶梯形式）**：
   - 必要时交换行
   - 某行乘以非零常数
   - 将某行的倍数加到另一行

2. 通过**回代法**求解

---

### **示例1：使用高斯消元法求解方程组**

求解方程组：
\\[
\begin{aligned}
2x + y - z &= 3 \\
4x - 6y &= 2 \\
-2x + 7y + 2z &= 5
\end{aligned}
\\]

#### **步骤1：转换为增广矩阵**
\\[
\left[
\begin{array}{ccc|c}
2 & 1 & -1 & 3 \\
4 & -6 & 0 & 2 \\
-2 & 7 & 2 & 5
\end{array}
\right]
\\]

#### **步骤2：使首元为1**
第一行除以2：
\\[
\left[
\begin{array}{ccc|c}
1 & 0.5 & -0.5 & 1.5 \\
4 & -6 & 0 & 2 \\
-2 & 7 & 2 & 5
\end{array}
\right]
\\]

#### **步骤3：消去首元下方元素**
第二行减去4倍的第一行：
第三行加上2倍的第一行：

\\[
\left[
\begin{array}{ccc|c}
1 & 0.5 & -0.5 & 1.5 \\
0 & -8 & 2 & -4 \\
0 & 8 & 1 & 8
\end{array}
\right]
\\]

#### **步骤4：使次元为1**
第二行除以-8：

\\[
\left[
\begin{array}{ccc|c}
1 & 0.5 & -0.5 & 1.5 \\
0 & 1 & -0.25 & 0.5 \\
0 & 8 & 1 & 8
\end{array}
\right]
\\]

#### **步骤5：消去次元下方元素**
第三行减去8倍的第二行：

\\[
\left[
\begin{array}{ccc|c}
1 & 0.5 & -0.5 & 1.5 \\
0 & 1 & -0.25 & 0.5 \\
0 & 0 & 3 & 4
\end{array}
\right]
\\]

#### **步骤6：回代求解**
从下往上求解：
- \\( 3z = 4 \Rightarrow z = \frac{4}{3} \\)
- \\( y - 0.25z = 0.5 \Rightarrow y = 0.5 + 0.25(4/3) = \frac{7}{6} \\)
- \\( x + 0.5y - 0.5z = 1.5 \Rightarrow x = 1.5 - 0.5(7/6) + 0.5(4/3) = \frac{11}{6} \\)

**解：**
\\[
x = \frac{11}{6}, \quad y = \frac{7}{6}, \quad z = \frac{4}{3}
\\]

---

## **3. 解的类型**
1. **唯一解**：\\( x_1, x_2, \dots \\) 有唯一解
2. **无穷多解**：系统相关，存在多个解
3. **无解**：系统不一致

---

## **4. 齐次与非齐次方程组**
- **齐次方程组**：\\( A\mathbf{x} = 0 \\)
  - 至少存在**零解** \\( \mathbf{x} = 0 \\)
  - 当 \\( A \\) 的行列式为零时可能有无穷多解

- **非齐次方程组**：\\( A\mathbf{x} = \mathbf{b} \\)
  - 可能有**唯一解、无穷多解或无解**

---

## **结论**
- 高斯消元法是求解方程组的有效方法
- 解的数量取决于矩阵的**秩**
- 齐次方程组总是存在零解

如需更多示例或解释，请告诉我！🚀
