---
audio: false
generated: true
image: false
lang: en
layout: post
title: torch.chunk in PyTorch Explained
translated: false
type: note
---

Question: What does `torch.chunk` do in PyTorch?

Answer: Splits a tensor into a specific number of chunks along a given dimension. If the dimension size doesn't divide evenly, all chunks are equal size except the last one, which is smaller.

```python
import torch

x = torch.arange(10)
chunks = torch.chunk(x, 3)  # split into 3 pieces along dim=0
for c in chunks:
    print(c, c.shape)

# tensor([0, 1, 2, 3]) torch.Size([4])
# tensor([4, 5, 6, 7]) torch.Size([4])
# tensor([8, 9])       torch.Size([2])   <- last chunk smaller, not equal
```

Key signature:

```python
torch.chunk(input, chunks, dim=0)
```

- `chunks`: number of pieces requested. You may get **fewer** than this if the dim size is too small (never more).
- Unlike `torch.split`, you specify the *count* of chunks, not the *size* of each chunk.
- Returns a tuple of views (no copy) when possible — same underlying storage, so modifying one chunk in-place can mutate the original tensor if it's contiguous and shares memory.

Comparison you'll actually hit in transformer code — splitting QKV projections:

```python
qkv = torch.randn(2, 10, 3 * 768)  # (batch, seq, 3*d_model)
q, k, v = qkv.chunk(3, dim=-1)     # each (2, 10, 768)
```

This is the standard pattern in attention implementations (e.g. GPT-2 `c_attn` output) — one big linear projection, then `chunk(3, dim=-1)` to split into Q, K, V instead of three separate linear layers.

Gotcha: if `dim_size % chunks != 0`, chunk sizes are uneven (ceil-based), whereas `torch.split(x, size)` lets you control exact size per split and `torch.tensor_split` guarantees exactly `n` chunks even when it doesn't divide evenly (redistributing the remainder across the first few chunks instead of dumping it all in the last one).

References:

- [torch.chunk — PyTorch docs](https://pytorch.org/docs/stable/generated/torch.chunk.html)
- [torch.tensor_split — PyTorch docs](https://pytorch.org/docs/stable/generated/torch.tensor_split.html)
