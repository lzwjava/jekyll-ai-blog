---
audio: false
generated: true
image: false
lang: en
layout: post
title: repeat_interleave element repetition
translated: false
type: note
---

Question: What does `repeat_interleave` do in PyTorch?

Answer: Repeats each *element* of a tensor consecutively, along a given dim. Different from `repeat`/`tile`, which repeats the whole tensor as a block.

```python
import torch

x = torch.tensor([1, 2, 3])

x.repeat_interleave(2)
# tensor([1, 1, 2, 2, 3, 3])   <- each element repeated in place

x.repeat(2)
# tensor([1, 2, 3, 1, 2, 3])   <- whole sequence tiled
```

Per-dim, with 2D tensors:

```python
x = torch.tensor([[1, 2], [3, 4]])

x.repeat_interleave(2, dim=0)
# tensor([[1, 2],
#         [1, 2],
#         [3, 4],
#         [3, 4]])

x.repeat_interleave(2, dim=1)
# tensor([[1, 1, 2, 2],
#         [3, 3, 4, 4]])
```

Per-element repeat counts (not just a scalar) — pass a tensor:

```python
x = torch.tensor([1, 2, 3])
x.repeat_interleave(torch.tensor([1, 2, 3]))
# tensor([1, 2, 2, 3, 3, 3])
```

Real use case — this is exactly how GQA (grouped-query attention) expands KV heads to match Q heads without materializing a copy per query head via einsum tricks:

```python
# kv: [batch, n_kv_heads, seq, head_dim]
# n_rep = n_q_heads // n_kv_heads
kv_expanded = kv.repeat_interleave(n_rep, dim=1)
# now [batch, n_q_heads, seq, head_dim], each kv head repeated n_rep times
# consecutively so it lines up with the corresponding block of q heads
```

Also common in beam search (expanding batch dim by beam count) and in upsampling ops before conv layers.

References:
- [torch.repeat_interleave docs](https://docs.pytorch.org/docs/stable/generated/torch.repeat_interleave.html)
