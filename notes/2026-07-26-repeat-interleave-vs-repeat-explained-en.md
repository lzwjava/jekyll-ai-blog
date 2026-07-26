---
audio: false
generated: true
image: false
lang: en
layout: post
title: Repeat Interleave vs Repeat Explained
translated: false
type: note
---

Question: What does `torch.repeat_interleave` do, as a general tensor op (not GQA-specific)?

Answer:

It repeats each element along a dimension *in place*, before moving to the next element — as opposed to `repeat`, which tiles the whole sequence.

```python
import torch

x = torch.tensor([1, 2, 3])

x.repeat_interleave(2)
# tensor([1, 1, 2, 2, 3, 3])   <- each element repeated 2x, then next element

x.repeat(2)
# tensor([1, 2, 3, 1, 2, 3])   <- whole sequence tiled 2x
```

**With `dim` argument** — repeats slices along that dim, keeping other dims intact:

```python
x = torch.tensor([[1, 2],
                   [3, 4]])

x.repeat_interleave(2, dim=0)
# tensor([[1, 2],
#         [1, 2],
#         [3, 4],
#         [3, 4]])   <- each ROW duplicated before next row

x.repeat_interleave(2, dim=1)
# tensor([[1, 1, 2, 2],
#         [3, 3, 4, 4]])   <- each COLUMN duplicated before next column
```

**Per-element repeat counts** (not just a scalar) — you can pass a tensor specifying how many times each element repeats:

```python
x = torch.tensor([1, 2, 3])
x.repeat_interleave(torch.tensor([1, 2, 3]))
# tensor([1, 2, 2, 3, 3, 3])
```

This is why it's the right tool for GQA head expansion — you want KV head 0 → 0,0,0,0, KV head 1 → 1,1,1,1 (block-adjacent duplicates), not a retiled `0,1,2,3,0,1,2,3` pattern that `repeat` would give you.