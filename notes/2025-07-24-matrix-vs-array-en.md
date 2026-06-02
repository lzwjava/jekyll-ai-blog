---
audio: false
generated: true
lang: en
layout: post
title: Matrices vs Multi-D Arrays
translated: false
type: note
---

Here’s a quick mental model that usually helps programmers keep the two straight.

---

### 1  Core idea they share

* **Grid‑like storage** – Both a mathematical matrix and a multi‑dimensional array organise elements by multiple integer indices (row/column, or row/col/…/k).
* **Indexed access** – You reach an element with a coordinate triple such as `A[i][j]` (matrix → two indices; general array → any count of indices).
* **Bulk operations** – Thinking in blocks rather than scalars encourages vectorised or loop‑based code, cache‑friendly memory layouts, GPU usage, etc.

---

### 2  Where they part ways

**a. Purpose & semantics**

*Matrix*

* Purely **mathematical**: every element is a number from a field (ℝ, ℂ, …).
* Carries built‑in algebra: addition, scalar multiple, determinant, inverse, eigen‑stuff, etc.
* Shape is always 2‑D; a “rank‑3 tensor” isn’t called a matrix.

*Multi‑D array*

* **Programming container**: can store any data type, numeric or not.
* No inherent algebra; operations are whatever you code (or the library supplies).
* Rank is arbitrary: 1‑D (vector), 2‑D, 5‑D, … even ragged structures.

**b. Implementation details**

*Matrix libraries* (NumPy `ndarray`, MATLAB, Eigen, BLAS, etc.)

* Usually pay attention to **row‑major vs column‑major** order because it affects performance of algebraic kernels.
* May keep metadata such as leading dimension, stride, triangular/packed forms.
* Provide overloaded operators so `C = A @ B` triggers high‑performance matrix multiplication.

*General arrays* (C arrays, Java arrays, Rust slices, Python lists of lists)

* Memory layout is language‑specific: contiguous, array‑of‑pointers, or even fragmented (in Python lists).
* Lack automatic algebra; to multiply two 2‑D arrays you write nested loops or call a math library.
* Can be sparse, jagged, or mixed‑type in dynamically‑typed languages.

**c. Typical operations**

*Matrix* – dot products, LU/QR decomposition, solving linear systems, SVD, gradients in ML, graphics transforms.

*Multi‑D array* – anything: RGBA image pixels, a 3‑D voxel world, a lookup table of strings, game board states.

---

### 3  Analogy in code

```python
# Matrix viewpoint (NumPy)
import numpy as np
A = np.array([[1, 2],
              [3, 4]])          # 2×2 matrix
B = np.array([[5, 6],
              [7, 8]])
C = A @ B                       # matrix multiplication, algebra-aware
detA = np.linalg.det(A)         # determinant

# Pure multi‑D array viewpoint (vanilla Python)
table = [[1, 2], [3, 4]]        # list of lists
value = table[1][0]             # 3
# Multiplication? Need explicit loops or comprehension
product = [[sum(table[i][k]*B[k][j] for k in range(2))
           for j in range(2)] for i in range(2)]
```

---

### 4  TL;DR

* **Same shape, different meaning:** A matrix is a 2‑D numeric array *plus* a bundle of linear‑algebra laws; a multi‑dimensional array is just an indexed container—nothing more, nothing less.
* In practice, you often store matrices *inside* multi‑D arrays, then rely on libraries to endow them with matrix semantics and speed.
