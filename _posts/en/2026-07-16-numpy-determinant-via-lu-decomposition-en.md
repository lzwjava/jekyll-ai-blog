---
audio: false
generated: true
image: false
lang: en
layout: post
title: Numpy determinant via LU decomposition
translated: false
type: note
---

Question: How does numpy compute the determinant of a matrix, and what's the underlying algorithm?

Answer: `np.linalg.det` doesn't use cofactor expansion (that's O(n!)). It uses **LU decomposition** — factor A = PLU, then det(A) = det(P) *det(L)* det(U). Since L is unit lower-triangular (det=1) and U is upper-triangular, det(U) = product of diagonal. det(P) = ±1 depending on permutation parity.

```python
import numpy as np
from scipy.linalg import lu

A = np.array([[4., 3., 2.],
              [1., 5., 6.],
              [7., 8., 9.]])

print(np.linalg.det(A))  # -55.0000...

# what's happening under the hood
P, L, U = lu(A)
print(np.diag(U))                     # diagonal of U
sign = np.linalg.det(P)               # ±1, permutation parity
det = sign * np.prod(np.diag(U))
print(det)
```

Under the hood numpy calls LAPACK's `dgetrf` (double) or `sgetrf` (float) for the LU factorization with partial pivoting, cost O(n³) vs O(n!) for cofactor expansion. That's why a 1000x1000 determinant is instant.

Gotcha you'll hit in practice: floating point. LU pivoting means tiny numerical errors compound, so `det` on a genuinely singular matrix might return `1e-14` instead of exactly `0`. Check with a tolerance, not `== 0`:

```python
if abs(np.linalg.det(A)) < 1e-10:
    print("singular")
```

For log-determinants (common in GMMs, Gaussian processes, normalizing flows — avoiding under/overflow on large matrices), use `np.linalg.slogdet` instead, which tracks sign and log|det| separately:

```python
sign, logdet = np.linalg.slogdet(A)
```

References:

- [numpy.linalg.det docs](https://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html)
- [LAPACK dgetrf](https://netlib.org/lapack/explore-html/dd/d9a/group__getrf.html)
