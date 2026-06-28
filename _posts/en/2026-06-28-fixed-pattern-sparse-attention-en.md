---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed-Pattern Sparse Attention
translated: false
type: note
---

These are related-work entries from a paper on sparse/efficient attention. Here's the intro context:

**Sparse Transformer (Child et al., 2019)** is the foundational work on *fixed-pattern* sparse attention. The core problem: full self-attention is O(n²) in sequence length — every token attends to every other token. For long sequences (images flattened to thousands of tokens, audio, long documents), this is prohibitive in both compute and memory.

The key insight: instead of dense attention, **factorize the attention pattern** into a fixed, content-agnostic sparse structure. Each token attends to only O(√n) positions, giving O(n√n) total complexity.

Two factorized heads:
- **Strided attention** — each position attends to the previous `l` positions (local window) and every `l`-th position (strided/dilated). Natural for data with periodic structure like images, where `l ≈ √n` matches the row width.
- **Fixed attention** — specific columns/positions act as routing tokens that aggregate and broadcast information globally. Better for data without clear periodic structure (text).

Minimal sketch of the strided pattern:

```python
import torch

def strided_mask(n, l):
    # l ~ sqrt(n); each token i attends to local window + strided positions
    idx = torch.arange(n)
    i, j = idx[:, None], idx[None, :]
    local = (i - j >= 0) & (i - j < l)        # previous l positions
    strided = (i >= j) & ((i - j) % l == 0)   # every l-th position back
    return local | strided                     # causal block-sparse pattern
```

"Content-agnostic" is the load-bearing phrase: the sparsity pattern is fixed before you see the data, determined purely by position. This is what distinguishes it from later *content-based* approaches (Reformer's LSH bucketing, Routing Transformer's clustering) where which tokens attend to which depends on the actual key/query values. Your paper is almost certainly contrasting its method against this fixed-pattern baseline — the `BlockSparse` lineage starts here.

Worth knowing the paper also contributed engineering pieces orthogonal to the sparsity: recomputation of attention matrices to save memory (gradient checkpointing applied to attention), and fused block-sparse GPU kernels. Those are why it was practical, not just theoretical.

Want me to trace the lineage forward — how Longformer/BigBird generalized the fixed patterns, or how the content-based branch diverged?
