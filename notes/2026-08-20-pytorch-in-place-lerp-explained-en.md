---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch in-place lerp explained
translated: false
type: note
---

Question: What does `lerp_` mean?

Answer: `lerp_` is an **in-place linear interpolation** operation, commonly seen in PyTorch and similar frameworks.

- `lerp` stands for **linear interpolation** — computing a value between two points based on a weight parameter `t`:

```
result = start + t * (end - start)
```

- The trailing **underscore `_`** is a convention (especially in PyTorch) indicating the operation is **in-place**, meaning it modifies the tensor directly rather than returning a new one.

So `tensor.lerp_(end, weight)` is equivalent to:

```
tensor = tensor + weight * (end - tensor)
```

where `weight` is a scalar between 0.0 and 1.0:

- `weight = 0.0` → result equals the original tensor
- `weight = 1.0` → result equals `end`
- `weight = 0.5` → result is the midpoint

Common uses include smooth animations, blending model weights, and gradient-based optimization.

References:

- [PyTorch torch.lerp documentation](https://pytorch.org/docs/stable/generated/torch.lerp.html)
- [Linear interpolation — Wikipedia](https://en.wikipedia.org/wiki/Linear_interpolation)
