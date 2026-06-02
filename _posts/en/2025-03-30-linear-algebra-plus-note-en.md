---
audio: false
generated: true
lang: en
layout: post
title: Linear Algebra Plus Note
translated: false
type: note
---

In linear algebra, two square matrices \\( A \\) and \\( B \\) are said to be similar if there exists an invertible matrix \\( P \\) such that:

\\[ B = P^{-1}AP \\]

This relationship is known as a similarity transformation. The matrix \\( P \\) is called the change of basis matrix, and it transforms the matrix \\( A \\) into the matrix \\( B \\).

### Key Properties of Similar Matrices

1. **Same Eigenvalues**: Similar matrices have the same eigenvalues. This is because the eigenvalues are preserved under similarity transformations.
2. **Same Determinant**: The determinant of similar matrices is the same because \\(\det(P^{-1}AP) = \det(A)\\).
3. **Same Trace**: The trace (sum of the diagonal elements) of similar matrices is the same because \\(\text{tr}(P^{-1}AP) = \text{tr}(A)\\).
4. **Same Rank**: Similar matrices have the same rank.
5. **Same Characteristic Polynomial**: Similar matrices share the same characteristic polynomial.

### Intuition

Similar matrices represent the same linear transformation but in different bases. The matrix \\( P \\) can be thought of as a change of coordinates, transforming the basis in which the linear transformation is represented.

### Example

Consider two matrices \\( A \\) and \\( B \\):

\\[ A = \begin{pmatrix} 1 & 2 \\ 0 & 3 \end{pmatrix}, \quad B = \begin{pmatrix} 3 & 0 \\ 2 & 1 \end{pmatrix} \\]

To check if they are similar, we need to find an invertible matrix \\( P \\) such that \\( B = P^{-1}AP \\).

Would you like to see an example of how to find such a matrix \\( P \\) for specific matrices \\( A \\) and \\( B \\)?

---

Yes, the matrix:

\\[
A = \begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}
\\]

does indeed have a Singular Value Decomposition (SVD). Let's go through the process to find the SVD of this matrix.

### Step 1: Compute \\( A^T A \\)

First, we compute the matrix \\( A^T A \\):

\\[
A^T = \begin{bmatrix} 1 & 3 \\ 2 & 4 \end{bmatrix}
\\]

Now, multiply \\( A^T \\) and \\( A \\):

\\[
A^T A = \begin{bmatrix} 1 & 3 \\ 2 & 4 \end{bmatrix} \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} = \begin{bmatrix} 1 + 9 & 2 + 12 \\ 2 + 12 & 4 + 16 \end{bmatrix} = \begin{bmatrix} 10 & 14 \\ 14 & 20 \end{bmatrix}
\\]

### Step 2: Eigenvalues and Eigenvectors of \\( A^T A \\)

To find the singular values, we need the eigenvalues of \\( A^T A \\). We solve the characteristic equation \\( \text{det}(A^T A - \lambda I) = 0 \\):

\\[
\text{det}\begin{bmatrix} 10 - \lambda & 14 \\ 14 & 20 - \lambda \end{bmatrix} = 0
\\]

This gives:

\\[
(10 - \lambda)(20 - \lambda) - 14 \times 14 = 0
\\]

\\[
\lambda^2 - 30\lambda + 100 - 196 = 0
\\]

\\[
\lambda^2 - 30\lambda - 96 = 0
\\]

Solving this quadratic equation:

\\[
\lambda = \frac{-(-30) \pm \sqrt{(-30)^2 - 4(1)(-96)}}{2(1)} = \frac{30 \pm \sqrt{900 + 384}}{2} = \frac{30 \pm \sqrt{1284}}{2}
\\]

\\[
\lambda = \frac{30 \pm 35.86}{2}
\\]

Thus, the eigenvalues are:

\\[
\lambda_1 \approx 32.93 \quad \text{and} \quad \lambda_2 \approx 0.93
\\]

### Step 3: Compute Singular Values

The singular values are the square roots of the eigenvalues of \\( A^T A \\). Therefore, we have:

\\[
\sigma_1 = \sqrt{32.93} \approx 5.73 \quad \text{and} \quad \sigma_2 = \sqrt{0.93} \approx 0.96
\\]

### Step 4: Compute the Matrices \\( U \\) and \\( V \\)

To find the matrices \\( U \\) and \\( V \\), we need to compute the eigenvectors of \\( A^T A \\) and \\( A A^T \\), but since this requires detailed steps that go beyond the basic calculation, you would typically solve for them numerically.

However, based on the eigenvalues above, we know that the singular values are \\( 5.73 \\) and \\( 0.96 \\), and \\( U \\) and \\( V \\) would be orthogonal matrices corresponding to the eigenvectors of \\( A A^T \\) and \\( A^T A \\).

Thus, the SVD of the matrix \\( A \\) is:

\\[
A = U \Sigma V^T
\\]

Where:

- \\( \Sigma = \begin{bmatrix} 5.73 & 0 \\ 0 & 0.96 \end{bmatrix} \\)
- \\( U \\) and \\( V \\) are orthogonal matrices corresponding to the eigenvectors of \\( A A^T \\) and \\( A^T A \\).

You can find the exact values for \\( U \\) and \\( V \\) by solving the eigenvalue problems for \\( A^T A \\) and \\( A A^T \\).

---

The statement describes the behavior of the matrix as a linear transformation. Let's break it down to understand why this happens:

### Matrix as a Linear Transformation

- **Input Space**: The matrix operates on vectors from a 3-dimensional space (since it has 3 columns). This means it takes 3-component vectors as input.
- **Output Space**: The matrix maps these vectors to a 2-dimensional space (since it has 2 rows). This means it produces 2-component vectors as output.

### Null Space

- **Definition**: The null space (or kernel) of a matrix consists of all vectors that, when multiplied by the matrix, result in the zero vector.
- **Dimension**: The nullity of the matrix is the dimension of this null space. In this case, the nullity is 1, meaning there is a 1-dimensional subspace of vectors that get mapped to zero.
- **Interpretation**: This 1-dimensional subspace represents a line (in the 3-dimensional input space) of vectors that are "collapsed" or "squashed" to the zero vector in the 2-dimensional output space.

### Why This Happens

- **Rank-Nullity Theorem**: The theorem states that for any \\(m \times n\\) matrix, the rank (dimension of the column space) plus the nullity (dimension of the null space) equals the number of columns \\(n\\). Here, the rank is 2 and the number of columns is 3, so the nullity must be 1.
- **Linear Dependence**: The existence of a null space with dimension 1 indicates that there is some redundancy or linear dependence among the columns of the matrix. This means that one of the columns can be expressed as a linear combination of the other two.

### Visualization

- Imagine a 3D space where all points on a specific line (the null space) are mapped to the origin in a 2D space. This line represents the vectors that are "lost" or "ignored" by the transformation defined by the matrix.

This behavior is a fundamental aspect of linear transformations and highlights how matrices can reduce the dimensionality of the space they act upon.

---

To determine which option is necessary for a matrix to be diagonalizable, I'll examine each statement.

A square matrix A is diagonalizable if and only if there exists an invertible matrix P such that P⁻¹AP is a diagonal matrix. This happens precisely when A has a complete set of linearly independent eigenvectors.

Let's analyze each option:

a) The matrix must have at least one eigenvalue.
While all n×n matrices have at least one eigenvalue (in the complex field), this alone doesn't guarantee diagonalizability. A matrix could have eigenvalues but still not be diagonalizable if it doesn't have enough linearly independent eigenvectors.

b) The matrix must have distinct eigenvalues.
Having distinct eigenvalues is sufficient but not necessary for diagonalizability. A matrix with repeated eigenvalues can still be diagonalizable if it has enough linearly independent eigenvectors associated with those repeated eigenvalues.

c) The matrix must have enough linearly independent eigenvectors.
This is exactly the necessary and sufficient condition for diagonalizability. Specifically, an n×n matrix is diagonalizable if and only if it has n linearly independent eigenvectors, forming a basis for the vector space.

Therefore, option c) is the correct answer: a matrix is diagonalizable if and only if it has enough linearly independent eigenvectors.
