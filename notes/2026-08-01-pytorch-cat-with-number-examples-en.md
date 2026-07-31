---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch cat with Number Examples
translated: false
type: note
---

Question: Can you show `torch.cat` with actual numbers instead of just shapes?

Answer:

```python
import torch

a = torch.tensor([[1., 2., 3.],
                   [4., 5., 6.]])   # shape (2,3)

b = torch.tensor([[7., 8., 9.],
                   [10., 11., 12.]]) # shape (2,3)

print(torch.cat([a, b], dim=0))
```

`dim=0` → stack along rows (rows just get appended below):

```
tensor([[ 1.,  2.,  3.],
        [ 4.,  5.,  6.],
        [ 7.,  8.,  9.],
        [10., 11., 12.]])   # shape (4, 3)
```

```python
print(torch.cat([a, b], dim=1))
```

`dim=1` → stack along columns (each row from `a` gets `b`'s matching row glued on the right):

```
tensor([[ 1.,  2.,  3.,  7.,  8.,  9.],
        [ 4.,  5.,  6., 10., 11., 12.]])   # shape (2, 6)
```

Mental model: `dim=0` walks down the first axis (index which row block), `dim=1` walks across the second axis (index within row). Whatever dim you pick, that's the dim that grows (2+2=4 for dim0, 3+3=6 for dim1); every other dim must already match.

Real case — KV cache, made concrete:

```python
# k_cache: (batch=1, heads=2, seq=3, head_dim=4)
k_cache = torch.zeros(1, 2, 3, 4)
k_new   = torch.ones(1, 2, 1, 4)  # one new token

k_cache = torch.cat([k_cache, k_new], dim=2)  # seq dim grows: 3 -> 4
print(k_cache.shape)  # torch.Size([1, 2, 4, 4])
```

Every dim matches except `dim=2` (seq length), which is exactly the dim you're appending the new token onto.
