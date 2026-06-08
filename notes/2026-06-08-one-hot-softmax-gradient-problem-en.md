---
audio: false
generated: true
image: false
lang: en
layout: post
title: One-Hot Softmax Gradient Problem
translated: false
type: note
---

**Question:** In the context of attention without scaling, what does "one-hot softmax" mean and why does it cause gradient problems?

**Answer:**

A one-hot vector is a vector where one element is (nearly) 1 and all others are (nearly) 0.

In unscaled attention:
- Dot products range [-500, 500] (large values)
- `softmax(z) = exp(z) / sum(exp(z))` amplifies these differences exponentially
- One token's attention weight becomes ~0.99999, all others ~0.00001

**Why this kills gradients:**

The softmax gradient is:
```
dL/dq_i = dL/d(softmax) * d(softmax)/dq_i
```

For softmax, the Jacobian per element is:
```
∂softmax_j / ∂z_i = softmax_j * (δ_ij - softmax_i)
```

When softmax is one-hot (say, softmax_j ≈ 1, all others ≈ 0):
- For the dominant position: `∂softmax_j / ∂z_j = 1 * (1 - 1) = 0`
- For others: `∂softmax_k / ∂z_i ≈ 0 * (0 - 1) ≈ 0`

**Result:** All gradients → 0. The query, key, and value projections receive vanishing gradients.

**How scaling fixes it:**

With `scale = 1/√d_k`:
- Dot products now range [-2, 2] (softmax stays "soft")
- Multiple tokens get non-trivial attention weights
- Gradients flow through all positions

```python
# Unscaled: attention_weights ≈ [0.99999, 0.00001, 0.00000]
# dL/dq contracts to near-zero across all dimensions

# Scaled: attention_weights ≈ [0.68, 0.24, 0.08]
# dL/dq has non-zero flow through multiple paths
```

This is why the Transformer paper uses `d_k = 64` and scales by `1/√64 = 0.125`—keeps dot products in the [−√d_k, √d_k] range where softmax remains differentiable.
