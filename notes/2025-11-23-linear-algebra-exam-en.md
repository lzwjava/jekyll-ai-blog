---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-2.5-flash
title: Linear Algebra Exam Practice Questions
translated: false
type: note
---

I understand you're looking for typical past "big questions" (formalization and calculation problems) from the **Guangdong Self-Study Exam Linear Algebra (Course Code: 02198)** to use as practice.

Since the official English syllabus and past papers are hard to find, I'll provide you with common types of big questions from a standard undergraduate linear algebra course, which are highly likely to cover the final, most involved questions on the 02198 exam. These questions usually test a deeper understanding and involve multiple steps.

Here are three major categories of big questions, along with specific exercise examples.

---

## 1. ⚙️ Calculation-Intensive Questions

These questions often involve large matrices and require a sequence of operations.

### Exercise 1: Finding an Inverse Matrix and Solving a System

Given the matrix \\(A = \begin{pmatrix} 1 & -1 & 0 \\ 0 & 2 & 1 \\ 1 & 0 & 3 \end{pmatrix}\\).

1. Calculate the **inverse matrix** \\(A^{-1}\\) using the adjugate matrix formula or the row reduction method \\(\left(A | I\right) \to \left(I | A^{-1}\right)\\).
2. Use the inverse matrix \\(A^{-1}\\) to solve the system of linear equations \\(A\mathbf{x} = \mathbf{b}\\), where \\(\mathbf{b} = \begin{pmatrix} 2 \\ 1 \\ 5 \end{pmatrix}\\).

### Exercise 2: Change of Basis and Coordinate Transformation

In \\(\mathbb{R}^3\\), consider two bases:

* The **standard basis** \\(E = \{\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3\}\\).
* A new basis \\(B = \{\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}\\), where \\(\mathbf{v}_1 = \begin{pmatrix} 1 \\ 0 \\ 1 \end{pmatrix}\\), \\(\mathbf{v}_2 = \begin{pmatrix} 1 \\ 1 \\ 0 \end{pmatrix}\\), and \\(\mathbf{v}_3 = \begin{pmatrix} 0 \\ 1 \\ 1 \end{pmatrix}\\).

1. Find the **transition matrix** \\(P_{E \leftarrow B}\\) from basis \\(B\\) to basis \\(E\\).
2. Find the transition matrix \\(P_{B \leftarrow E}\\) from basis \\(E\\) to basis \\(B\\).
3. If a vector \\(\mathbf{w}\\) has coordinates \\([\mathbf{w}]_B = \begin{pmatrix} 2 \\ -1 \\ 3 \end{pmatrix}\\) in basis \\(B\\), find its coordinates \\([\mathbf{w}]_E\\) in the standard basis \\(E\\).

---

## 2. 🔢 Eigenvalues and Diagonalization Questions

These are almost always the most important and multi-step questions.

### Exercise 3: Diagonalization and Matrix Powers

Given the matrix \\(A = \begin{pmatrix} 2 & 2 & -2 \\ 2 & 2 & -2 \\ -2 & -2 & 2 \end{pmatrix}\\).

1. Find all the **eigenvalues** \\(\lambda\\) of \\(A\\).
2. For each eigenvalue, find the corresponding **eigenspace** and a set of **linearly independent eigenvectors**.
3. Determine if \\(A\\) is **diagonalizable**. If it is, find the invertible matrix \\(P\\) and the diagonal matrix \\(\Lambda\\) such that \\(P^{-1}AP = \Lambda\\).
4. Use the result to calculate the matrix power \\(A^{100}\\).

---

## 3. ✍️ Formalization/Proof and Conceptual Questions

These questions often involve properties of matrices or linear maps and require a rigorous argument, sometimes using definitions or theorems.

### Exercise 4: Rank and Linear Systems (Formalization)

Consider a system of \\(m\\) linear equations in \\(n\\) unknowns, \\(A\mathbf{x} = \mathbf{b}\\). Let \\(A\\) be the **coefficient matrix** and \\(\tilde{A} = (A|\mathbf{b})\\) be the **augmented matrix**.

**Formalization/Proof Question:**

Prove that the system \\(A\mathbf{x} = \mathbf{b}\\) has:

1. **No solution** if and only if \\(Rank(A) < Rank(\tilde{A})\\).
2. **A unique solution** if and only if \\(Rank(A) = Rank(\tilde{A}) = n\\).
3. **Infinitely many solutions** if and only if \\(Rank(A) = Rank(\tilde{A}) < n\\).

### Exercise 5: Properties of Linear Maps (Formalization)

Let \\(V\\) and \\(W\\) be two finite-dimensional vector spaces, and let \\(T: V \to W\\) be a **linear transformation**.

**Formalization/Proof Question:**

Prove that if \\(T\\) is **injective** (one-to-one), then the **nullity** of \\(T\\) (the dimension of the kernel \\(\text{Null}(T)\\)) is zero. That is, \\(\dim(\text{Null}(T)) = 0\\).

***

### Summary of Key Concepts Tested

The "big questions" typically involve a combination of these core topics:

* **Matrix Operations:** Determinants, Inverses, Adjugates.
* **Linear Systems:** Rank, Rouché–Capelli theorem, solving non-homogeneous systems.
* **Vector Spaces:** Basis, Dimension, Subspaces, Change of Basis.
* **Eigen-Theory:** Eigenvalues, Eigenvectors, Eigenspaces, Diagonalization, Quadratic Forms.

Would you like me to provide **step-by-step solutions** for any of these exercises, or should I try to find a few more examples focusing on **Quadratic Forms**?
