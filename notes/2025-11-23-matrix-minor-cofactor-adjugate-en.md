---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5.1
title: Matrix Minor, Cofactor, and Adjugate Guide
translated: false
type: note
---

Here’s a clean way to untangle **minor**, **cofactor**, **cofactor matrix**, and **adjugate** so you never mix them again.

---

## 1. Minor

For an entry at position ((i,j)) in a matrix (A):

* **Minor (M_{ij})** = determinant of the matrix you get **after deleting row (i) and column (j)**.
* No signs involved.
* No (a_{ij}) involved.

So:
[
M_{ij} = \det(A \text{ without row } i \text{ and column } j)
]

---

## 2. Cofactor

For the same entry:

* **Cofactor (C_{ij})** = sign factor ( (-1)^{i+j} ) multiplied by the **minor**.

So:
[
C_{ij} = (-1)^{i+j} M_{ij}
]

Still no multiplying by the original matrix entry (a_{ij}).
That is only in the Laplace expansion of det(A), not in the definition of cofactors.

---

## 3. Cofactor Matrix

Make a matrix out of all the cofactors:

[
\text{Cof}(A) =
\begin{bmatrix}
C_{11} & C_{12} & \cdots \
C_{21} & C_{22} & \cdots \
\vdots & \vdots
\end{bmatrix}
]

Nothing is flipped here. Just list the cofactors in their original positions.

---

## 4. Adjugate (a.k.a. Adjoint)

The **adjugate** is simply the transpose of the cofactor matrix:

[
\operatorname{adj}(A) = \text{Cof}(A)^\mathsf{T}
]

That’s *the only difference*: you swap rows and columns.

---

## 5. Where does the (a_{ij}) multiplication appear?

You only multiply by (a_{ij}) when expanding **determinant** along a row or column:

[
\det(A) = \sum_{j=1}^n a_{ij} C_{ij}
]

or

[
\det(A) = \sum_{i=1}^n a_{ij} C_{ij}
]

That’s **not** part of the definition of the cofactor.

---

## 6. Quick mental summary (no tables)

* Remove row (i), column (j) → **minor**.
* Multiply by sign → **cofactor**.
* Collect all cofactors → **cofactor matrix**.
* Transpose that → **adjugate**.
* Multiply by (a_{ij}) only when computing **determinant**.

---

If you want, I can also give you a concrete 3×3 example that shows all four objects at once.
