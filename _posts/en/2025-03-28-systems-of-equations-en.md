---
audio: false
generated: true
lang: en
layout: post
title: Systems of Equations and Gaussian Elimination
translated: false
type: note
---

This tutorial provides a detailed guide on **systems of equations**, their representation, solutions, and the **Gaussian elimination** method used to solve them.

---

## **1. Systems of Equations: Definition and Representation**

A **system of linear equations** consists of multiple linear equations that share variables. A general system with \\( n \\) variables and \\( m \\) equations can be written as:

\\[
\begin{aligned}
a_{11}x_1 + a_{12}x_2 + \dots + a_{1n}x_n &= b_1 \\
a_{21}x_1 + a_{22}x_2 + \dots + a_{2n}x_n &= b_2 \\
\vdots & \\
a_{m1}x_1 + a_{m2}x_2 + \dots + a_{mn}x_n &= b_m
\end{aligned}
\\]

where:

- \\( x_1, x_2, \dots, x_n \\) are the unknown variables.
- \\( a_{ij} \\) are the coefficients.
- \\( b_1, b_2, \dots, b_m \\) are the constants on the right-hand side.

### **Matrix Representation**

A system of equations can be represented using **matrices**:

\\[
A \mathbf{x} = \mathbf{b}
\\]

where:

- \\( A \\) is the **coefficient matrix**:

  \\[
  A =
  \begin{bmatrix}
  a_{11} & a_{12} & \dots & a_{1n} \\
  a_{21} & a_{22} & \dots & a_{2n} \\
  \vdots & \vdots & \ddots & \vdots \\
  a_{m1} & a_{m2} & \dots & a_{mn}
  \end{bmatrix}
  \\]

- \\( \mathbf{x} \\) is the **variable column vector**:

  \\[
  \mathbf{x} =
  \begin{bmatrix}
  x_1 \\
  x_2 \\
  \vdots \\
  x_n
  \end{bmatrix}
  \\]

- \\( \mathbf{b} \\) is the **constant column vector**:

  \\[
  \mathbf{b} =
  \begin{bmatrix}
  b_1 \\
  b_2 \\
  \vdots \\
  b_m
  \end{bmatrix}
  \\]

The **augmented matrix** is written as:

\\[
[A | \mathbf{b}]
\\]

Example:
\\[
\begin{aligned}
2x + 3y &= 8 \\
5x - y &= 3
\end{aligned}
\\]

Matrix representation:
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

Augmented matrix:
\\[
\left[
\begin{array}{cc|c}
2 & 3 & 8 \\
5 & -1 & 3
\end{array}
\right]
\\]

---

## **2. Gaussian Elimination Method**

Gaussian elimination is a systematic method for solving systems of equations by transforming the augmented matrix into **row echelon form (REF)** and then solving for the variables using **back-substitution**.

### **Steps of Gaussian Elimination**

1. **Convert the augmented matrix into an upper triangular (row echelon) form** by using row operations:
   - Swap rows if needed.
   - Multiply a row by a nonzero constant.
   - Add or subtract a multiple of one row from another.

2. **Back-substitution** to find the solution.

---

### **Example 1: Solving a System using Gaussian Elimination**

Solve the system:
\\[
\begin{aligned}
2x + y - z &= 3 \\
4x - 6y &= 2 \\
-2x + 7y + 2z &= 5
\end{aligned}
\\]

#### **Step 1: Convert to Augmented Matrix**

\\[
\left[
\begin{array}{ccc|c}
2 & 1 & -1 & 3 \\
4 & -6 & 0 & 2 \\
-2 & 7 & 2 & 5
\end{array}
\right]
\\]

#### **Step 2: Make the First Pivot 1**

Divide row 1 by 2:
\\[
\left[
\begin{array}{ccc|c}
1 & 0.5 & -0.5 & 1.5 \\
4 & -6 & 0 & 2 \\
-2 & 7 & 2 & 5
\end{array}
\right]
\\]

#### **Step 3: Eliminate First Column Below Pivot**

Replace row 2 by subtracting 4 times row 1:
Replace row 3 by adding 2 times row 1:

\\[
\left[
\begin{array}{ccc|c}
1 & 0.5 & -0.5 & 1.5 \\
0 & -8 & 2 & -4 \\
0 & 8 & 1 & 8
\end{array}
\right]
\\]

#### **Step 4: Make Second Pivot 1**

Divide row 2 by -8:

\\[
\left[
\begin{array}{ccc|c}
1 & 0.5 & -0.5 & 1.5 \\
0 & 1 & -0.25 & 0.5 \\
0 & 8 & 1 & 8
\end{array}
\right]
\\]

#### **Step 5: Eliminate Second Column Below Pivot**

Replace row 3 by subtracting 8 times row 2:

\\[
\left[
\begin{array}{ccc|c}
1 & 0.5 & -0.5 & 1.5 \\
0 & 1 & -0.25 & 0.5 \\
0 & 0 & 3 & 4
\end{array}
\right]
\\]

#### **Step 6: Back Substitution**

Solve from bottom to top:

- \\( 3z = 4 \Rightarrow z = \frac{4}{3} \\)
- \\( y - 0.25z = 0.5 \Rightarrow y = 0.5 + 0.25(4/3) = \frac{7}{6} \\)
- \\( x + 0.5y - 0.5z = 1.5 \Rightarrow x = 1.5 - 0.5(7/6) + 0.5(4/3) = \frac{11}{6} \\)

**Solution:**
\\[
x = \frac{11}{6}, \quad y = \frac{7}{6}, \quad z = \frac{4}{3}
\\]

---

## **3. Solution Types**

1. **Unique Solution**: A single solution for \\( x_1, x_2, \dots \\).
2. **Infinite Solutions**: Many solutions (system is dependent).
3. **No Solution**: Inconsistent system.

---

## **4. Homogeneous vs. Non-Homogeneous Systems**

- **Homogeneous system**: \\( A\mathbf{x} = 0 \\)
  - Always has at least the **trivial solution** \\( \mathbf{x} = 0 \\).
  - May have infinitely many solutions if the determinant of \\( A \\) is zero.

- **Non-homogeneous system**: \\( A\mathbf{x} = \mathbf{b} \\)
  - May have **unique, infinite, or no solutions**.

---

## **Conclusion**

- Gaussian elimination is a powerful method to solve systems.
- The number of solutions depends on the **rank** of the matrix.
- Homogeneous systems always have a trivial solution.

Let me know if you need more examples or explanations! 🚀
