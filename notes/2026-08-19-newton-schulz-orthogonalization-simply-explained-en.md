---
audio: false
generated: true
image: false
lang: en
layout: post
title: Newton-Schulz Orthogonalization Simply Explained
translated: false
type: note
---

Question: Can you explain Newton-Schulz orthogonalization more simply?

Answer:

Let's build intuition from scratch, no jargon.

---

**The Problem: What does "orthogonalize" even mean?**

Imagine your gradient matrix has directions with very **unequal importance**:

```
Gradient directions:
→→→→→→→→  (dimension A, huge gradient, dominates updates)
→          (dimension B, tiny gradient, barely updates)
```

This imbalance makes training unstable. We want:

```
After orthogonalization:
→→→  (dimension A, normalized)
→→→  (dimension B, same importance)
```

**Every direction gets equal weight.** That's what orthogonalization does.

---

**What Newton-Schulz does — one picture**

Think of it like repeatedly squishing a blob into a circle:
```
Start:  irregular blob (your gradient matrix)
Step 1: less irregular
Step 2: rounder
Step 3: almost a circle
Step 4: ≈ perfect circle (orthogonal matrix!)
```

Each iteration applies this formula:
```
X_new = 1.5 × X  -  0.5 × X × X^T × X
```

This is just a **correction formula** — it nudges singular values (the "stretching amounts") toward 1.0 each step.

---

**Singular values — the key concept**

A matrix stretches space differently in different directions. The stretch amounts are called **singular values**.

```
Before orthogonalization:   singular values = [8.2,  3.1,  0.4,  0.01]
                                               big   ok   small  tiny
After orthogonalization:    singular values = [1.0,  1.0,  1.0,  1.0]
                                               all equal!
```

Newton-Schulz is a fast way to push all singular values → 1.0

---

**Why not just use SVD instead?**

You could do exact orthogonalization with SVD:
```python
U, S, Vt = torch.linalg.svd(G)
Q = U @ Vt  # perfect orthogonal matrix
```

But SVD is **very slow** on large matrices. Newton-Schulz does the same thing with just **matrix multiplications** — which GPUs are extremely fast at. 5 iterations ≈ good enough, and 10× faster.

---

**The whole Muon idea in plain English**

```
Normal Adam:
  gradient → scale by history → update weights
             (some dims updated a lot, some barely)

Muon:
  gradient → orthogonalize → update weights
             (every dim updated equally)
             → more balanced, more stable training
```

---

**Minimal working example to see it yourself**

```python
import torch

def orthogonalize(G, steps=10):
    X = G / G.norm()               # normalize first
    for _ in range(steps):
        X = 1.5 * X - 0.5 * X @ X.T @ X   # nudge toward orthogonal
    return X

# Try it
G = torch.randn(4, 4)
Q = orthogonalize(G)

# Check: singular values should all be ≈ 1.0
print("Before:", torch.linalg.svdvals(G).round(decimals=2))
print("After: ", torch.linalg.svdvals(Q).round(decimals=2))
```

Expected output:
```
Before: tensor([2.31, 1.47, 0.83, 0.21])   ← unequal
After:  tensor([1.00, 1.00, 1.00, 1.00])   ← all equal ✓
```

That's it. Newton-Schulz is just a fast, GPU-friendly way to make all singular values equal to 1.

References:
- [Muon Blog – Keller Jordan](https://kellerjordan.github.io/posts/muon/)
- [Singular Value Decomposition – Wikipedia](https://en.wikipedia.org/wiki/Singular_value_decomposition)
- [Muon Source Code](https://github.com/KellerJordan/Muon/blob/master/muon.py)
