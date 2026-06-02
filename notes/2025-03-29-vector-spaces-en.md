---
audio: false
generated: true
lang: en
layout: post
title: Tutorial on Vector Spaces in Linear Algebra
translated: false
type: note
---

This tutorial covers key concepts related to **vector spaces**, including **subspaces, basis, dimension, and linear independence**. These topics are fundamental in linear algebra and are essential for understanding more advanced concepts.

---

### **1. Vector Spaces**

A **vector space** (or linear space) is a set of vectors that satisfies certain properties under vector addition and scalar multiplication.

#### **Definition**

A vector space \\( V \\) over a field \\( \mathbb{F} \\) (e.g., real numbers \\( \mathbb{R} \\) or complex numbers \\( \mathbb{C} \\)) is a set of elements (vectors) along with two operations:

- **Vector Addition:** \\( \mathbf{u} + \mathbf{v} \\) for \\( \mathbf{u}, \mathbf{v} \in V \\).
- **Scalar Multiplication:** \\( c \mathbf{v} \\) for \\( c \in \mathbb{F} \\) and \\( \mathbf{v} \in V \\).

These operations must satisfy the following **axioms**:

1. **Associativity of Addition:** \\( (\mathbf{u} + \mathbf{v}) + \mathbf{w} = \mathbf{u} + (\mathbf{v} + \mathbf{w}) \\).
2. **Commutativity of Addition:** \\( \mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u} \\).
3. **Existence of Zero Vector:** There exists a vector \\( \mathbf{0} \\) such that \\( \mathbf{v} + \mathbf{0} = \mathbf{v} \\) for all \\( \mathbf{v} \\).
4. **Existence of Additive Inverses:** For every \\( \mathbf{v} \\), there exists \\( -\mathbf{v} \\) such that \\( \mathbf{v} + (-\mathbf{v}) = \mathbf{0} \\).
5. **Distributivity of Scalar Multiplication over Vector Addition:** \\( c(\mathbf{u} + \mathbf{v}) = c\mathbf{u} + c\mathbf{v} \\).
6. **Distributivity of Scalar Multiplication over Field Addition:** \\( (a + b) \mathbf{v} = a\mathbf{v} + b\mathbf{v} \\).
7. **Associativity of Scalar Multiplication:** \\( a(b\mathbf{v}) = (ab)\mathbf{v} \\).
8. **Multiplicative Identity:** \\( 1 \mathbf{v} = \mathbf{v} \\).

#### **Examples of Vector Spaces**

1. \\( \mathbb{R}^n \\) (n-dimensional Euclidean space)
2. The space of polynomials of degree \\( \leq n \\).
3. The set of \\( m \times n \\) matrices.
4. The set of continuous functions.

---

### **2. Subspaces**

A **subspace** is a subset \\( W \\) of a vector space \\( V \\) that is itself a vector space under the same operations.

#### **Subspace Conditions**

A non-empty subset \\( W \\) of \\( V \\) is a subspace if:

1. **Closed under addition:** If \\( \mathbf{u}, \mathbf{v} \in W \\), then \\( \mathbf{u} + \mathbf{v} \in W \\).
2. **Closed under scalar multiplication:** If \\( \mathbf{v} \in W \\) and \\( c \in \mathbb{F} \\), then \\( c\mathbf{v} \in W \\).

#### **Examples of Subspaces**

1. The set of all vectors in \\( \mathbb{R}^3 \\) of the form \\( (x, 0, 0) \\).
2. The set of all polynomials with only even-degree terms.
3. The set of solutions to a homogeneous linear equation.

---

### **3. Linear Independence**

A set of vectors \\( \{ \mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_k \} \\) in \\( V \\) is **linearly dependent** if there exist scalars \\( c_1, c_2, \dots, c_k \\), **not all zero**, such that:

\\[
c_1 \mathbf{v}_1 + c_2 \mathbf{v}_2 + \dots + c_k \mathbf{v}_k = 0
\\]

If the only solution to this equation is \\( c_1 = c_2 = \dots = c_k = 0 \\), the vectors are **linearly independent**.

#### **Examples**

- The vectors \\( (1,0) \\) and \\( (0,1) \\) in \\( \mathbb{R}^2 \\) are **linearly independent**.
- The vectors \\( (1,1) \\), \\( (2,2) \\) in \\( \mathbb{R}^2 \\) are **linearly dependent** because \\( 2(1,1) - (2,2) = (0,0) \\).

---

### **4. Basis of a Vector Space**

A **basis** of a vector space \\( V \\) is a set of **linearly independent vectors** that **span** \\( V \\). This means:

1. The basis vectors are linearly independent.
2. Every vector in \\( V \\) can be expressed as a linear combination of the basis vectors.

#### **Examples**

1. The **standard basis** for \\( \mathbb{R}^2 \\) is \\( \{ (1,0), (0,1) \} \\).
2. The **standard basis** for \\( \mathbb{R}^3 \\) is \\( \{ (1,0,0), (0,1,0), (0,0,1) \} \\).

---

### **5. Dimension of a Vector Space**

The **dimension** of a vector space \\( V \\), denoted \\( \dim(V) \\), is the number of vectors in any basis for \\( V \\).

#### **Examples**

- \\( \dim(\mathbb{R}^n) = n \\).
- The space of polynomials of degree \\( \leq 2 \\) has dimension **3**, with basis \\( \{1, x, x^2\} \\).
- The set of solutions to a homogeneous system of 3 equations in 5 unknowns forms a subspace of dimension **2**.

---

### **Summary of Key Points**

| Concept | Definition |
|---------|-----------|
| **Vector Space** | A set of vectors closed under addition and scalar multiplication. |
| **Subspace** | A subset of a vector space that is itself a vector space. |
| **Linear Independence** | A set of vectors is independent if no vector can be written as a linear combination of the others. |
| **Basis** | A minimal set of vectors that spans the vector space. |
| **Dimension** | The number of vectors in a basis of the space. |

---

### **Practice Problems**

1. Determine whether the set of vectors \\( \{(1,2,3), (4,5,6), (7,8,9)\} \\) in \\( \mathbb{R}^3 \\) is linearly independent.
2. Find a basis for the subspace of \\( \mathbb{R}^3 \\) spanned by \\( \{(1,2,3), (2,4,6)\} \\).
3. Find the dimension of the space of solutions to the system:
   \\[
   x + y + z = 0
   \\]
   \\[
   2x + 3y + 5z = 0
   \\]
4. Verify whether the set \\( \{1, x, x^2, x^3\} \\) forms a basis for the space of polynomials of degree \\( \leq 3 \\).

Let me know if you need explanations for any of these problems! 🚀
