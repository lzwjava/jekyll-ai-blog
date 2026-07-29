---
audio: false
generated: true
image: false
lang: en
layout: post
title: "PyTorch squeeze: Removing singleton dimensions"
translated: false
type: note
---

Question: What does `squeeze` do in PyTorch?

Answer: Removes dimensions of size 1. Inverse of `unsqueeze`. Also a view op, no copy.

```python
import torch

x = torch.randn(1, 3, 1, 4)  # shape [1, 3, 1, 4]

x.squeeze().shape       # [3, 4]     -> removes ALL size-1 dims
x.squeeze(0).shape      # [3, 1, 4]  -> removes only dim 0 (if it's size 1)
x.squeeze(2).shape      # [1, 3, 4]  -> removes only dim 2
x.squeeze(1).shape      # [1, 3, 1, 4] -> no-op, dim 1 has size 3, not 1
```

Gotcha: calling `squeeze()` with no args on a batch of size 1 can silently kill your batch dim too.

```python
batch = torch.randn(1, 5)  # 1 sample, 5 features
batch.squeeze().shape      # [5] -> batch dim gone, now looks unbatched
```

This bites people in loss functions and loops that assume a fixed rank — e.g. iterating over "batch" after `squeeze()` when batch size is 1 gives you a scalar/1D tensor instead of a list of one row. Prefer `squeeze(dim)` explicit form in production code, or `squeeze(0)` only when you're sure that dim is the one you want gone.

Common pairing: `unsqueeze` to add a dim for broadcasting, then `squeeze` to remove it after an op.

```python
x = torch.randn(4, 5)
w = torch.randn(5)
out = (x * w.unsqueeze(0)).sum(dim=1, keepdim=True)  # [4,1]
out = out.squeeze(1)  # [4]
```

References:

- [torch.squeeze docs](https://docs.pytorch.org/docs/stable/generated/torch.squeeze.html)
