---
audio: false
generated: true
image: false
lang: en
layout: post
title: "torch.arange: evenly spaced 1D tensor"
translated: false
type: note
---

Question: What does `torch.arange` do?

Answer: Same as Python's `range` / numpy's `arange` — returns a 1D tensor of evenly spaced values over `[start, end)`.

```python
import torch

torch.arange(5)                  # tensor([0, 1, 2, 3, 4])
torch.arange(2, 10, 2)           # tensor([2, 4, 6, 8])   start, end, step
torch.arange(0, 1, 0.25)         # tensor([0.0000, 0.2500, 0.5000, 0.7500])

# dtype/device matter for downstream ops
torch.arange(5, dtype=torch.float32, device='cuda')
```

Signature: `torch.arange(start=0, end, step=1, dtype=None, device=None)`. `end` is exclusive, unlike `torch.linspace` where the endpoint is inclusive by default.

Where you'll actually hit it: building position indices for RoPE/positional embeddings, causal mask construction, indexing into a KV cache.

```python
# classic use: positions for RoPE
seq_len = 8
pos = torch.arange(seq_len)  # tensor([0,1,...,7])

# causal mask
mask = torch.arange(seq_len)[None, :] <= torch.arange(seq_len)[:, None]
```

One gotcha: floating-point `step` can accumulate rounding error near `end`, so for fractional steps `linspace` is often safer than `arange`.

References:
- [torch.arange — PyTorch docs](https://docs.pytorch.org/docs/stable/generated/torch.arange.html)