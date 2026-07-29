---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch unsqueeze Explained
translated: false
type: note
---

Question: What does `unsqueeze` do in PyTorch?

Answer: Inserts a dimension of size 1 at the specified position. It's the inverse of `squeeze`. No data copy, just a view (metadata change on strides).

```python
import torch

x = torch.arange(6).reshape(2, 3)  # shape [2, 3]

x.unsqueeze(0).shape   # [1, 2, 3]  -> insert at front
x.unsqueeze(1).shape   # [2, 1, 3]  -> insert in middle
x.unsqueeze(-1).shape  # [2, 3, 1]  -> insert at end
x.unsqueeze(2).shape   # [2, 3, 1]  -> same as -1 here
```

Index semantics: for tensor of dim `n`, valid range for `dim` is `[-(n+1), n]`. The new dim gets inserted *before* that index in the output shape.

Common use case — batch dim for a single sample:

```python
img = torch.randn(3, 224, 224)      # C, H, W
batch = img.unsqueeze(0)            # [1, 3, 224, 224]
```

Or broadcasting alignment, e.g. adding a bias per-row:

```python
a = torch.randn(4, 5)
b = torch.randn(4)
c = a + b.unsqueeze(1)  # b: [4] -> [4,1], broadcasts against [4,5]
```

It's a view op — `x.unsqueeze(0).data_ptr() == x.data_ptr()` is `True`. Gradients flow through fine since it's just a reshape in the autograd graph.

References:

- [torch.unsqueeze docs](https://docs.pytorch.org/docs/stable/generated/torch.unsqueeze.html)
