---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch lerp_ In-Place Linear Interpolation
translated: false
type: note
---

Question: What does `lerp_` mean in Python (specifically PyTorch)?

Answer:

`lerp_` is the **in-place version of `lerp`** (Linear Interpolation).

**`lerp` formula:**

```
result = start + weight * (end - start)
```

Or equivalently:

```
result = (1 - weight) * start + weight * end
```

The trailing underscore `_` is a **PyTorch convention** meaning the operation modifies the tensor **in-place** (no new tensor is allocated).

**Example:**

```python
import torch

a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([10.0, 20.0, 30.0])

# in-place: a is modified directly
a.lerp_(b, weight=0.5)
# a is now: tensor([5.5, 11.0, 16.5])
# = 1 + 0.5*(10-1), 2 + 0.5*(20-2), 3 + 0.5*(30-3)
```

**vs non-in-place:**

```python
result = torch.lerp(a, b, weight=0.5)  # returns a new tensor, a unchanged
a.lerp_(b, weight=0.5)                 # modifies a directly
```

**Common use cases:**

- Smooth transitions / animations
- Model weight averaging (e.g., EMA — Exponential Moving Average)
- Blending values in ML training loops

References:

- [torch.lerp — PyTorch Docs](https://pytorch.org/docs/stable/generated/torch.lerp.html)
