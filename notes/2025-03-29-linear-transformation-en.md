---
audio: false
generated: true
lang: en
layout: post
title: Linear Transformations
translated: false
type: note
---

**Definition, Examples, Matrix Representation, Kernel, Image, Properties (Injectivity, Surjectivity)**

Linear transformations are fundamental in linear algebra, providing a bridge between vector spaces and matrices. This tutorial covers:
- **Definition** of linear transformations
- **Examples** of common linear transformations
- **Matrix representation** of linear transformations
- **Kernel (null space)** and **Image (range)**
- **Properties**: Injectivity (one-to-one) and Surjectivity (onto)

---

## **1. Definition of a Linear Transformation**
A **linear transformation** (or linear map) between two vector spaces \\( V \\) and \\( W \\) over a field \\( \mathbb{F} \\) (usually \\( \mathbb{R} \\) or \\( \mathbb{C} \\)) is a function \\( T: V \to W \\) that satisfies:
1. **Additivity**:
   \\[
   T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v}) \quad \forall \mathbf{u}, \mathbf{v} \in V
   \\]
2. **Homogeneity (Scalar Multiplication)**:
   \\[
   T(c \mathbf{v}) = c T(\mathbf{v}) \quad \forall c \in \mathbb{F}, \mathbf{v} \in V
   \\]

**Key Idea**: Linear transformations preserve vector addition and scalar multiplication.

---

## **2. Examples of Linear Transformations**

### **(a) Zero Transformation**
- \\( T(\mathbf{v}) = \mathbf{0} \\) for all \\( \mathbf{v} \in V \\).

### **(b) Identity Transformation**
- \\( T(\mathbf{v}) = \mathbf{v} \\) for all \\( \mathbf{v} \in V \\).

### **(c) Rotation in \\( \mathbb{R}^2 \\)**
- Rotating a vector by angle \\( \theta \\):
  \\[
  T \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} \cos \theta & -\sin \theta \\ \sin \theta & \cos \theta \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix}
  \\]

### **(d) Differentiation (Polynomial Space)**
- \\( T: P_n \to P_{n-1} \\) where \\( T(p(x)) = p'(x) \\).

### **(e) Matrix Multiplication**
- For a fixed \\( m \times n \\) matrix \\( A \\), \\( T: \mathbb{R}^n \to \mathbb{R}^m \\) is defined by \\( T(\mathbf{x}) = A\mathbf{x} \\).

---

## **3. Matrix Representation of Linear Transformations**
Every linear transformation \\( T: \mathbb{R}^n \to \mathbb{R}^m \\) can be represented by an \\( m \times n \\) matrix \\( A \\) such that:
\\[
T(\mathbf{x}) = A\mathbf{x}
\\]

### **How to Find the Matrix \\( A \\)**
1. Apply \\( T \\) to the standard basis vectors \\( \mathbf{e}_1, \mathbf{e}_2, \dots, \mathbf{e}_n \\) of \\( \mathbb{R}^n \\).
2. The columns of \\( A \\) are \\( T(\mathbf{e}_1), T(\mathbf{e}_2), \dots, T(\mathbf{e}_n) \\).

**Example**:
Let \\( T: \mathbb{R}^2 \to \mathbb{R}^2 \\) be defined by:
\\[
T \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 2x + y \\ x - 3y \end{pmatrix}
\\]
- Compute \\( T(\mathbf{e}_1) = T(1, 0) = (2, 1) \\)
- Compute \\( T(\mathbf{e}_2) = T(0, 1) = (1, -3) \\)
- Thus, the matrix \\( A \\) is:
  \\[
  A = \begin{pmatrix} 2 & 1 \\ 1 & -3 \end{pmatrix}
  \\]

---

## **4. Kernel (Null Space) and Image (Range)**

### **(a) Kernel (Null Space)**
The **kernel** of \\( T \\) is the set of all vectors in \\( V \\) that map to \\( \mathbf{0} \\):
\\[
\ker(T) = \{ \mathbf{v} \in V \mid T(\mathbf{v}) = \mathbf{0} \}
\\]

**Properties**:
- \\( \ker(T) \\) is a subspace of \\( V \\).
- \\( T \\) is **injective (one-to-one)** if and only if \\( \ker(T) = \{ \mathbf{0} \} \\).

**Example**:
For \\( T(\mathbf{x}) = A\mathbf{x} \\) where \\( A = \begin{pmatrix} 1 & 2 \\ 3 & 6 \end{pmatrix} \\),
\\[
\ker(T) = \text{Span} \left\{ \begin{pmatrix} -2 \\ 1 \end{pmatrix} \right\}
\\]

### **(b) Image (Range)**
The **image** of \\( T \\) is the set of all outputs in \\( W \\):
\\[
\text{Im}(T) = \{ T(\mathbf{v}) \mid \mathbf{v} \in V \}
\\]

**Properties**:
- \\( \text{Im}(T) \\) is a subspace of \\( W \\).
- \\( T \\) is **surjective (onto)** if and only if \\( \text{Im}(T) = W \\).

**Example**:
For \\( T(\mathbf{x}) = A\mathbf{x} \\) where \\( A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{pmatrix} \\),
\\[
\text{Im}(T) = \text{Span} \left\{ \begin{pmatrix} 1 \\ 0 \\ 1 \end{pmatrix}, \begin{pmatrix} 0 \\ 1 \\ 1 \end{pmatrix} \right\}
\\]

---

## **5. Properties: Injectivity and Surjectivity**

### **(a) Injectivity (One-to-One)**
A linear transformation \\( T \\) is **injective** if:
\\[
T(\mathbf{u}) = T(\mathbf{v}) \implies \mathbf{u} = \mathbf{v}
\\]
**Test**:
- \\( T \\) is injective \\( \iff \ker(T) = \{ \mathbf{0} \} \\).
- If \\( \dim(V) < \dim(W) \\), \\( T \\) may not be injective.

### **(b) Surjectivity (Onto)**
A linear transformation \\( T \\) is **surjective** if:
\\[
\forall \mathbf{w} \in W, \exists \mathbf{v} \in V \text{ such that } T(\mathbf{v}) = \mathbf{w}
\\]
**Test**:
- \\( T \\) is surjective \\( \iff \text{Im}(T) = W \\).
- If \\( \dim(V) > \dim(W) \\), \\( T \\) may not be surjective.

### **(c) Rank-Nullity Theorem**
For \\( T: V \to W \\),
\\[
\dim(V) = \dim(\ker(T)) + \dim(\text{Im}(T))
\\]
- **Rank** \\( = \dim(\text{Im}(T)) \\)
- **Nullity** \\( = \dim(\ker(T)) \\)

**Example**:
If \\( T: \mathbb{R}^3 \to \mathbb{R}^2 \\) has \\( \dim(\ker(T)) = 1 \\), then \\( \dim(\text{Im}(T)) = 2 \\).

---

## **Summary**

| Concept | Definition | Key Property |
|---------|------------|--------------|
| **Linear Transformation** | \\( T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v}) \\) and \\( T(c\mathbf{v}) = cT(\mathbf{v}) \\) | Preserves linear structure |
| **Matrix Representation** | \\( T(\mathbf{x}) = A\mathbf{x} \\) where columns of \\( A \\) are \\( T(\mathbf{e}_i) \\) | Encodes transformation |
| **Kernel** | \\( \ker(T) = \{ \mathbf{v} \mid T(\mathbf{v}) = \mathbf{0} \} \\) | Measures injectivity |
| **Image** | \\( \text{Im}(T) = \{ T(\mathbf{v}) \mid \mathbf{v} \in V \} \\) | Measures surjectivity |
| **Injectivity** | \\( \ker(T) = \{ \mathbf{0} \} \\) | One-to-one |
| **Surjectivity** | \\( \text{Im}(T) = W \\) | Onto |

---

## **Practice Problems**
1. Find the matrix representation of \\( T(x, y, z) = (2x - y, y + 3z) \\).
2. Determine if \\( T(\mathbf{x}) = \begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix} \mathbf{x} \\) is injective/surjective.
3. Compute \\( \ker(T) \\) and \\( \text{Im}(T) \\) for \\( T(x, y) = (x + y, 2x - y, x) \\).

---

This tutorial covers the core concepts of linear transformations as typically taught in an undergraduate linear algebra course. Let me know if you need further clarification or additional examples!
