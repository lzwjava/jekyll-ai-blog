---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Precise Linear Algebra Pocket Guide
translated: false
type: note
---

As your engineering-focused tutor, this guide emphasizes verifiable, index-explicit computations for matrices \\( A = [a_{ij}]_{i=1}^m, j=1^n \in \mathbb{R}^{m \times n} \\) (rows indexed by \\( i \\), columns by \\( j \\), 1-based). All steps are shown with indices for clarity; examples annotate entries inline. Review via row reduction and eigenvalue solves on 2×2/3×3 cases.

## 1. Matrix Operations
- **Addition**: \\( (A + B)_{ij} = a_{ij} + b_{ij} \\) for all \\( i,j \\).
- **Scalar Multiplication**: \\( (cA)_{ij} = c a_{ij} \\) for scalar \\( c \\), all \\( i,j \\).
- **Matrix Multiplication** (if \\( m \times p \\) and \\( p \times n \\)): \\( (AB)_{ij} = \sum_{k=1}^p a_{ik} b_{kj} \\) for all \\( i=1^m \\), \\( j=1^n \\).
- **Transpose**: \\( (A^T)_{ij} = a_{ji} \\); thus \\( (AB)^T_{ij} = \sum_k b_{ki} a_{kj} = (B^T A^T)_{ij} \\).
- **Inverse** (for square \\( n \times n \\), \\( \det A \neq 0 \\)): \\( A^{-1} \\) satisfies \\( \sum_k a_{ik} (A^{-1})_{kj} = \delta_{ij} \\) (Kronecker delta: 1 if \\( i=j \\), 0 else). Properties: \\( (AB)^{-1}_{ij} = \sum_k (B^{-1})_{ik} (A^{-1})_{kj} = (B^{-1} A^{-1})_{ij} \\); \\( (A^T)^{-1}_{ij} = \sum_k (A^{-1})_{ki} (A^T)_{kj} ? Wait, no: (A^{-1})^T_{ij} = (A^{-1})_{ji} \\), so \\( [(A^T)^{-1}]_{ij} = (A^{-1})_{ji} \\).

**Example (2×2 Inverse Annotation)**: Let \\( A = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix} \\). Then \\( A^{-1} = \frac{1}{\det A} \begin{pmatrix} a_{22} & -a_{12} \\ -a_{21} & a_{11} \end{pmatrix} \\), where \\( \det A = a_{11} a_{22} - a_{12} a_{21} \\).

## 2. Determinants
- **Definition**: For square \\( A \\), \\( \det A \\) via cofactor expansion along row \\( i \\): \\( \det A = \sum_{j=1}^n a_{ij} C_{ij} \\), where minor \\( M_{ij} \\) is submatrix deleting row \\( i \\) and column \\( j \\) (so \\( M_{ij} = [m_{pq}] \\) with \\( p=1^{n-1} \setminus i \\), \\( q=1^{n-1} \setminus j \\), relabeled 1-based), cofactor \\( C_{ij} = (-1)^{i+j} \det(M_{ij}) \\).
- **Properties**:
  - \\( \det(AB) = \det A \cdot \det B \\); \\( \det(A^T) = \det A \\) (since expansion symmetric).
  - \\( \det(cA) = c^n \det A \\).
  - Row swap: \\( \det \\) multiplies by -1; add multiple of row \\( k \\) to row \\( i \neq k \\): unchanged; scale row \\( i \\) by \\( c \\): multiplies by \\( c \\).
  - \\( \det I = 1 \\) (diagonal 1s); singular if \\( \det A = 0 \\) (rank < n).
- **Adjugate**: \\( \adj(A)_{ij} = C_{ji} = [C^T]_{ij} \\), where \\( C = [C_{pq}] \\). Inverse: \\( A^{-1} = \frac{1}{\det A} \adj A \\), so \\( (A^{-1})_{ij} = \frac{1}{\det A} \sum_k \delta_{ik} C_{kj} ? No: matrix form verifies \\( A \adj A = (\det A) I \\).

**Example (2×2 Cofactors)**: For above \\( A \\), \\( M_{11} = [a_{22}] \\), \\( C_{11} = (-1)^{1+1} a_{22} = a_{22} \\); \\( M_{12} = [a_{21}] \\), \\( C_{12} = (-1)^{1+2} a_{21} = -a_{21} \\); similarly \\( C_{21} = -a_{12} \\), \\( C_{22} = a_{11} \\). Thus \\( \adj A = \begin{pmatrix} C_{11} & C_{21} \\ C_{12} & C_{22} \end{pmatrix} = \begin{pmatrix} a_{22} & -a_{12} \\ -a_{21} & a_{11} \end{pmatrix} \\).

- **Cramer's Rule** (for \\( \sum_j a_{ij} x_j = b_i \\), \\( i=1^n \\), \\( \det A \neq 0 \\)): \\( x_r = \frac{\det A_r}{\det A} \\), where \\( A_r \\) replaces column \\( r \\) of \\( A \\) with \\( [b_i]_{i=1}^n \\), so \\( (A_r)_{ij} = a_{ij} \\) if \\( j \neq r \\), else \\( b_i \\).

## 3. Linear Systems & Gaussian Elimination
- **Augmented Matrix**: \\( [A | b] = [a_{ij} | b_i] \\) for \\( i=1^m \\), \\( j=1^n \\).
- **Row Reduction to REF**: Apply elementary ops (swap rows \\( p \leftrightarrow q \\); scale row \\( p \\) by \\( c \neq 0 \\): row \\( p \leftarrow c \\) row \\( p \\); add \\( c \\) row \\( q \\) to row \\( p \\)) to get row echelon form: leading entry (pivot) in row \\( i \\) at column \\( p_i \geq p_{i-1} \\), zeros below pivots.
- **To RREF**: Continue to zeros above pivots, scale pivots to 1.
- **Rank**: Number of nonzero rows in REF (or pivots).
- **Solutions**:
  - Unique if rank \\( A = n \\), rank \\( [A|b] = n \\) (nullity 0).
  - Infinite if rank \\( A = \\) rank \\( [A|b] = r < n \\) (n-r free vars).
  - Inconsistent if rank \\( A < \\) rank \\( [A|b] \\).
- **General Solution**: \\( x = x_p + x_h \\), particular \\( x_p \\) from RREF, homogeneous \\( x_h \\) spans nullspace (free vars basis).
- **Step Example (2×2 System Annotation)**: Solve \\( a_{11} x_1 + a_{12} x_2 = b_1 \\), \\( a_{21} x_1 + a_{22} x_2 = b_2 \\). Row2 ← Row2 - (a_{21}/a_{11}) Row1: new row2 = [0, a_{22} - (a_{21} a_{12}/a_{11}), b_2 - (a_{21} b_1 / a_{11}) ]. Back-sub: \\( x_2 = \\) ... / det term, etc.

## 4. Vector Spaces
- **Subspaces**: Col(A) = span{ col j of A, j=1^n } = { \\( \sum_j x_j \\) col j | x }; dim = rank A.
- **Row Space**: Row(A) = Col(A^T); dim = rank A.
- **Nullspace**: Nul(A) = { x | \\( \sum_j a_{ij} x_j = 0 \\) ∀ i }; basis from RREF free columns.
- **Rank-Nullity**: rank A + dim Nul(A) = n.

## 5. Linear Transformations
- **Matrix Rep**: T(x)_i = \\( \sum_j a_{ij} x_j \\).
- **Kernel**: Ker T = Nul(A); Im T = Col(A).

## 6. Eigenvalues
- **Char Poly**: det(A - λ I) = 0, where (A - λ I)_{ij} = a_{ij} - λ δ_{ij}.
- **Eigenvectors**: For λ, solve \\( \sum_j (a_{ij} - λ δ_{ij}) v_j = 0 \\), v = [v_j] ≠ 0.
- **Diagonalizable**: If alg mult(λ_k) = geo mult(λ_k) ∀ k (full eigenspace dim), then A = P D P^{-1}, D_{ij} = λ_i δ_{ij}, P columns = eigenvectors.
- **Symmetric**: A = A^T ⇒ orthogonal diag: A = Q D Q^T, Q^T Q = I.

## 7. Inner Products & Orthogonalization
- **Euclidean**: <u,v> = \\( \sum_i u_i v_i = u^T v \\).
- **Gram-Schmidt Step**: For basis {v^{(k)}}, u^{(1)} = v^{(1)}; u^{(k)} = v^{(k)} - \sum_{m=1}^{k-1} \proj_{u^{(m)}} v^{(k)}, where \proj_w v = \frac{<v,w>}{<w,w>} w (component \\( \sum_i ... \\)).

**Quick Verification Tip**: Always row-reduce [A - λI | 0] for eigenspaces; check det via expansion if n≤3.

[Linear Algebra Cheat Sheet - Indexed Formulas](https://laurentlessard.com/teaching/ece532/cheat_sheet.pdf)
[Self-Exam 02198 Review](https://doc.quark.cn/preview/jiaoyukaoshi-shijuan-gaokao/1130FC966EE595249D3822AFF5DF0167)
