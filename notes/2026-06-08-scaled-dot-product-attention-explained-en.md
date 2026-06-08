---
audio: false
generated: true
image: false
lang: en
layout: post
title: Scaled Dot-Product Attention Explained
translated: false
type: note
---

**Question:** What does the scaled dot-product attention formula compute, and why is it structured that way?

**Answer:**

This is the **scaled dot-product attention** core — the first step in computing how much each token "looks at" every other token.

## Breakdown

```python
att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
```

### Part 1: `q @ k.transpose(-2, -1)` — Raw Compatibility Scores

- `q`: query vectors, shape `(B, nh, T, d_k)` where `B=batch, nh=num_heads, T=seq_len, d_k=head_dim`
- `k.transpose(-2, -1)`: key vectors transposed to `(B, nh, d_k, T)`
- `@` (matrix multiply): produces `(B, nh, T, T)` — a square matrix where `[i, j]` = how much query position `i` "matches" key position `j`

This is a **similarity score**. If `q[i]` and `k[j]` are aligned, their dot product is large. If orthogonal, it's near zero.

### Part 2: `* (1.0 / math.sqrt(k.size(-1)))` — Scaling

Why divide by `sqrt(d_k)`?

When `d_k` is large (say 64), the dot products grow large too. Large values get pushed into the flat tail regions of softmax, killing gradients during backprop.

**Empirical effect:**

```
Without scaling (d_k=64):
  dot products ~ range [-500, 500]
  softmax is nearly one-hot
  dL/dq ~ tiny gradient

With scaling (divide by sqrt(64)=8):
  dot products ~ range [-7, 7]
  softmax is smooth
  dL/dq ~ healthy gradient
```

The scale factor `1/sqrt(d_k)` normalizes variance. If you initialize `q` and `k` with zero mean and variance 1, their dot product has variance `d_k`. Dividing by `sqrt(d_k)` brings it back to variance 1 — statistically stable.

## Full Context (Forward Pass)

```python
def scaled_dot_product_attention(q, k, v, mask=None):
    # q, k, v: (B, nh, T, d_k)

    # Step 1: Compute attention scores
    scores = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))  # (B, nh, T, T)

    # Step 2: Mask (optional) — zero out future positions in causal attention
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)

    # Step 3: Softmax to get attention weights
    weights = F.softmax(scores, dim=-1)  # (B, nh, T, T) — rows sum to 1

    # Step 4: Apply weights to values
    output = weights @ v  # (B, nh, T, d_k)

    return output
```

## Shape Flow

```
q: (4, 8, 100, 64)           batch=4, heads=8, seq_len=100, head_dim=64
k: (4, 8, 100, 64)
———————————————————
q @ k.T: (4, 8, 100, 100)    — each query compares to all keys
* scale: (4, 8, 100, 100)    — same shape, just scaled values
→ softmax: (4, 8, 100, 100)  — attention weights, each row sums to 1
→ @ v: (4, 8, 100, 64)       — weighted average of values
```

**Key insight:** Attention is a learned, differentiable **routing mechanism**. At position `i`, the softmax weights tell you which positions to pay attention to. The `1/sqrt(d_k)` scaling keeps the softmax in a healthy regime.
