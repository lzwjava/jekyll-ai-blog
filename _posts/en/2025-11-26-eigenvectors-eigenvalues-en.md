---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding Eigenvectors and Eigenvalues
translated: false
type: note
---

You're very close to understanding, but there's one key misunderstanding that's confusing you.

Let me explain eigenvectors and eigenvalues step by step, in a simple and clear way.

### 1. What is an eigenvector?

An **eigenvector** of a square matrix **A** is a **non-zero vector** v such that when you multiply it by A, you get back a **scaled version** of the same vector:

```
A × v = λ × v
```

Here:
- v = eigenvector (a direction)
- λ = eigenvalue (a number, the scaling factor)

In words:
**The matrix A stretches or shrinks the eigenvector v, but does not change its direction** (it might flip it if λ is negative).

So after applying A, the vector is still pointing in the same (or opposite) direction — only its length changes by factor |λ|.

### 2. Why do we write (A − λI) v = 0 ?

From A v = λ v, we can rearrange:

```
A v − λ v = 0
A v − λ I v = 0
(A − λ I) v = 0
```

This is a system of linear equations.

For there to be a **non-zero** solution v, the matrix (A − λI) must be **singular** (not invertible), which means:

```
det(A − λI) = 0
```

This is the **characteristic equation**. Solving it gives the eigenvalues λ.

Then, for each λ, you solve (A − λI) v = 0 to find the eigenvectors v.

### 3. Your confusion: Why is (A − λI) v = 0, not something else?

You said:

> "(A−λE) * eigenvector = 0 , but that like 3×3 ⋅ 3×1 = 3×1 matrix, how can it be zero?"

Yes, the result is a 3×1 vector.
But **It is the zero vector** (i.e., [0, 0, 0]ᵀ), **not the zero matrix**.

So:

```
(A − λI) v = [0]
             [0]   ← the 3×1 zero vector
             [0]
```

This does **not** mean that (A − λI) is the zero matrix!
It just means that v is in the **null space** of (A − λI).
The matrix (A − λI) sends the special vector v to zero, but sends other vectors elsewhere.

### Simple Example (2×2 matrix)

Let
```
A = [2  1]
    [0  2]
```

Try v = [1, 0]ᵀ

Then
A v = [2 1] [1] = [2×1 + 1×0] = [2] = 2 × [1
      [0 2] [0]   [0×1 + 2×0]   [0]     [0]

So A v = 2 v → λ = 2, v = [1,0]ᵀ is an eigenvector.

Now check (A − 2I)v:

```
A − 2I = [2-2  1] = [0 1]
         [0    2-2]   [0 0]

[0 1] [1] = [0×1 + 1×0] = [0] = 0 vector
[0 0] [0]   [0×1 + 0×0]   [0]
```

Yes! It's zero, even though (A − 2I) is not the zero matrix.

### Summary

| Term            | Meaning                                                                 |
|-----------------|-------------------------------------------------------------------------|
| Eigenvalue λ    | How much the eigenvector is stretched/shrunk (can be negative or zero)  |
| Eigenvector v   | A special direction that doesn't change under A (only scaled)           |
| (A − λI)v = 0   | Means the vector v is killed (sent to zero) by the matrix (A − λI)       |
| det(A − λI) = 0 | Condition for such non-zero v to exist                                  |

So don't think of (A − λI)v = 0 as "the whole matrix times v gives nothing" in a confusing way — it's just saying: **this particular direction v is completely wiped out** by the shifted matrix.

Once you see that, everything clicks.

Let me know if you want to compute an example together!
