---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Matrix Dimensions in Ax=0
translated: false
type: note
---

Not necessarily! Let me clarify:

**x** is a column vector with **n components**: x₁, x₂, ..., xₙ. That part is correct.

**However, A doesn't have to be an n×n matrix.** A can be an **m×n matrix**, where:

- **m** = number of rows (number of equations)
- **n** = number of columns (number of variables)

So the system Ax = 0 has:

- **m equations**
- **n unknowns** (the components of x)

**Examples:**

1. If A is 3×3 and x is 3×1, you have 3 equations in 3 unknowns.
2. If A is 5×3 and x is 3×1, you have 5 equations in 3 unknowns (overdetermined system).
3. If A is 2×4 and x is 4×1, you have 2 equations in 4 unknowns (underdetermined system).

**Special case:** If A is specifically an **n×n square matrix**, then yes, you have n equations in n unknowns, and the behavior of solutions depends on whether A is invertible or singular.

So the general answer is: **A is an m×n matrix, and x is an n×1 column vector**, but they don't have to be square!
