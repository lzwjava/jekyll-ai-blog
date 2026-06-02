---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Characteristic Polynomial Definition and Properties
translated: false
type: note
---

In linear algebra, the **characteristic polynomial** of a square matrix \\( A \\) (of size \\( n \times n \\)) is a polynomial that encodes information about the matrix's eigenvalues. It is defined as:

\\[
p(\lambda) = \det(A - \lambda I)
\\]

where:

- \\( A \\) is the \\( n \times n \\) matrix.
- \\( \lambda \\) is a scalar (the variable of the polynomial).
- \\( I \\) is the \\( n \times n \\) identity matrix.
- \\( \det \\) denotes the determinant.

### Key Characteristics

1. **Form**: The characteristic polynomial is a monic polynomial of degree \\( n \\), meaning its leading coefficient (for the \\( \lambda^n \\) term) is 1.
   - For a \\( 2 \times 2 \\) matrix \\( A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \\), the characteristic polynomial is:
     \\[
     p(\lambda) = \det \begin{bmatrix} a - \lambda & b \\ c & d - \lambda \end{bmatrix} = \lambda^2 - (a + d)\lambda + (ad - bc)
     \\]
     where \\( a + d \\) is the trace and \\( ad - bc \\) is the determinant.

2. **Eigenvalues**: The roots of the characteristic polynomial \\( p(\lambda) = 0 \\) are the eigenvalues of the matrix \\( A \\). These can be real or complex numbers.

3. **Coefficients**: The coefficients of the polynomial are related to the matrix's properties:
   - The coefficient of \\( \lambda^{n-1} \\) is \\( -\text{trace}(A) \\).
   - The constant term is \\( (-1)^n \det(A) \\).
   - Other coefficients are determined by sums of principal minors of \\( A \\).

4. **Invariance**: The characteristic polynomial is invariant under similarity transformations. If \\( B = P^{-1}AP \\), then \\( A \\) and \\( B \\) have the same characteristic polynomial.

5. **Cayley-Hamilton Theorem**: The matrix \\( A \\) satisfies its own characteristic polynomial, i.e., if \\( p(\lambda) \\) is the characteristic polynomial, then \\( p(A) = 0 \\) (the zero matrix).

### Example

For a matrix \\( A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} \\):

- Compute \\( A - \lambda I = \begin{bmatrix} 1 - \lambda & 2 \\ 3 & 4 - \lambda \end{bmatrix} \\).
- The characteristic polynomial is:
  \\[
  p(\lambda) = \det \begin{bmatrix} 1 - \lambda & 2 \\ 3 & 4 - \lambda \end{bmatrix} = (1 - \lambda)(4 - \lambda) - (2)(3) = \lambda^2 - 5\lambda + 4 - 6 = \lambda^2 - 5\lambda - 2
  \\]
- The eigenvalues are found by solving \\( \lambda^2 - 5\lambda - 2 = 0 \\).

### Applications

- **Eigenvalue computation**: Solving \\( p(\lambda) = 0 \\) gives the eigenvalues.
- **Matrix properties**: Helps determine diagonalizability, invertibility, and other properties.
- **Differential equations**: Used in systems of linear differential equations to find solutions.

If you need a specific example or further details, let me know!
