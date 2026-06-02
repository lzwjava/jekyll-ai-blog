---
audio: false
generated: false
image: false
lang: en
layout: post
title: Linear Algebra
translated: false
type: post
---

- Singular Value Decomposition can be used for image compression.

- The determinant of a matrix indicates how much the area changes when the matrix is applied to a shape.

- The eigenvalues are defined by the equation \\[ \det(\lambda I - A) = 0 \\].

- NumPy's `linalg` package can be used to study and solve problems in linear algebra.

- Use linear-algebra transforms in n-dimensional **space** to understand matrices.

- A matrix is a group of numbers arranged in rows and columns.

- The equation \\[ Ax = B \\] has a solution when \\[ \text{rank}(A) = \text{rank}([A or B]) \\].

- The rank of a matrix is the number of linearly independent rows (or columns) in its **echelon form**.

---

What is the use of the rank concept? It tells us how many rows retain information during a linear transformation. In contrast, the nullity (dimension of the null space) counts how many rows are mapped to zero.

What is the difference between a matrix and a plain array of numbers? An array has no inherent direction, whereas a matrix does.

What is the difference between a matrix and a vector? A vector is a one-dimensional column of numbers and has a direction.

Matrix multiplication follows a fixed rule: the number of columns in the first matrix must equal the number of rows in the second matrix. A 2×3 matrix multiplied by a 3×4 matrix yields a 2×4 matrix. In the resulting matrix, the value at position (i, j) is the dot product of the i-th row of matrix A and the j-th column of matrix B.

The determinant of a matrix carries meaning: if it is not equal to 0, the matrix is invertible.
