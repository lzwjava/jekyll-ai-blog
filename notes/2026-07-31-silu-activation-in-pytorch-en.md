---
audio: false
generated: true
image: false
lang: en
layout: post
title: SiLU Activation in PyTorch
translated: false
type: note
---

Question: What does `F.silu(x)` mean in PyTorch?

Answer:

SiLU (Sigmoid Linear Unit), aka Swish:

```
silu(x) = x * sigmoid(x) = x / (1 + exp(-x))
```

```python
import torch
import torch.nn.functional as F

x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
print(F.silu(x))
# tensor([-0.2384, -0.2689,  0.0000,  0.7311,  1.7616])

# manual equivalent
def silu(x):
    return x * torch.sigmoid(x)

print(silu(x))  # same
```

Shape: for `x < 0` it dips slightly negative (min ≈ -0.278 at x ≈ -1.278) before rising, unlike ReLU which hard-zeros. Smooth, non-monotonic, differentiable everywhere — better gradient flow than ReLU near zero, no dead-neuron problem.

Derivative:

```
silu'(x) = sigmoid(x) + x * sigmoid(x) * (1 - sigmoid(x))
         = silu(x) + sigmoid(x) * (1 - silu(x))
```

Where you'll actually see it: SwiGLU in LLaMA/Mistral/Qwen MLP blocks —

```python
def swiglu(x, W, V, W2):
    return (F.silu(x @ W) * (x @ V)) @ W2
```

This is why it matters for you — every modern transformer MLP you're training on MI300X uses this instead of plain GELU-MLP. `F.silu` is literally the gate activation in that block.

References:

- [torch.nn.functional.silu docs](https://pytorch.org/docs/stable/generated/torch.nn.functional.silu.html)
- [SwiGLU paper — Shazeer, GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202)
