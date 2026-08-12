---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rank of a Matrix
translated: false
type: note
---

In linear algebra, the **rank of a matrix** is the number of **linearly independent rows or columns** in the matrix.

Informally, rank tells you **how much unique information** a matrix contains.

### Example 1

[
A=
\begin{bmatrix}
1 & 2\
2 & 4
\end{bmatrix}
]

The second row is just 2 times the first row, so the rows are not independent.

* Number of independent rows = 1
* Rank = 1

### Example 2

[
B=
\begin{bmatrix}
1 & 2\
3 & 4
\end{bmatrix}
]

Neither row can be made from the other, so both are independent.

* Number of independent rows = 2
* Rank = 2

### How to find rank

A common method is to perform **row reduction** (Gaussian elimination) and count the number of **pivot rows** (rows containing leading nonzero entries).

### Why rank matters

The rank tells you:

* Whether a system of equations has unique solutions, infinitely many solutions, or no solution.
* The dimension of the space spanned by the matrix's rows or columns.
* Whether a square matrix is invertible:

  * Full rank ⇒ invertible.
  * Not full rank ⇒ singular (not invertible).

For an (m \times n) matrix:

[
\text{rank}(A) \leq \min(m,n)
]

So, for a (3 \times 4) matrix, the maximum possible rank is 3.

**Simple definition:** Rank = the maximum number of rows (or columns) that are linearly independent.
