---
audio: false
generated: true
image: false
lang: en
layout: post
title: Newton-Schulz Orthogonalization for Momentum
translated: false
type: note
---

Question: How does Newton-Schulz iteration work to orthogonalize a momentum matrix?

Answer:

**Goal:** Given a matrix $G$ (the momentum buffer), find an orthogonal approximation $Q \approx G / \|G\|$ such that $Q^T Q \approx I$.

---

**The Newton-Schulz Iteration**

It's a polynomial iteration that converges to the orthogonal factor of a matrix (from its polar decomposition $G = QS$ where $Q$ is orthogonal and $S$ is symmetric positive semi-definite).

**Update rule (one step):**

$$X_{k+1} = \frac{3}{2} X_k - \frac{1}{2} X_k X_k^T X_k$$

Starting from $X_0 = G / \|G\|_F$, this converges cubically to the orthogonal factor $Q$.

---

**Step-by-Step in Code**

```python
import torch

def newton_schulz_orthogonalize(G, steps=5, eps=1e-7):
    """
    Orthogonalize matrix G using Newton-Schulz iteration.
    Returns Q ≈ orthogonal factor of G.
    """
    # Step 1: Normalize to ensure spectral norm < 1
    X = G / (G.norm() + eps)

    # Step 2: Iterate
    for _ in range(steps):
        A = X @ X.T          # X X^T
        X = 1.5 * X - 0.5 * (A @ X)   # Newton-Schulz update

    return X
```

---

**Muon's Actual Polynomial (Slightly Different)**

The Muon implementation uses a degree-5 Chebyshev-like polynomial for faster convergence:

```python
def zeropower_via_newtonschulz5(G, steps=10, eps=1e-7):
    assert G.ndim == 2
    a, b, c = (3.4445, -4.7750, 2.0315)  # tuned coefficients

    X = G / (G.norm() + eps)

    # Handle non-square matrices: work on the smaller dimension
    if G.shape[0] > G.shape[1]:
        X = X.T

    for _ in range(steps):
        A = X.T @ X          # X^T X  (square, for tall matrices)
        X = a * X + (b * X) @ A + (c * X) @ (A @ A)

    if G.shape[0] > G.shape[1]:
        X = X.T

    return X
```

---

**How It Fits Into Muon**

```python
def muon_update(param, momentum_buffer, lr=0.01, steps=5):
    G = momentum_buffer          # accumulated gradient momentum
    Q = zeropower_via_newtonschulz5(G, steps=steps)  # orthogonalize
    
    # Scale by RMS like Adam does, but use orthogonal direction
    scale = max(1, G.shape[0] / G.shape[1]) ** 0.5
    param.data -= lr * scale * Q
```

---

**Intuition Summary**

| Step | What happens |
| --- | --- |
| Normalize $G$ | Bring spectral norm close to 1 |
| Iterate $X \leftarrow f(X)$ | Push singular values toward 1 |
| Converged $X = Q$ | All singular values = 1 → orthogonal matrix |

The result is an update matrix where **all gradient directions are treated equally** — no single direction dominates — leading to more stable training.

References:

- [Muon Source Code – newton-schulz impl](https://github.com/KellerJordan/Muon/blob/master/muon.py)
- [Polar Decomposition via Newton-Schulz – Wikipedia](https://en.wikipedia.org/wiki/Polar_decomposition#Algorithms)
- [Keller Jordan's Muon Blog Post](https://kellerjordan.github.io/posts/muon/)
