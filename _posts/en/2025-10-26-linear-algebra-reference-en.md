---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Linear Algebra Exam Quick Reference
translated: false
type: note
---

Quick reference for key concepts and formulas. Focus on matrices, determinants, linear systems, vector spaces, transformations, eigenvalues, and quadratic forms—core topics from past exams. Review definitions, properties, and computations.

## 1. Matrices
- **Definition**: \\( A = [a_{ij}] \in \mathbb{R}^{m \times n} \\).
- **Operations**:
  - Addition: \\( (A + B)_{ij} = a_{ij} + b_{ij} \\).
  - Scalar: \\( (cA)_{ij} = c a_{ij} \\).
  - Multiplication: \\( (AB)_{ij} = \sum_k a_{ik} b_{kj} \\) (if compatible sizes).
- **Transpose**: \\( (A^T)_{ij} = a_{ji} \\); \\( (AB)^T = B^T A^T \\), \\( (A^T)^T = A \\).
- **Inverse** (square): \\( AA^{-1} = I \\); \\( (AB)^{-1} = B^{-1} A^{-1} \\); \\( (A^T)^{-1} = (A^{-1})^T \\).
- **Types**:
  - Diagonal: Non-zero only on diagonal.
  - Upper/Lower Triangular: Zeros below/above diagonal.
  - Symmetric: \\( A = A^T \\).
  - Orthogonal: \\( A^T A = I \\) (columns orthonormal).

## 2. Determinants (det A)
- **Properties**:
  - \\( \det(AB) = \det A \cdot \det B \\); \\( \det(A^T) = \det A \\); \\( \det(cA) = c^n \det A \\).
  - Row/Column swap: Multiplies by -1.
  - Add multiple of row/column: No change.
  - Scale row/column by c: Multiplies by c.
  - \\( \det I = 1 \\); \\( \det A = 0 \\) if singular (dependent rows/columns).
- **Computation**:
  - 2x2: \\( \det \begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc \\).
  - Cofactor Expansion (row i): \\( \det A = \sum_j a_{ij} C_{ij} \\), where \\( C_{ij} = (-1)^{i+j} M_{ij} \\) (minor det).
  - Triangular: Product of diagonal entries.
- **Adjugate/Inverse**: \\( A^{-1} = \frac{1}{\det A} \adj A \\), where \\( \adj A = C^T \\) (cofactor transpose).
- **Cramer's Rule** (for \\( Ax = b \\), det A ≠ 0): \\( x_i = \frac{\det A_i}{\det A} \\) (A_i replaces i-th column with b).

## 3. Linear Systems (Ax = b)
- **Gaussian Elimination**: Row reduce [A | b] to REF/RREF.
  - REF: Pivots (leading 1s) staircase down-right; zeros below pivots.
  - Back-substitution for unique solution.
- **Solutions**:
  - Unique: rank A = n (full column rank), nullspace {0}.
  - Infinite: rank A = rank [A|b] < n (free variables).
  - None: rank A < rank [A|b].
- **Complete Solution**: Particular solution + nullspace basis (homogeneous solutions).
- **LU Decomposition** (no pivoting): A = LU (L lower unit triangular, U upper); solve Ly = b, Ux = y.
- **Least Squares** (overdetermined): \\( \hat{x} = (A^T A)^{-1} A^T b \\) (if full rank).

## 4. Vector Spaces & Subspaces
- **Vector Space**: Closed under addition/scalar mult.; axioms (e.g., 0 vector, inverses).
- **Subspaces**: Span of vectors; closed, contains 0.
  - Column Space: Col(A) = span(columns of A); dim = rank A.
  - Row Space: Row(A) = Col(A^T); dim = rank A.
  - Nullspace: Nul(A) = {x | Ax = 0}; dim = n - rank A.
  - Left Nullspace: Nul(A^T).
- **Linear Independence**: c1 v1 + ... + ck vk = 0 ⇒ all ci = 0.
- **Basis**: Lin. indep. spanning set.
- **Dimension**: # vectors in basis; dim Col(A) + dim Nul(A) = n (rank-nullity).
- **Rank**: # pivot columns = dim Col(A) = dim Row(A).

## 5. Linear Transformations
- **Definition**: T: V → W linear if T(u + v) = T u + T v, T(cu) = c T u.
- **Matrix Rep.**: [T] wrt bases = A where T(x) = A x (std. basis).
- **Kernel**: Ker T = Nul(A); Image: Im T = Col(A).
- **Isomorphism**: 1-1 onto (invertible matrix).
- **Rank-Nullity**: dim Ker T + dim Im T = dim V.

## 6. Eigenvalues & Eigenvectors
- **Definition**: A v = λ v (v ≠ 0 eigenvector, λ eigenvalue).
- **Characteristic Eq.**: det(A - λ I) = 0; roots λi (algebraic multiplicity).
- **Eigenvectors**: Solve (A - λ I) v = 0; geometric mult. = dim eigenspace.
- **Diagonalizable**: n lin. indep. eigenvectors ⇒ A = X Λ X^{-1} (Λ diag(λi), X = [v1 ... vn]).
  - Symmetric A: Always diagonalizable; orthogonal eigenvectors (A = Q Λ Q^T, Q orthogonal).
- **Trace**: tr A = ∑ λi.
- **Det**: det A = ∏ λi.
- **Similar Matrices**: A ~ B if A = P B P^{-1}; same eigenvalues, trace, det.

## 7. Inner Products & Quadratic Forms
- **Inner Product**: <u, v> = u^T v (Euclidean); ||v|| = √<v,v>.
- **Orthogonal**: <u,v> = 0; Orthonormal basis: <ei, ej> = δij.
- **Gram-Schmidt**: Orthogonalize basis {v1,...,vn} → {u1,...,un}.
  - u1 = v1; uk = vk - proj_{span(u1..u_{k-1})} vk; proj_w v = (<v,w>/<w,w>) w.
- **Quadratic Form**: q(x) = x^T A x (A symmetric).
  - Positive Definite: q(x) > 0 for x ≠ 0 (all λi > 0).
  - Diagonalize: q(x) = ∑ λi yi^2 (y = Q^T x).

## Quick Tips
- Compute rank: Row reduce to find # pivots.
- Check diagonalizable: Geometric mult. = algebraic mult. for each λ.
- For exams: Practice row reduction, det expansion, eigenproblems on 2x2/3x3 matrices.
- Common Errors: Forgetting multiplicity; sign in cofactors; non-commutative mult.

Good luck tomorrow—focus on understanding over memorizing!

[Linear Algebra Cheat Sheet - Laurent Lessard](https://laurentlessard.com/teaching/ece532/cheat_sheet.pdf)
[Linear Algebra Review - Yiping Lu](https://2prime.github.io/files/linear/finalsheet.pdf)
[2023 Self-Exam Linear Algebra Questions](https://doc.quark.cn/preview/jiaoyukaoshi-shijuan-gaokao/1130FC966EE595249D3822AFF5DF0167)
