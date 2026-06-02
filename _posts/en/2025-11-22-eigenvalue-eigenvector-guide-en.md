---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Finding Eigenvalues and Eigenvectors Guide
translated: false
type: note
---

## Eigenvalues

To find eigenvalues of a matrix **A**, you solve the **characteristic equation**:

**det(A - λI) = 0**

where λ (lambda) represents the eigenvalues and **I** is the identity matrix.

**Steps:**

1. Subtract λ from the diagonal elements of A to get (A - λI)
2. Calculate the determinant of (A - λI)
3. Set the determinant equal to zero
4. Solve the resulting polynomial equation for λ

## Eigenvectors

Once you have an eigenvalue λ, find its corresponding eigenvector by solving:

**(A - λI)v = 0**

where **v** is the eigenvector (a non-zero vector).

**Steps:**

1. Substitute the eigenvalue λ into (A - λI)
2. Solve the homogeneous system of linear equations
3. Find all non-zero vectors that satisfy the equation
4. The solution space forms the **eigenspace** for that eigenvalue

## Example

For a 2×2 matrix **A** = [[3, 1], [1, 3]]:

**Finding eigenvalues:**

- A - λI = [[3-λ, 1], [1, 3-λ]]
- det(A - λI) = (3-λ)² - 1 = λ² - 6λ + 8 = 0
- Solving: λ = 4 and λ = 2

**Finding eigenvector for λ = 4:**

- (A - 4I)v = 0 gives [[−1, 1], [1, −1]]v = 0
- This yields v = [[1], [1]] (or any scalar multiple)

**Finding eigenvector for λ = 2:**

- (A - 2I)v = 0 gives [[1, 1], [1, 1]]v = 0
- This yields v = [[1], [−1]]

For numerical computation or larger matrices, software like Python (NumPy), MATLAB, or other linear algebra tools can compute these automatically.
