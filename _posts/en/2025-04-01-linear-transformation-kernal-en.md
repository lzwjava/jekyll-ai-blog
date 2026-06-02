---
audio: false
generated: true
lang: en
layout: post
title: The Kernel of a Linear Transformation
translated: false
type: note
---

The **kernel** of a linear transformation is the set of all input vectors that the transformation maps to the zero vector.

### Definition

If \\( T: V \to W \\) is a linear transformation between two vector spaces \\( V \\) and \\( W \\), then the **kernel** (or **null space**) of \\( T \\) is:

\\[
\ker(T) = \{ v \in V \mid T(v) = 0 \}
\\]

### Key Properties

1. **Subspace**: The kernel of a linear transformation is always a subspace of the domain \\( V \\).
2. **Dimension**: The dimension of the kernel is called the **nullity** of the transformation.
3. **Relation to Injectivity**:
   - If \\( \ker(T) = \{0\} \\), then \\( T \\) is **injective** (one-to-one).
   - If \\( \ker(T) \\) has dimension greater than zero, then \\( T \\) is not injective.

### Example

Consider the matrix transformation \\( T: \mathbb{R}^3 \to \mathbb{R}^2 \\) given by:

\\[
T(x, y, z) = (x + y, y + z)
\\]

Writing this as a matrix,

<div>
$$
T \begin{bmatrix} x \\ y \\ z \end{bmatrix} =
\begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \end{bmatrix}
\begin{bmatrix} x \\ y \\ z \end{bmatrix}
$$
</div>

To find the kernel, solve:

\\[
\begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \end{bmatrix}
\begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
\\]

This gives the system:

\\[
x + y = 0
\\]
\\[
y + z = 0
\\]

Solving for \\( x, y, z \\):

\\[
x = -y, \quad z = -y
\\]

Thus, the kernel consists of all vectors of the form:

<div>
$$
\ker(T) = \text{span} \left\{ \begin{bmatrix} -1 \\ 1 \\ -1 \end{bmatrix} \right\}
$$
</div>

which is a one-dimensional subspace of \\( \mathbb{R}^3 \\).

Let me know if you need further clarification!
