---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding torch.cat and torch.stack
translated: false
type: note
---

Question: What does `torch.cat` do?

Answer: Concatenates a sequence of tensors along an existing dimension. No new dimension is created (unlike `torch.stack`). All tensors must match shape on every dim except the concat dim.

```python
import torch

a = torch.randn(2, 3)
b = torch.randn(2, 3)

torch.cat([a, b], dim=0).shape  # torch.Size([4, 3])  -> stacks rows
torch.cat([a, b], dim=1).shape  # torch.Size([2, 6])  -> stacks cols
```

Common uses you'll actually hit:

```python
# KV cache append (autoregressive decoding)
k_cache = torch.cat([k_cache, k_new], dim=seq_dim)

# Concatenating along batch dim for multi-GPU gather
gathered = torch.cat(tensor_list, dim=0)

# Skip connections (U-Net, etc.) — channel concat, not add
x = torch.cat([up_features, skip_features], dim=1)
```

Gotcha: `cat` requires an existing dim to match (e.g. concat two `(2,3)` on dim 0 → `(4,3)`). `stack` requires *all* dims to match and adds a new one (`(2,3)` + `(2,3)` on dim 0 → `(2,2,3)`). If you're building a KV cache or doing skip connections, you want `cat`; if you're batching independent same-shape tensors into a new leading dim, you want `stack`.

References:

- [torch.cat — PyTorch docs](https://pytorch.org/docs/stable/generated/torch.cat.html)
- [torch.stack — PyTorch docs](https://pytorch.org/docs/stable/generated/torch.stack.html)
