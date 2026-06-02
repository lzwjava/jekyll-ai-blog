---
audio: false
generated: true
lang: en
layout: post
title: Linear Transformations - Gemini
translated: false
type: note
---

Okay, let's dive into a detailed tutorial on linear transformations, covering the definition, examples, matrix representation, kernel, image, and properties like injectivity and surjectivity. This is a fundamental topic in linear algebra.

## 6. Linear Transformations: A Detailed Tutorial

A **linear transformation** is a function between two vector spaces that preserves the operations of vector addition and scalar multiplication. Let \\(V\\) and \\(W\\) be vector spaces over the same field \\(F\\) (which is often the set of real numbers \\(\mathbb{R}\\) or complex numbers \\(\mathbb{C}\\)).

**Definition:** A function \\(T: V \rightarrow W\\) is a linear transformation if it satisfies the following two properties for all vectors \\(\mathbf{u}, \mathbf{v} \in V\\) and all scalars \\(c \in F\\):

1.  **Additivity:** \\(T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})\\)
2.  **Homogeneity (Scalar Multiplication):** \\(T(c\mathbf{u}) = cT(\mathbf{u})\\)

These two properties can be combined into a single condition:
\\(T(c\mathbf{u} + d\mathbf{v}) = cT(\mathbf{u}) + dT(\mathbf{v})\\) for all \\(\mathbf{u}, \mathbf{v} \in V\\) and all scalars \\(c, d \in F\\).

**Key Consequences of Linearity:**

* \\(T(\mathbf{0}_V) = \mathbf{0}_W\\), where \\(\mathbf{0}_V\\) is the zero vector in \\(V\\) and \\(\mathbf{0}_W\\) is the zero vector in \\(W\\). (Proof: \\(T(\mathbf{0}_V) = T(0\mathbf{u}) = 0T(\mathbf{u}) = \mathbf{0}_W\\) for any \\(\mathbf{u} \in V\\)).
* \\(T(-\mathbf{u}) = -T(\mathbf{u})\\). (Proof: \\(T(-\mathbf{u}) = T((-1)\mathbf{u}) = (-1)T(\mathbf{u}) = -T(\mathbf{u})\\)).

### Examples of Linear Transformations

Let's look at some examples to understand the concept better.

**Example 1: Transformation in \\(\mathbb{R}^2\\) (Rotation)**

Consider a transformation \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^2\\) that rotates every vector in \\(\mathbb{R}^2\\) counterclockwise by an angle \\(\theta\\). If \\(\mathbf{v} = \begin{pmatrix} x \\ y \end{pmatrix}\\), then \\(T(\mathbf{v}) = \begin{pmatrix} x\cos\theta - y\sin\theta \\ x\sin\theta + y\cos\theta \end{pmatrix}\\).

Let's check if this is a linear transformation. Let \\(\mathbf{u} = \begin{pmatrix} x_1 \\ y_1 \end{pmatrix}\\) and \\(\mathbf{v} = \begin{pmatrix} x_2 \\ y_2 \end{pmatrix}\\), and let \\(c\\) be a scalar.

* **Additivity:**
    \\(T(\mathbf{u} + \mathbf{v}) = T\left(\begin{pmatrix} x_1 + x_2 \\ y_1 + y_2 \end{pmatrix}\right) = \begin{pmatrix} (x_1 + x_2)\cos\theta - (y_1 + y_2)\sin\theta \\ (x_1 + x_2)\sin\theta + (y_1 + y_2)\cos\theta \end{pmatrix}\\)
    \\(= \begin{pmatrix} (x_1\cos\theta - y_1\sin\theta) + (x_2\cos\theta - y_2\sin\theta) \\ (x_1\sin\theta + y_1\cos\theta) + (x_2\sin\theta + y_2\cos\theta) \end{pmatrix} = T(\mathbf{u}) + T(\mathbf{v})\\)

* **Homogeneity:**
    \\(T(c\mathbf{u}) = T\left(\begin{pmatrix} cx_1 \\ cy_1 \end{pmatrix}\right) = \begin{pmatrix} (cx_1)\cos\theta - (cy_1)\sin\theta \\ (cx_1)\sin\theta + (cy_1)\cos\theta \end{pmatrix}\\)
    \\(= \begin{pmatrix} c(x_1\cos\theta - y_1\sin\theta) \\ c(x_1\sin\theta + y_1\cos\theta) \end{pmatrix} = c \begin{pmatrix} x_1\cos\theta - y_1\sin\theta \\ x_1\sin\theta + y_1\cos\theta \end{pmatrix} = cT(\mathbf{u})\\)

Thus, rotation is a linear transformation.

**Example 2: Transformation in \\(\mathbb{R}^2\\) (Projection onto the x-axis)**

Consider \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^2\\) defined by \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x \\ 0 \end{pmatrix}\\). This transformation projects every vector onto the x-axis. You can verify that this is also a linear transformation using the definition.

**Example 3: Transformation in \\(\mathbb{R}^2\\) (Translation)**

Consider \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^2\\) defined by \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + a \\ y + b \end{pmatrix}\\), where \\(a\\) and \\(b\\) are constants (not both zero).

Let's check the first property:
\\(T(\mathbf{u} + \mathbf{v}) = T\left(\begin{pmatrix} x_1 + x_2 \\ y_1 + y_2 \end{pmatrix}\right) = \begin{pmatrix} (x_1 + x_2) + a \\ (y_1 + y_2) + b \end{pmatrix} = \begin{pmatrix} x_1 + a + x_2 + a \\ y_1 + b + y_2 + b \end{pmatrix}\\)
\\(T(\mathbf{u}) + T(\mathbf{v}) = \begin{pmatrix} x_1 + a \\ y_1 + b \end{pmatrix} + \begin{pmatrix} x_2 + a \\ y_2 + b \end{pmatrix} = \begin{pmatrix} x_1 + a + x_2 + a \\ y_1 + b + y_2 + b \end{pmatrix}\\)

This seems correct, let's recheck.
\\(T(\mathbf{u} + \mathbf{v}) = \begin{pmatrix} x_1 + x_2 + a \\ y_1 + y_2 + b \end{pmatrix}\\)
\\(T(\mathbf{u}) + T(\mathbf{v}) = \begin{pmatrix} x_1 + a \\ y_1 + b \end{pmatrix} + \begin{pmatrix} x_2 + a \\ y_2 + b \end{pmatrix} = \begin{pmatrix} x_1 + x_2 + 2a \\ y_1 + y_2 + 2b \end{pmatrix}\\)

If \\(a \neq 0\\) or \\(b \neq 0\\), then \\(T(\mathbf{u} + \mathbf{v}) \neq T(\mathbf{u}) + T(\mathbf{v})\\). Also, \\(T(\mathbf{0}) = T\left(\begin{pmatrix} 0 \\ 0 \end{pmatrix}\right) = \begin{pmatrix} a \\ b \end{pmatrix} \neq \begin{pmatrix} 0 \\ 0 \end{pmatrix}\\) if \\(a\\) or \\(b\\) is non-zero. Therefore, translation is generally **not** a linear transformation.

**Example 4: Transformation from \\(\mathbb{R}^n\\) to \\(\mathbb{R}^m\\) defined by a matrix**

Let \\(A\\) be an \\(m \times n\\) matrix. The transformation \\(T: \mathbb{R}^n \rightarrow \mathbb{R}^m\\) defined by \\(T(\mathbf{x}) = A\mathbf{x}\\) (where \\(\mathbf{x}\\) is an \\(n \times 1\\) column vector) is a linear transformation. This is because matrix multiplication satisfies the properties of additivity and homogeneity:
\\(A(\mathbf{u} + \mathbf{v}) = A\mathbf{u} + A\mathbf{v}\\)
\\(A(c\mathbf{u}) = c(A\mathbf{u})\\)

**Example 5: Differentiation of Polynomials**

Let \\(P_n\\) be the vector space of polynomials of degree at most \\(n\\). The transformation \\(D: P_n \rightarrow P_{n-1}\\) defined by \\(D(p(x)) = p'(x)\\) (the derivative of \\(p(x)\\)) is a linear transformation.
If \\(p(x)\\) and \\(q(x)\\) are polynomials and \\(c\\) is a scalar:
\\(D(p(x) + q(x)) = (p(x) + q(x))' = p'(x) + q'(x) = D(p(x)) + D(q(x))\\)
\\(D(cp(x)) = (cp(x))' = cp'(x) = cD(p(x))\\)

**Example 6: Integration of Functions**

Let \\(C[a, b]\\) be the vector space of continuous functions on the interval \\([a, b]\\). The transformation \\(I: C[a, b] \rightarrow \mathbb{R}\\) defined by \\(I(f) = \int_a^b f(x) dx\\) is a linear transformation.
\\(I(f + g) = \int_a^b (f(x) + g(x)) dx = \int_a^b f(x) dx + \int_a^b g(x) dx = I(f) + I(g)\\)
\\(I(cf) = \int_a^b cf(x) dx = c \int_a^b f(x) dx = cI(f)\\)

### Matrix Representation of a Linear Transformation

A fundamental result in linear algebra is that any linear transformation between finite-dimensional vector spaces can be represented by a matrix.

Let \\(V\\) be an \\(n\\)-dimensional vector space with basis \\(\mathcal{B} = \{\mathbf{b}_1, \mathbf{b}_2, ..., \mathbf{b}_n\}\\) and \\(W\\) be an \\(m\\)-dimensional vector space with basis \\(\mathcal{C} = \{\mathbf{c}_1, \mathbf{c}_2, ..., \mathbf{c}_m\}\\). Let \\(T: V \rightarrow W\\) be a linear transformation.

To find the matrix representation of \\(T\\) with respect to the bases \\(\mathcal{B}\\) and \\(\mathcal{C}\\) (denoted as \\([T]_{\mathcal{B}}^{\mathcal{C}}\\) or simply \\([T]\\) when the bases are understood), we need to determine the images of the basis vectors of \\(V\\) under \\(T\\) and express these images as linear combinations of the basis vectors of \\(W\\).

For each \\(\mathbf{b}_j \in \mathcal{B}\\), \\(T(\mathbf{b}_j)\\) is a vector in \\(W\\), so it can be uniquely written as a linear combination of the basis vectors in \\(\mathcal{C}\\):
\\(T(\mathbf{b}_j) = a_{1j}\mathbf{c}_1 + a_{2j}\mathbf{c}_2 + ... + a_{mj}\mathbf{c}_m = \sum_{i=1}^{m} a_{ij}\mathbf{c}_i\\)

The coefficients of this linear combination form the \\(j\\)-th column of the matrix representation \\([T]_{\mathcal{B}}^{\mathcal{C}}\\):
$[T]_{\mathcal{B}}^{\mathcal{C}} = \begin{pmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{pmatrix}$

If \\(\mathbf{v} \in V\\) has a coordinate vector \\([\mathbf{v}]_{\mathcal{B}} = \begin{pmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{pmatrix}\\) with respect to the basis \\(\mathcal{B}\\), then the coordinate vector of \\(T(\mathbf{v})\\) with respect to the basis \\(\mathcal{C}\\), denoted as \\([T(\mathbf{v})]_{\mathcal{C}}\\), is given by the matrix product:
\\([T(\mathbf{v})]_{\mathcal{C}} = [T]_{\mathcal{B}}^{\mathcal{C}} [\mathbf{v}]_{\mathcal{B}}\\)

**Example: Matrix Representation**

Let \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^3\\) be a linear transformation defined by \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\). Let the standard bases for \\(\mathbb{R}^2\\) and \\(\mathbb{R}^3\\) be \\(\mathcal{B} = \{\mathbf{e}_1, \mathbf{e}_2\} = \left\{ \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \begin{pmatrix} 0 \\ 1 \end{pmatrix} \right\}\\) and \\(\mathcal{C} = \{\mathbf{f}_1, \mathbf{f}_2, \mathbf{f}_3\} = \left\{ \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix}, \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}, \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix} \right\}\\).

We find the images of the basis vectors of \\(\mathbb{R}^2\\) under \\(T\\):
\\(T(\mathbf{e}_1) = T\left(\begin{pmatrix} 1 \\ 0 \end{pmatrix}\right) = \begin{pmatrix} 1 + 0 \\ 2(1) - 0 \\ 3(0) \end{pmatrix} = \begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix} = 1\mathbf{f}_1 + 2\mathbf{f}_2 + 0\mathbf{f}_3\\)
\\(T(\mathbf{e}_2) = T\left(\begin{pmatrix} 0 \\ 1 \end{pmatrix}\right) = \begin{pmatrix} 0 + 1 \\ 2(0) - 1 \\ 3(1) \end{pmatrix} = \begin{pmatrix} 1 \\ -1 \\ 3 \end{pmatrix} = 1\mathbf{f}_1 - 1\mathbf{f}_2 + 3\mathbf{f}_3\\)

The matrix representation of \\(T\\) with respect to the standard bases is:
\\([T]_{\mathcal{B}}^{\mathcal{C}} = \begin{pmatrix} 1 & 1 \\ 2 & -1 \\ 0 & 3 \end{pmatrix}\\)

Now, let's take an arbitrary vector \\(\mathbf{v} = \begin{pmatrix} x \\ y \end{pmatrix}\\) in \\(\mathbb{R}^2\\). Its coordinate vector with respect to \\(\mathcal{B}\\) is \\([\mathbf{v}]_{\mathcal{B}} = \begin{pmatrix} x \\ y \end{pmatrix}\\).
\\([T(\mathbf{v})]_{\mathcal{C}} = [T]_{\mathcal{B}}^{\mathcal{C}} [\mathbf{v}]_{\mathcal{B}} = \begin{pmatrix} 1 & 1 \\ 2 & -1 \\ 0 & 3 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\)
The coordinate vector with respect to \\(\mathcal{C}\\) is indeed \\(\begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\), which corresponds to the vector \\(T(\mathbf{v})\\) we defined earlier.

### Kernel (Null Space) of a Linear Transformation

The **kernel** (or null space) of a linear transformation \\(T: V \rightarrow W\\), denoted by \\(\text{ker}(T)\\) or \\(N(T)\\), is the set of all vectors in \\(V\\) that are mapped to the zero vector in \\(W\\):
\\(\text{ker}(T) = \{\mathbf{v} \in V \mid T(\mathbf{v}) = \mathbf{0}_W\}\\)

**Properties of the Kernel:**

* The kernel of a linear transformation is always a subspace of the domain \\(V\\).
    * **Contains the zero vector:** \\(T(\mathbf{0}_V) = \mathbf{0}_W\\), so \\(\mathbf{0}_V \in \text{ker}(T)\\).
    * **Closed under addition:** If \\(\mathbf{u}, \mathbf{v} \in \text{ker}(T)\\), then \\(T(\mathbf{u}) = \mathbf{0}_W\\) and \\(T(\mathbf{v}) = \mathbf{0}_W\\). Thus, \\(T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v}) = \mathbf{0}_W + \mathbf{0}_W = \mathbf{0}_W\\), so \\(\mathbf{u} + \mathbf{v} \in \text{ker}(T)\\).
    * **Closed under scalar multiplication:** If \\(\mathbf{u} \in \text{ker}(T)\\) and \\(c\\) is a scalar, then \\(T(c\mathbf{u}) = cT(\mathbf{u}) = c\mathbf{0}_W = \mathbf{0}_W\\), so \\(c\mathbf{u} \in \text{ker}(T)\\).

**Example: Finding the Kernel**

Consider the linear transformation \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^3\\) defined by \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\).
To find the kernel, we need to solve \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}\\):
\\(\begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}\\)

This gives the system of linear equations:
\\(x + y = 0\\)
\\(2x - y = 0\\)
\\(3y = 0\\)

From the third equation, \\(y = 0\\). Substituting this into the first equation, \\(x + 0 = 0\\), so \\(x = 0\\). The second equation is also satisfied: \\(2(0) - 0 = 0\\).
The only solution is \\(x = 0\\) and \\(y = 0\\). Therefore, \\(\text{ker}(T) = \left\{ \begin{pmatrix} 0 \\ 0 \end{pmatrix} \right\}\\), which is the zero subspace of \\(\mathbb{R}^2\\).

### Image (Range) of a Linear Transformation

The **image** (or range) of a linear transformation \\(T: V \rightarrow W\\), denoted by \\(\text{im}(T)\\) or \\(R(T)\\), is the set of all vectors in \\(W\\) that are the image of some vector in \\(V\\):
\\(\text{im}(T) = \{\mathbf{w} \in W \mid \mathbf{w} = T(\mathbf{v}) \text{ for some } \mathbf{v} \in V\}\\)

**Properties of the Image:**

* The image of a linear transformation is always a subspace of the codomain \\(W\\).
    * **Contains the zero vector:** \\(T(\mathbf{0}_V) = \mathbf{0}_W\\), so \\(\mathbf{0}_W \in \text{im}(T)\\).
    * **Closed under addition:** If \\(\mathbf{w}_1, \mathbf{w}_2 \in \text{im}(T)\\), then there exist \\(\mathbf{v}_1, \mathbf{v}_2 \in V\\) such that \\(T(\mathbf{v}_1) = \mathbf{w}_1\\) and \\(T(\mathbf{v}_2) = \mathbf{w}_2\\). Then \\(\mathbf{w}_1 + \mathbf{w}_2 = T(\mathbf{v}_1) + T(\mathbf{v}_2) = T(\mathbf{v}_1 + \mathbf{v}_2)\\). Since \\(\mathbf{v}_1 + \mathbf{v}_2 \in V\\), \\(\mathbf{w}_1 + \mathbf{w}_2 \in \text{im}(T)\\).
    * **Closed under scalar multiplication:** If \\(\mathbf{w} \in \text{im}(T)\\) and \\(c\\) is a scalar, then there exists \\(\mathbf{v} \in V\\) such that \\(T(\mathbf{v}) = \mathbf{w}\\). Then \\(c\mathbf{w} = cT(\mathbf{v}) = T(c\mathbf{v})\\). Since \\(c\mathbf{v} \in V\\), \\(c\mathbf{w} \in \text{im}(T)\\).

* If \\(V\\) is finite-dimensional with a basis \\(\{\mathbf{b}_1, \mathbf{b}_2, ..., \mathbf{b}_n\}\\), then the image of \\(T\\) is the span of the images of the basis vectors:
    \\(\text{im}(T) = \text{span}\{T(\mathbf{b}_1), T(\mathbf{b}_2), ..., T(\mathbf{b}_n)\}\\)

**Example: Finding the Image**

Consider the linear transformation \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^3\\) defined by \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\).
Using the standard basis of \\(\mathbb{R}^2\\), \\(\{\begin{pmatrix} 1 \\ 0 \end{pmatrix}, \begin{pmatrix} 0 \\ 1 \end{pmatrix}\}\\), we have:
\\(T\left(\begin{pmatrix} 1 \\ 0 \end{pmatrix}\right) = \begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix}\\)
\\(T\left(\begin{pmatrix} 0 \\ 1 \end{pmatrix}\right) = \begin{pmatrix} 1 \\ -1 \\ 3 \end{pmatrix}\\)

The image of \\(T\\) is the span of these two vectors:
\\(\text{im}(T) = \text{span}\left\{ \begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix}, \begin{pmatrix} 1 \\ -1 \\ 3 \end{pmatrix} \right\}\\)
This is a subspace of \\(\mathbb{R}^3\\). Since these two vectors are linearly independent (one is not a scalar multiple of the other), the image is a plane passing through the origin in \\(\mathbb{R}^3\\).

**Relationship between Matrix Representation and Image:**

If \\(T: \mathbb{R}^n \rightarrow \mathbb{R}^m\\) is given by \\(T(\mathbf{x}) = A\mathbf{x}\\), where \\(A\\) is an \\(m \times n\\) matrix, then the image of \\(T\\) is the column space of the matrix \\(A\\), i.e., the span of the columns of \\(A\\).

### Properties of Linear Transformations: Injectivity and Surjectivity

**Injectivity (One-to-one)**

A linear transformation \\(T: V \rightarrow W\\) is **injective** (or one-to-one) if for every \\(\mathbf{w} \in W\\), there is at most one \\(\mathbf{v} \in V\\) such that \\(T(\mathbf{v}) = \mathbf{w}\\). Equivalently, if \\(T(\mathbf{u}) = T(\mathbf{v})\\), then \\(\mathbf{u} = \mathbf{v}\\).

**Theorem:** A linear transformation \\(T: V \rightarrow W\\) is injective if and only if its kernel is the zero subspace, i.e., \\(\text{ker}(T) = \{\mathbf{0}_V\}\\).

**Proof:**
* **(\\(\Rightarrow\\)) Assume \\(T\\) is injective.** If \\(\mathbf{v} \in \text{ker}(T)\\), then \\(T(\mathbf{v}) = \mathbf{0}_W\\). We also know that \\(T(\mathbf{0}_V) = \mathbf{0}_W\\). Since \\(T\\) is injective and \\(T(\mathbf{v}) = T(\mathbf{0}_V)\\), it must be that \\(\mathbf{v} = \mathbf{0}_V\\). Thus, \\(\text{ker}(T) = \{\mathbf{0}_V\}\\).
* **(\\(\Leftarrow\\)) Assume \\(\text{ker}(T) = \{\mathbf{0}_V\}\\).** Suppose \\(T(\mathbf{u}) = T(\mathbf{v})\\) for some \\(\mathbf{u}, \mathbf{v} \in V\\). Then \\(T(\mathbf{u}) - T(\mathbf{v}) = \mathbf{0}_W\\). By linearity, \\(T(\mathbf{u} - \mathbf{v}) = \mathbf{0}_W\\). This means that \\(\mathbf{u} - \mathbf{v} \in \text{ker}(T)\\). Since \\(\text{ker}(T) = \{\mathbf{0}_V\}\\), we have \\(\mathbf{u} - \mathbf{v} = \mathbf{0}_V\\), which implies \\(\mathbf{u} = \mathbf{v}\\). Therefore, \\(T\\) is injective.

**Example: Checking for Injectivity**

For the transformation \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^3\\) defined by \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\), we found that \\(\text{ker}(T) = \left\{ \begin{pmatrix} 0 \\ 0 \end{pmatrix} \right\}\\). Therefore, this transformation is injective.

**Surjectivity (Onto)**

A linear transformation \\(T: V \rightarrow W\\) is **surjective** (or onto) if for every \\(\mathbf{w} \in W\\), there exists at least one \\(\mathbf{v} \in V\\) such that \\(T(\mathbf{v}) = \mathbf{w}\\). In other words, the image of \\(T\\) is equal to the codomain \\(W\\), i.e., \\(\text{im}(T) = W\\).

**Theorem (Rank-Nullity Theorem):** For a linear transformation \\(T: V \rightarrow W\\), where \\(V\\) is a finite-dimensional vector space,
\\(\text{dim}(\text{ker}(T)) + \text{dim}(\text{im}(T)) = \text{dim}(V)\\)
Here, \\(\text{dim}(\text{ker}(T))\\) is called the **nullity** of \\(T\\), and \\(\text{dim}(\text{im}(T))\\) is called the **rank** of \\(T\\).

**Relationship between Surjectivity and Dimensions:**

If \\(T: V \rightarrow W\\) is a linear transformation between finite-dimensional vector spaces, then:
* If \\(\text{dim}(V) < \text{dim}(W)\\), \\(T\\) cannot be surjective. (By Rank-Nullity Theorem, \\(\text{dim}(\text{im}(T)) \leq \text{dim}(V) < \text{dim}(W)\\)).
* If \\(\text{dim}(V) > \text{dim}(W)\\), \\(T\\) cannot be injective (because \\(\text{dim}(\text{ker}(T)) = \text{dim}(V) - \text{dim}(\text{im}(T)) \geq \text{dim}(V) - \text{dim}(W) > 0\\), so the kernel is not just the zero vector).
* If \\(\text{dim}(V) = \text{dim}(W)\\), then \\(T\\) is injective if and only if it is surjective. (If \\(T\\) is injective, \\(\text{dim}(\text{ker}(T)) = 0\\), so \\(\text{dim}(\text{im}(T)) = \text{dim}(V) = \text{dim}(W)\\), meaning \\(\text{im}(T) = W\\), so \\(T\\) is surjective. Conversely, if \\(T\\) is surjective, \\(\text{dim}(\text{im}(T)) = \text{dim}(W) = \text{dim}(V)\\), so \\(\text{dim}(\text{ker}(T)) = 0\\), meaning \\(T\\) is injective).

**Example: Checking for Surjectivity**

For the transformation \\(T: \mathbb{R}^2 \rightarrow \mathbb{R}^3\\) defined by \\(T\left(\begin{pmatrix} x \\ y \end{pmatrix}\right) = \begin{pmatrix} x + y \\ 2x - y \\ 3y \end{pmatrix}\\), we found that \\(\text{im}(T) = \text{span}\left\{ \begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix}, \begin{pmatrix} 1 \\ -1 \\ 3 \end{pmatrix} \right\}\\). The dimension of the image (rank of \\(T\\)) is 2, as the two spanning vectors are linearly independent. The dimension of the domain is \\(\text{dim}(\mathbb{R}^2) = 2\\). By the Rank-Nullity Theorem, \\(\text{dim}(\text{ker}(T)) + \text{dim}(\text{im}(T)) = 2\\), so \\(\text{dim}(\text{ker}(T)) + 2 = 2\\), which gives \\(\text{dim}(\text{ker}(T)) = 0\\), consistent with our earlier finding.

Since the dimension of the image (2) is less than the dimension of the codomain (3), the image is a proper subspace of the codomain, and thus the transformation is not surjective. There are vectors in \\(\mathbb{R}^3\\) that are not in the image of \\(T\\). For example, \\(\begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}\\) cannot be expressed as a linear combination of \\(\begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix}\\) and \\(\begin{pmatrix} 1 \\ -1 \\ 3 \end{pmatrix}\\).

**Isomorphism**

A linear transformation \\(T: V \rightarrow W\\) is called an **isomorphism** if it is both injective and surjective. If there exists an isomorphism between two vector spaces \\(V\\) and \\(W\\), then \\(V\\) and \\(W\\) are said to be **isomorphic**, denoted by \\(V \cong W\\). Isomorphic vector spaces have essentially the same algebraic structure.

For finite-dimensional vector spaces, two vector spaces are isomorphic if and only if they have the same dimension. If \\(\text{dim}(V) = \text{dim}(W) = n\\), then a linear transformation \\(T: V \rightarrow W\\) is an isomorphism if and only if it is either injective or surjective.

**Summary of Key Concepts:**

* **Linear Transformation:** A function between vector spaces that preserves vector addition and scalar multiplication.
* **Matrix Representation:** A way to represent a linear transformation between finite-dimensional vector spaces as a matrix.
* **Kernel (Null Space):** The set of vectors in the domain that are mapped to the zero vector in the codomain. It is a subspace of the domain.
* **Image (Range):** The set of vectors in the codomain that are the image of some vector in the domain. It is a subspace of the codomain.
* **Injectivity (One-to-one):** A linear transformation is injective if and only if its kernel is the zero subspace.
* **Surjectivity (Onto):** A linear transformation is surjective if and only if its image is equal to the codomain.
* **Rank-Nullity Theorem:** For a linear transformation \\(T: V \rightarrow W\\) with finite-dimensional \\(V\\), \\(\text{dim}(\text{ker}(T)) + \text{dim}(\text{im}(T)) = \text{dim}(V)\\).
* **Isomorphism:** A linear transformation that is both injective and surjective.

This detailed tutorial should provide a solid foundation for understanding linear transformations. Remember to practice with various examples to solidify your understanding of these concepts. Good luck with your studies!
