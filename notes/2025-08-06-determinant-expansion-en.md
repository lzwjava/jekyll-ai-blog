---
audio: false
generated: true
image: false
lang: en
layout: post
title: 'Determinant: Expansion via Linearity and Alternation'
translated: false
type: note
---

When you learn that the determinant is a function that is

1. **multilinear** in the rows (or columns), and
2. **alternating** (swapping two rows flips its sign),

the cofactor‐expansion formula falls out naturally. Here’s a step‐by‐step “why” for the 3×3 case:

---

### 1. Determinant via permutations

The most general definition of a 3×3 determinant is

$$
\det A \;=\;
\sum_{\sigma\in S_3}\!\mathrm{sgn}(\sigma)\,a_{1,\sigma(1)}\,a_{2,\sigma(2)}\,a_{3,\sigma(3)},
$$

where you sum over all six permutations σ of {1,2,3}, and sgn(σ) is +1 for even permutations and –1 for odd ones.

If you write them out, you get exactly the six terms:

$$
a_{11}a_{22}a_{33},\;a_{12}a_{23}a_{31},\;a_{13}a_{21}a_{32}
\;-\;
\bigl(a_{13}a_{22}a_{31}+a_{11}a_{23}a_{32}+a_{12}a_{21}a_{33}\bigr).
$$

---

### 2. Grouping by one row or column

Notice you can **group** those six terms according to which entry in the first row they use:

* Terms containing \$a\_{11}\$:

  $$
    a_{11}\,(a_{22}a_{33} - a_{23}a_{32})
    = a_{11}\det\!\begin{pmatrix}a_{22}&a_{23}\\a_{32}&a_{33}\end{pmatrix}.
  $$
* Terms containing \$a\_{12}\$:

  $$
    a_{12}\,(a_{23}a_{31} - a_{21}a_{33})
    = -\,a_{12}\det\!\begin{pmatrix}a_{21}&a_{23}\\a_{31}&a_{33}\end{pmatrix}.
  $$
* Terms containing \$a\_{13}\$:

  $$
    a_{13}\,(a_{21}a_{32} - a_{22}a_{31})
    = \;a_{13}\det\!\begin{pmatrix}a_{21}&a_{22}\\a_{31}&a_{32}\end{pmatrix}.
  $$

That’s exactly the **cofactor expansion along the first row**:

$$
\det A
= a_{11}C_{11} \;+\; a_{12}C_{12} \;+\; a_{13}C_{13},
$$

where each cofactor $C_{1j} = (-1)^{1+j}\det(\text{minor}_{1j})$.

---

### 3. Why “minors” and “signs”?

* **Minor**: $\det(\text{minor}_{ij})$ is the determinant of the 2×2 submatrix you get by deleting row i and column j.
* **Sign factor** $(−1)^{i+j}$: ensures that if you swap two rows of $A$, the overall sign flips—just like the permutation definition demands.

Because the determinant must be linear in each row, you can “pull out” one entry from a row, leaving the determinant of the smaller matrix multiplied by that entry. The alternating property forces those $(−1)$ signs.

---

### 4. Geometric intuition

For a 3×3 matrix whose rows are vectors $\mathbf{u},\mathbf{v},\mathbf{w}\in\mathbb{R}^3$, $\det A$ is the signed volume of the parallelepiped they span.

* Expanding along, say, the first row, you’re decomposing that volume into “slabs” perpendicular to each coordinate axis.
* Each slab’s area is the area of the parallelogram spanned by the other two row‐vectors (a 2×2 determinant), and you scale it by the corresponding coordinate $u_j$ of $\mathbf{u}$.
* The sign $(−1)^{1+j}$ keeps track of orientation.

---

### 5. Generalization to $n\times n$

All of this works in the same way for any size $n$: the permutation definition has $n!$ terms, you group them by one row or column, and each group collapses to

$$
a_{ij}\,(-1)^{i+j}\det(\text{minor}_{ij}).
$$

That is the **cofactor expansion** principle.

---

**In short:**
Cofactor expansion is simply the permutation‐sum definition of the determinant, reorganized by one row (or column), together with the requirements of linearity and sign‐alternation. It offers a recursive way to compute—and a clear geometric picture of—the determinant.
