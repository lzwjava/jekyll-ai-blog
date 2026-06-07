---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-Head Attention Dimensions
translated: false
type: note
---

**Question:** In the multi-head attention reshape, what do the dimensions B, nh, T, hs represent, and how does (1, 12, 2, 64) map to them?

**Answer:**

Correct mapping. Given `v = (1, 12, 2, 64)`:

| Dimension | Symbol | Meaning | Value in your example |
|-----------|--------|---------|----------------------|
| **B** | Batch size | Number of sequences processed in parallel | 1 |
| **nh** | Number of heads | How many independent attention subspaces | 12 |
| **T** | Sequence length | Number of tokens | 2 |
| **hs** | Head size | Embedding dimension **per head** | 64 |

**Why the reshape matters:**

Original shape before the view: `(B, T, C)` = `(1, 2, 768)`
- C is the full embedding dimension (12 heads × 64 dims = 768)

After `view(B, T, self.n_head, C // self.n_head)`: `(1, 2, 12, 64)`
- Splits C into separate heads

After `transpose(1, 2)`: `(1, 12, 2, 64)` = `(B, nh, T, hs)`
- Moves head dimension forward so attention happens **per head in parallel**

**The computation that follows:**
```python
# Attention scores: (B, nh, T, T)
scores = (q @ k.transpose(-2, -1)) * (hs ** -0.5)
attn = softmax(scores, dim=-1)

# Output: (B, nh, T, hs)
out = attn @ v
```

Each of the 12 heads independently computes attention over the 2 tokens with 64-dimensional keys/queries/values. Then concatenate heads back to C=768. This parallelization is why multi-head attention scales well.

In your case (T=2), you're working with a very short sequence — useful for debugging, but real inference has T ranging from 100s to 100k+ tokens depending on context window.
