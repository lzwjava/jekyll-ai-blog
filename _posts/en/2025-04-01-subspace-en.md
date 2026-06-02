---
audio: false
generated: true
lang: en
layout: post
title: Subspace
translated: false
type: note
---

To determine which of the given sets is a subspace of $\mathbb{R}^2$, we need to check if they satisfy the three conditions for a subspace:

1.  **The zero vector is in the subspace.**
2.  **The subspace is closed under vector addition.** If $\mathbf{u}$ and $\mathbf{v}$ are in the subspace, then $\mathbf{u} + \mathbf{v}$ is also in the subspace.
3.  **The subspace is closed under scalar multiplication.** If $\mathbf{u}$ is in the subspace and $c$ is any scalar, then $c\mathbf{u}$ is also in the subspace.

Let's examine each option:

**a) The line y = x + 1**

1.  **Zero vector:** The zero vector in $\mathbb{R}^2$ is $\begin{pmatrix} 0 \\ 0 \end{pmatrix}$. For this vector to be on the line, it must satisfy the equation $y = x + 1$. Substituting $x=0$ and $y=0$, we get $0 = 0 + 1$, which is $0 = 1$. This is false, so the zero vector is not on the line $y = x + 1$.

Since the first condition is not met, the line $y = x + 1$ is not a subspace of $\mathbb{R}^2$.

**b) The line y = 2x**

1.  **Zero vector:** For the zero vector $\begin{pmatrix} 0 \\ 0 \end{pmatrix}$ to be on the line, it must satisfy the equation $y = 2x$. Substituting $x=0$ and $y=0$, we get $0 = 2(0)$, which is $0 = 0$. This is true, so the zero vector is on the line $y = 2x$.

2.  **Closure under vector addition:** Let $\mathbf{u} = \begin{pmatrix} x_1 \\ y_1 \end{pmatrix}$ and $\mathbf{v} = \begin{pmatrix} x_2 \\ y_2 \end{pmatrix}$ be two vectors on the line $y = 2x$. This means $y_1 = 2x_1$ and $y_2 = 2x_2$.
    Their sum is $\mathbf{u} + \mathbf{v} = \begin{pmatrix} x_1 + x_2 \\ y_1 + y_2 \end{pmatrix}$. We need to check if this vector lies on the line $y = 2x$. Substituting the components, we get $y_1 + y_2 = 2(x_1 + x_2)$. Since $y_1 = 2x_1$ and $y_2 = 2x_2$, we have $2x_1 + 2x_2 = 2x_1 + 2x_2$, which is true. Thus, the line is closed under vector addition.

3.  **Closure under scalar multiplication:** Let $\mathbf{u} = \begin{pmatrix} x \\ y \end{pmatrix}$ be a vector on the line $y = 2x$, so $y = 2x$. Let $c$ be any scalar. Then $c\mathbf{u} = \begin{pmatrix} cx \\ cy \end{pmatrix}$. We need to check if this vector lies on the line $y = 2x$. Substituting the components, we get $cy = 2(cx)$. Since $y = 2x$, we have $c(2x) = 2(cx)$, which is $2cx = 2cx$. This is true, so the line is closed under scalar multiplication.

Since all three conditions are met, the line $y = 2x$ is a subspace of $\mathbb{R}^2$.

**c) The unit circle**

The unit circle in $\mathbb{R}^2$ is defined by the equation $x^2 + y^2 = 1$.

1.  **Zero vector:** The zero vector is $\begin{pmatrix} 0 \\ 0 \end{pmatrix}$. Substituting into the equation, we get $0^2 + 0^2 = 1$, which is $0 = 1$. This is false, so the zero vector is not on the unit circle.

Since the first condition is not met, the unit circle is not a subspace of $\mathbb{R}^2$.

Final Answer: The final answer is $\boxed{The line y = 2x}$

---

The requirement that "The zero vector is in the subspace" is one of the **three fundamental conditions** that a subset of a vector space must satisfy to be considered a **subspace**. Let's break down *why* this condition is necessary.

The concept of a subspace is about identifying smaller sets within a larger vector space that themselves behave like vector spaces. To behave like a vector space, these smaller sets must inherit certain essential properties. One of the most fundamental properties of any vector space is the existence of a **zero vector** (often denoted as $\mathbf{0}$). This vector has the crucial property that when added to any other vector in the space, it leaves that vector unchanged: $\mathbf{v} + \mathbf{0} = \mathbf{v}$ for all vectors $\mathbf{v}$ in the space.

Here's why the zero vector must be in a subspace:

1.  **Inheriting Vector Space Structure:** A subspace is meant to be a "mini-vector space" within a larger one. If a subset doesn't contain the zero vector, it lacks a crucial element required for it to satisfy the vector space axioms. Without a zero vector, the concept of additive inverses (another important axiom) becomes problematic.

2.  **Closure under Scalar Multiplication:** Consider a non-empty subset $W$ of a vector space $V$ that is closed under scalar multiplication. If $\mathbf{w}$ is any vector in $W$, and $W$ is a subspace, then for any scalar $c$, the vector $c\mathbf{w}$ must also be in $W$. If we choose the scalar $c = 0$, then $0\mathbf{w} = \mathbf{0}$ (this is a property of vector spaces). Therefore, if a subspace is closed under scalar multiplication and contains at least one vector, it *must* contain the zero vector.

3.  **Ensuring Additive Inverses:** While the presence of the zero vector alone doesn't guarantee the existence of additive inverses within the subspace, its absence creates a fundamental problem. If a vector $\mathbf{v}$ is in the subspace, and the subspace is closed under scalar multiplication, then $(-1)\mathbf{v} = -\mathbf{v}$ must also be in the subspace (this is the additive inverse of $\mathbf{v}$). For the addition of $\mathbf{v}$ and $-\mathbf{v}$ to result in a vector *within* the subspace, that resulting vector must be the zero vector. If the zero vector is not in the subset, then the closure under addition might be violated even if additive inverses exist within the larger vector space.

In simpler terms, if a subset doesn't even contain the "identity element" for vector addition (which is the zero vector), it can't really function as a self-contained system under vector addition and scalar multiplication, which are the defining operations of a vector space.

Therefore, the condition that the zero vector must be in the subspace is not arbitrary; it's a direct consequence of the requirement that a subspace must inherit the essential algebraic structure of the larger vector space it resides within.
