---
audio: false
generated: true
image: false
lang: en
layout: post
title: RoPE Outer Product Explained
translated: false
type: note
---

Question: What does `torch.outer(t, inv_freq)` mean in the context of RoPE (Rotary Position Embedding) in LLMs?

Answer:

`torch.outer(t, inv_freq)` computes the **outer product** of two 1D tensors:

- **`t`** — a tensor of token positions: `[0, 1, 2, ..., seq_len-1]`
- **`inv_freq`** — a tensor of inverse frequencies: `1 / (10000^(2i/d))` for each dimension pair `i`

The outer product produces a 2D matrix of shape `[seq_len, d/2]`:

```
         dim0      dim1      dim2  ...
pos 0: [ 0·f0,    0·f1,    0·f2,  ... ]
pos 1: [ 1·f0,    1·f1,    1·f2,  ... ]
pos 2: [ 2·f0,    2·f1,    2·f2,  ... ]
...
```

Each cell `[m, i]` = position `m` × frequency `fᵢ`, which becomes the **angle** used to rotate query/key vectors.

**Why this matters in RoPE:**

RoPE encodes position by rotating Q/K vectors in 2D subspaces. Each pair of dimensions gets rotated by angle `θ = m · fᵢ`, where:

- `m` = token position (farther token → bigger angle)
- `fᵢ` = frequency (lower dimensions rotate slower, higher ones faster)

This matrix is then expanded into `cos` and `sin` tables:

```python
freqs = torch.outer(t, inv_freq)        # [seq_len, d/2]
emb   = torch.cat([freqs, freqs], dim=-1)  # [seq_len, d]
cos   = emb.cos()
sin   = emb.sin()
```

These are applied to Q and K to inject positional information **without adding** a separate position embedding vector — the position is baked into the rotation itself.

References:

- [RoFormer: Enhanced Transformer with Rotary Position Embedding (arxiv)](https://arxiv.org/abs/2104.09864)
- [torch.outer — PyTorch docs](https://pytorch.org/docs/stable/generated/torch.outer.html)
