---
audio: false
generated: true
lang: en
layout: post
title: Determinants
translated: false
type: note
---

Got it! Here's the tutorial with only display math (block equations).

---

# **Chapter: Determinants**

## **1. Definition of a Determinant**
A determinant is a scalar value that can be computed from the elements of a square matrix. It provides essential information about the matrix, such as invertibility, volume scaling, and solutions to linear equations.

For an \\( n \times n \\) matrix \\( A \\), the determinant is denoted as:

\\[
\det(A) \quad \text{or} \quad |A|
\\]

## **2. Computation of Determinants**

### **2.1 Determinant of a 2×2 Matrix**
For a \\( 2 \times 2 \\) matrix:

\\[
A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}
\\]

The determinant is given by:

\\[
\det(A) = ad - bc
\\]

### **2.2 Determinant of a 3×3 Matrix**
For a \\( 3 \times 3 \\) matrix:

\\[
A = \begin{bmatrix} a_{11} & a_{12} & a_{13} \\ a_{21} & a_{22} & a_{23} \\ a_{31} & a_{32} & a_{33} \end{bmatrix}
\\]

The determinant can be computed using cofactor expansion along the first row:

\\[
\det(A) = a_{11} \begin{vmatrix} a_{22} & a_{23} \\ a_{32} & a_{33} \end{vmatrix}
- a_{12} \begin{vmatrix} a_{21} & a_{23} \\ a_{31} & a_{33} \end{vmatrix}
+ a_{13} \begin{vmatrix} a_{21} & a_{22} \\ a_{31} & a_{32} \end{vmatrix}
\\]

Each \\( 2 \times 2 \\) determinant is computed as shown earlier.

### **2.3 Determinants of Higher-Order Matrices**
For an \\( n \times n \\) matrix, determinants can be computed using:
- **Cofactor Expansion** (Laplace expansion along any row or column)
- **Row Reduction Method** (Transforming into upper triangular form and multiplying the diagonal elements)
- **Leibniz Formula** (Sum over all permutations, practical only for small \\( n \\))

## **3. Properties of Determinants**

\\[
\det(I_n) = 1
\\]

\\[
\det(B) = -\det(A) \quad \text{if } B \text{ is obtained by swapping two rows of } A.
\\]

\\[
\det(A) = 0 \quad \text{if a row (or column) is entirely zero.}
\\]

\\[
\det(kA) = k^n \det(A)
\\]

\\[
\det(A) = \text{Product of diagonal elements} \quad \text{if } A \text{ is triangular.}
\\]

\\[
\det(AB) = \det(A) \det(B)
\\]

\\[
\det(A^{-1}) = \frac{1}{\det(A)} \quad \text{if } A \text{ is invertible.}
\\]

\\[
\det(A^T) = \det(A)
\\]

## **4. Applications of Determinants**

### **4.1 Checking Invertibility**
A square matrix \\( A \\) is invertible if and only if

\\[
\det(A) \neq 0
\\]

### **4.2 Cramer’s Rule (Solving Linear Systems)**
For a system \\( Ax = b \\), where \\( A \\) is an \\( n \times n \\) invertible matrix, the solution for each variable \\( x_i \\) is:

\\[
x_i = \frac{\det(A_i)}{\det(A)}
\\]

where \\( A_i \\) is obtained by replacing the \\( i \\)-th column of \\( A \\) with \\( b \\).

### **4.3 Volume Interpretation**
The absolute value of the determinant of an \\( n \times n \\) matrix represents the volume of the transformed unit hypercube:

\\[
\text{Volume} = |\det(A)|
\\]

### **4.4 Eigenvalues and Characteristic Equation**
The determinant is used in finding eigenvalues via the characteristic equation:

\\[
\det(A - \lambda I) = 0
\\]

---

This tutorial provides a fundamental understanding of determinants, including their computation, properties, and applications. Let me know if you need further explanations or examples!
