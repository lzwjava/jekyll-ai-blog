---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Inverting a 3x3 Matrix
translated: false
type: note
---

Sure — let’s unpack that clearly and intuitively, without any table formatting so it’s easy to read line by line.

---

### 1. What the goal is
We want to find the inverse of a 3×3 matrix, usually written as A⁻¹.
The inverse is the matrix that “undoes” A, meaning
A × A⁻¹ = I,
where I is the identity matrix.

---

### 2. The core formula
The general formula for any invertible square matrix is

A⁻¹ = (1 / det(A)) × adj(A).

So we need two ingredients:
- the determinant det(A), and
- the adjugate matrix adj(A), which is the transpose of the cofactor matrix.

---

### 3. Determinant of a 3×3 matrix
If
A =
[a  b  c]
[d  e  f]
[g  h  i],

then

det(A) = a(ei − fh) − b(di − fg) + c(dh − eg).

This value tells you whether the matrix is invertible:
- if det(A) = 0 → no inverse (matrix is singular),
- if det(A) ≠ 0 → inverse exists.

---

### 4. Cofactors
To build adj(A), we first find the cofactor of each element.
The cofactor of entry aᵢⱼ is
Cᵢⱼ = (−1)^(i+j) × Mᵢⱼ,
where Mᵢⱼ is the determinant of the 2×2 submatrix you get after deleting row i and column j.

Doing this for all nine positions gives the “cofactor matrix.”
For the general case above:

C₁₁ = ei − fh
C₁₂ = −(di − fg)
C₁₃ = dh − eg

C₂₁ = −(bi − ch)
C₂₂ = ai − cg
C₂₃ = −(ah − bg)

C₃₁ = bf − ce
C₃₂ = −(af − cd)
C₃₃ = ae − bd

---

### 5. Transpose the cofactor matrix
Now take that cofactor matrix and transpose it — meaning swap rows and columns.
That new matrix is called the **adjugate** (or adjoint) of A, written adj(A).
If you think visually, this “transpose” is like rotating the matrix: what was in the first row becomes the first column, and so on.

---

### 6. Multiply by 1/det(A)
Finally, scale the adjugate matrix by dividing every term by det(A).
That gives you A⁻¹.

Symbolically:
A⁻¹ = (1/det(A)) × adj(A).

---

### 7. Why it works
This formula comes from a fundamental property of determinants and cofactors:

A × adj(A) = det(A) × I.

If you divide both sides by det(A), you get exactly
A × [(1/det(A)) × adj(A)] = I.

So the right-hand factor must be the inverse.

The reason this identity holds is that when you multiply A by its cofactor matrix, each diagonal term becomes the determinant itself (since it’s the expansion along that row), and each off-diagonal term becomes zero due to the alternating cofactor signs — that’s the algebraic cancellation at work.

---

### 8. Example
Let
A =
[1  2  3]
[0  1  4]
[5  6  0].

Compute det(A):
= 1(1×0 − 4×6) − 2(0×0 − 4×5) + 3(0×6 − 1×5)
= (−24) − (−40) + (−15)
= −24 + 40 − 15 = 1.

So det(A) = 1.

Then find all cofactors (a bit tedious, but straightforward), transpose them to get adj(A), and since det(A) = 1, the adjugate is already the inverse.

---

### 9. Summary intuition
- Determinant → a measure of how the matrix “scales space.”
- Cofactor → captures each element’s contribution to that scaling.
- Transposing → aligns those contributions so multiplication reconstructs the identity.
- Dividing by the determinant → normalizes the scaling.

---

Would you like me to show the detailed cofactor calculations for that example (the [1 2 3; 0 1 4; 5 6 0] one) so you can see every minor and sign?
