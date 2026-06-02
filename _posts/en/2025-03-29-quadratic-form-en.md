---
audio: false
generated: true
lang: en
layout: post
title: Quadratic Form
translated: false
type: note
---

In linear algebra, a **quadratic form** is a function $Q: \mathbb{R}^n \rightarrow \mathbb{R}$ that can be expressed as:

$Q(\mathbf{x}) = \mathbf{x}^T A \mathbf{x}$

where:
* $\mathbf{x}$ is a column vector in $\mathbb{R}^n$:
    $\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}$
* $A$ is an $n \times n$ symmetric matrix with real entries. This matrix is called the **matrix of the quadratic form**.
* $\mathbf{x}^T$ is the transpose of $\mathbf{x}$, which is a row vector.

**In simpler terms:**

A quadratic form is a homogeneous polynomial of degree two in $n$ variables. "Homogeneous" means that every term in the polynomial has a total degree of two.

For example, in two variables ($n=2$), a quadratic form looks like:
$Q(x_1, x_2) = a x_1^2 + b x_1 x_2 + c x_2^2$

This can be written in matrix form as:
$Q(x_1, x_2) = \begin{bmatrix} x_1 & x_2 \end{bmatrix} \begin{bmatrix} a & b/2 \\ b/2 & c \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$

Notice that the off-diagonal entries of the matrix $A$ are half the coefficient of the cross-term ($x_1 x_2$). We use a symmetric matrix $A$ because for any matrix $B$, $\mathbf{x}^T B \mathbf{x} = \mathbf{x}^T \left( \frac{B + B^T}{2} \right) \mathbf{x}$, and $\frac{B + B^T}{2}$ is always a symmetric matrix. Using the symmetric form simplifies many properties and theorems related to quadratic forms.

**Key Aspects of Quadratic Forms:**

* **Matrix Representation:** Every quadratic form can be uniquely represented by a symmetric matrix.
* **Evaluation:** The value of the quadratic form $Q(\mathbf{x})$ is a scalar obtained by the matrix multiplication $\mathbf{x}^T A \mathbf{x}$.
* **Classification:** Quadratic forms can be classified based on the values they take for non-zero vectors $\mathbf{x}$:
    * **Positive definite:** $Q(\mathbf{x}) > 0$ for all $\mathbf{x} \neq \mathbf{0}$. This occurs if and only if all eigenvalues of $A$ are positive.
    * **Positive semidefinite:** $Q(\mathbf{x}) \ge 0$ for all $\mathbf{x}$. This occurs if and only if all eigenvalues of $A$ are non-negative.
    * **Negative definite:** $Q(\mathbf{x}) < 0$ for all $\mathbf{x} \neq \mathbf{0}$. This occurs if and only if all eigenvalues of $A$ are negative.
    * **Negative semidefinite:** $Q(\mathbf{x}) \le 0$ for all $\mathbf{x}$. This occurs if and only if all eigenvalues of $A$ are non-positive.
    * **Indefinite:** $Q(\mathbf{x})$ takes both positive and negative values. This occurs if and only if $A$ has both positive and negative eigenvalues.
* **Change of Variables:** By performing a linear change of variables $\mathbf{x} = P\mathbf{y}$, where $P$ is an invertible matrix, the quadratic form can be transformed into a new quadratic form in terms of $\mathbf{y}$ with a different matrix representation ($P^T A P$). A key goal is often to find an orthogonal transformation (where $P$ is an orthogonal matrix) that diagonalizes the matrix $A$, resulting in a quadratic form with no cross-terms (only squared terms). This is related to the Principal Axis Theorem.

**Applications of Quadratic Forms:**

Quadratic forms appear in various areas of mathematics, physics, statistics, and engineering, including:

* **Conic Sections and Quadric Surfaces:** The equations of these geometric objects can be expressed using quadratic forms.
* **Optimization:** Determining the nature of critical points of multivariable functions often involves analyzing the quadratic form of the Hessian matrix.
* **Stability Analysis:** In dynamical systems, quadratic forms (like Lyapunov functions) are used to analyze the stability of equilibrium points.
* **Statistics:** Covariance matrices define quadratic forms that describe the spread and correlation of data.
* **Mechanics and Physics:** Kinetic and potential energy in some systems can be expressed as quadratic forms.

In summary, a quadratic form is a fundamental concept in linear algebra that provides a way to express and analyze homogeneous quadratic polynomials using the language of vectors and matrices. Its matrix representation and classification based on definiteness are crucial for understanding its properties and applications.
