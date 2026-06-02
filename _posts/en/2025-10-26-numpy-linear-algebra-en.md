---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: NumPy Linear Algebra Pocket Guide
translated: false
type: note
---

As your engineering-focused tutor, this guide builds on the prior index-explicit formulations by integrating practical NumPy demonstrations via `import numpy as np` and `np.linalg`. All math remains verifiable with indices (e.g., \\( A = [a_{ij}]_{i=1}^2, j=1^2 \\)); code uses explicit arrays for clarity. Outputs are from verified executions (e.g., for \\( A = \begin{pmatrix} a_{11}=1 & a_{12}=2 \\ a_{21}=3 & a_{22}=4 \end{pmatrix} \\), \\( B = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix} \\)). Use these for quick computations in exam prep—focus on interpreting outputs against formulas.

## 1. Matrix Operations
Math as before: \\( (AB)_{ij} = \sum_{k=1}^2 a_{ik} b_{kj} \\), etc.

**NumPy Demo**:
```python
import numpy as np
A = np.array([[1, 2], [3, 4]], dtype=float)
B = np.array([[5, 6], [7, 8]], dtype=float)
```
- Addition: `A + B` yields \\( \begin{pmatrix} 6 & 8 \\ 10 & 12 \end{pmatrix} \\) (entry-wise \\( a_{ij} + b_{ij} \\)).
- Scalar: `2 * A` yields \\( \begin{pmatrix} 2 & 4 \\ 6 & 8 \end{pmatrix} \\) (\\( c a_{ij} \\)).
- Multiplication: `A @ B` (or `np.dot(A, B)`) yields \\( \begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix} \\) (verify: row1-col1 sum \\( 1\cdot5 + 2\cdot7 = 19 \\)). Note non-commutativity: `np.allclose(A @ B, B @ A)` is `False`.
- Transpose: `A.T` yields \\( \begin{pmatrix} 1 & 3 \\ 2 & 4 \end{pmatrix} \\) (\\( (A^T)_{ij} = a_{ji} \\)).
- Inverse: `np.linalg.inv(A)` yields \\( \begin{pmatrix} -2 & 1 \\ 1.5 & -0.5 \end{pmatrix} \\) (verify: `A @ inv_A` ≈ \\( I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} \\), with tiny float errors ~1e-16).

## 2. Determinants
Math: \\( \det A = \sum_{j=1}^2 a_{1j} C_{1j} \\), \\( C_{1j} = (-1)^{1+j} \det(M_{1j}) \\) (e.g., \\( M_{11} = [4] \\), so \\( C_{11} = 4 \\); full \\( \det A = 1\cdot4 - 2\cdot3 = -2 \\)).

**NumPy Demo** (continuing above):
- `np.linalg.det(A)`: -2.0 (matches formula; float precision -2.0000000000000004).
- Product: `np.linalg.det(A @ B)` = 4.0; `det_A * np.linalg.det(B)` ≈ 4.0 (verifies \\( \det(AB) = \det A \cdot \det B \\)).
- Transpose: `np.linalg.det(A.T)` = -2.0 (verifies \\( \det(A^T) = \det A \\)).

For adjugate/inverse link: Inverse uses det in denom, as in formula \\( A^{-1} = \frac{1}{\det A} \adj A \\).

## 3. Linear Systems & Gaussian Elimination
Math: Augment \\( [A | b] \\) with \\( b = [b_i]_{i=1}^2 = [5, 11]^T \\); solve via back-sub after REF.

**NumPy Demo**:
- `np.linalg.solve(A, b)` yields [1. 2.] (exact: \\( x_1 = \frac{\det A_1}{\det A} \\), where \\( A_1 \\) swaps col1 with b, det= -2 same; verifies Cramer's).
- Check: `A @ x` = [5. 11.] (residual 0).
- Rank: `np.linalg.matrix_rank(A)` = 2 (full; for singular, rank < 2 implies infinite/no solutions).

NumPy's `solve` performs LU-like factorization internally (no explicit Gaussian code needed; for custom, use `scipy.linalg.lu` but stick to np.linalg here).

## 4. Vector Spaces
Math: rank A = # pivots = dim Col(A); nullity = 2 - rank A.

**NumPy Demo**:
- Rank as above: 2.
- Nullity estimate via SVD: `U, S, Vt = np.linalg.svd(A)`; count singular values > 1e-10: 2, so nullity = 2 - 2 = 0 (Nul(A) = {0}). For basis, nullspace vectors from Vt rows with small S.

## 5. Linear Transformations
Math: T(x)_i = \\( \sum_j a_{ij} x_j \\); matrix rep is A.

**NumPy Tie-In**: Same as matrix ops; e.g., `T_x = A @ x` applies transformation (vectorized).

## 6. Eigenvalues
Math: Solve det(A - λ I) = 0, (A - λ I)_{ij} = a_{ij} - λ δ_{ij}; then (A - λ I) v = 0 for v_j.

**NumPy Demo**:
- `eigvals, eigvecs = np.linalg.eig(A)`: eigvals ≈ [-0.372, 5.372] (roots of λ² - tr(A)λ + det A = λ² - 5λ -2 =0).
- Eigvecs columns: e.g., col0 ≈ [-0.825, 0.566]^T for λ≈-0.372.
- Check: `A @ eigvecs[:,0]` ≈ λ eigvecs[:,0] (scaled verify: `A @ eigvecs[:,0] / eigvals[0]` matches eigvecs[:,0]).

For diagonalizable: Full rank eigvecs (det ≠0).

## 7. Inner Products & Orthogonalization
Math: <u,v> = \\( \sum_i u_i v_i \\); proj = (<v,w>/<w,w>) w (scalar mult on w_i).

**NumPy Demo** (u=[1,2], v=[3,4]):
- `np.dot(u, v)` = 11 (or `u @ v`).
- `np.linalg.norm(u)` ≈ 2.236 (√<u,u>).

Gram-Schmidt: Use `np.linalg.qr(V)` for matrix V (columns as basis vectors); Q = orthonormal.
- Example V = \\( \begin{pmatrix} 3 & 0 & 0 \\ 1 & 2 & 0 \\ 0 & 0 & 3 \end{pmatrix} \\) (cols v^{(1)}=[3,1,0]^T, etc.).
- `ortho = np.linalg.qr(V)[0]` yields ≈ \\( \begin{pmatrix} -0.949 & -0.316 & 0 \\ -0.316 & 0.949 & 0 \\ 0 & 0 & 1 \end{pmatrix} \\) (sign flips ok).
- Check: `np.allclose(ortho.T @ ortho, np.eye(3))` = True (δ_{ij}).

Quadratic Form: `u @ A @ u` = 27.0 (x^T A x with x_i = u_i; for pos def, all eigvals >0—here mixed signs).

**Quick Verification Tip**: Always `np.allclose` for floats; row-reduce manually for small n, then match `solve` or `eig`. Practice: Swap in your 3×3 matrices.

[NumPy linalg Documentation](https://numpy.org/doc/stable/reference/routines.linalg.html)
[Linear Algebra in NumPy - SciPy Lecture Notes](https://scipy-lectures.org/intro/numpy/auto_examples/plot_linear_algebra.html)
