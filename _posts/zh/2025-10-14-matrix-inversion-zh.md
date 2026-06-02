---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 3x3矩阵求逆
translated: true
type: note
---

是的，你的思路完全正确！你描述的是求解3×3矩阵\\( A \\)（通常记作\\( A^{-1} \\)）逆矩阵的标准方法，即使用**余子式矩阵**（更准确地说，是**伴随矩阵**，即余子式矩阵的转置）。你提到的“除以1/值 * 矩阵”指的是乘以\\( 1/\det(A) \\)进行缩放，其中\\( \det(A) \\)是矩阵\\( A \\)的行列式。而“旋转”可能是指“转置”（将行转换为列）——这也是关键步骤之一。

下面我将逐步解释这个方法、其原理，以及如何计算任意3×3矩阵的逆。这源于矩阵逆的通用公式：\\( A^{-1} = \frac{1}{\det(A)} \adj(A) \\)，其中\\( \adj(A) \\)是伴随矩阵。

### 3×3矩阵求逆的逐步方法

假设你的矩阵是：
\\[
A = \begin{pmatrix}
a & b & c \\
d & e & f \\
g & h & i
\end{pmatrix}
\\]

1. **计算行列式\\( \det(A) \\)**（即用于除法的“值”）：
   \\[
   \det(A) = a(ei - fh) - b(di - fg) + c(dh - eg)
   \\]
   如果\\( \det(A) = 0 \\)，则该矩阵不可逆（称为奇异矩阵）。否则，继续下一步。

2. **求余子式矩阵\\( C \\)**：
   - 元素\\( a_{ij} \\)的余子式\\( C_{ij} \\)是\\( (-1)^{i+j} \\)乘以删除第\\( i \\)行和第\\( j \\)列后得到的2×2子矩阵的行列式。
   - 你不需要从头计算*所有*余子式——可以沿一行（或一列）计算，并利用性质填充其余部分，但对于3×3矩阵，直接计算全部九个更快捷。

   余子式如下：
   \\[
   C_{11} = (-1)^{2} \det\begin{pmatrix} e & f \\ h & i \end{pmatrix} = ei - fh
   \\]
   \\[
   C_{12} = (-1)^{3} \det\begin{pmatrix} d & f \\ g & i \end{pmatrix} = -(di - fg)
   \\]
   \\[
   C_{13} = (-1)^{4} \det\begin{pmatrix} d & e \\ g & h \end{pmatrix} = dh - eg
   \\]
   \\[
   C_{21} = (-1)^{3} \det\begin{pmatrix} b & c \\ h & i \end{pmatrix} = -(bi - ch)
   \\]
   \\[
   C_{22} = (-1)^{4} \det\begin{pmatrix} a & c \\ g & i \end{pmatrix} = ai - cg
   \\]
   \\[
   C_{23} = (-1)^{5} \det\begin{pmatrix} a & b \\ g & h \end{pmatrix} = -(ah - bg)
   \\]
   \\[
   C_{31} = (-1)^{4} \det\begin{pmatrix} b & c \\ e & f \end{pmatrix} = bf - ce
   \\]
   \\[
   C_{32} = (-1)^{5} \det\begin{pmatrix} a & c \\ d & f \end{pmatrix} = -(af - cd)
   \\]
   \\[
   C_{33} = (-1)^{6} \det\begin{pmatrix} a & b \\ d & e \end{pmatrix} = ae - bd
   \\]

   因此余子式矩阵为：
   \\[
   C = \begin{pmatrix}
   ei-fh & -(di-fg) & dh-eg \\
   -(bi-ch) & ai-cg & -(ah-bg) \\
   bf-ce & -(af-cd) & ae-bd
   \end{pmatrix}
   \\]

3. **转置得到伴随矩阵\\( \adj(A) = C^T \\)**（即“旋转”步骤——交换行和列）：
   \\[
   \adj(A) = \begin{pmatrix}
   ei-fh & -(bi-ch) & bf-ce \\
   -(di-fg) & ai-cg & -(af-cd) \\
   dh-eg & -(ah-bg) & ae-bd
   \end{pmatrix}
   \\]

4. **乘以\\( 1/\det(A) \\)缩放得到逆矩阵**：
   \\[
   A^{-1} = \frac{1}{\det(A)} \adj(A)
   \\]
   \\( \adj(A) \\)的每个元素都乘以\\( 1/\det(A) \\)。

### 示例

设\\( A = \begin{pmatrix} 1 & 2 & 3 \\ 0 & 1 & 4 \\ 5 & 6 & 0 \end{pmatrix} \\)。

- \\( \det(A) = 1(1\cdot0 - 4\cdot6) - 2(0\cdot0 - 4\cdot5) + 3(0\cdot6 - 1\cdot5) = 1(-24) - 2(-20) + 3(-5) = -24 + 40 - 15 = 1 \\)。
- 余子式（简略计算）：\\( C = \begin{pmatrix} -24 & 20 & -5 \\ -15 & -15 & 5 \\ -14 & -10 & 1 \end{pmatrix} \\)（此处省略详细计算，但你可以验证）。
- \\( \adj(A) = C^T = \begin{pmatrix} -24 & -15 & -14 \\ 20 & -15 & -10 \\ -5 & 5 & 1 \end{pmatrix} \\)。
- \\( A^{-1} = \frac{1}{1} \adj(A) = \begin{pmatrix} -24 & -15 & -14 \\ 20 & -15 & -10 \\ -5 & 5 & 1 \end{pmatrix} \\)。

你可以验证：\\( A \cdot A^{-1} = I \\)（单位矩阵）。

### 为什么这个方法有效？

关键原因在于行列式和余子式的性质：对于任意方阵\\( A \\)，
\\[
A \cdot \adj(A) = \det(A) \cdot I
\\]
（其中\\( I \\)是单位矩阵）。这源于沿行/列展开行列式的**拉普拉斯展开**。在\\( A \cdot \adj(A) \\)中，每个对角线上的元素展开后等于\\( \det(A) \\)，而非对角线元素由于余子式符号的抵消而为零。

假设\\( \det(A) \\)非零，将等式两边除以\\( \det(A) \\)：
\\[
A \cdot \left( \frac{1}{\det(A)} \adj(A) \right) = I \implies A^{-1} = \frac{1}{\det(A)} \adj(A)
\\]
类似地，\\( \adj(A) \cdot A = \det(A) \cdot I \\)，因此从两边都成立。

此方法可推广到任意\\( n \times n \\)矩阵，但对于3×3矩阵，该方法效率较高。对于更大规模的矩阵，高斯消元法通常在计算上更快。

如果你有具体的矩阵需要求逆，或想澄清某一步骤，请随时分享！
