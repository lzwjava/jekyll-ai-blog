---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: PyTorch Parameter for Learnable Weights
translated: false
type: note
---

`torch.nn.Parameter` is a subclass of `torch.Tensor` in PyTorch, designed specifically for representing learnable parameters in neural network modules. Its main purpose is to automatically register tensors as module parameters when they're assigned as attributes to a `torch.nn.Module`, making them accessible via methods like `module.parameters()` or `module.named_parameters()`. This helps distinguish trainable weights (e.g., for layers) from regular tensors, preventing temporary computations (like cached states in RNNs) from being mistakenly treated as parameters.

### Key Features
- **Automatic Registration**: When you assign a `Parameter` to a module (e.g., `self.weight = nn.Parameter(torch.randn(3, 3))` in a custom module's `__init__`), it's added to the module's parameter list without extra code.
- **Gradient Tracking**: By default, `requires_grad=True`, so it participates in backpropagation. This holds even inside a `torch.no_grad()` context—use autograd's local disabling for finer control.
- **Attributes**: It inherits all `Tensor` properties but adds no new ones beyond its special module behavior.

### Basic Usage
Here's a simple example in a custom module:

```python
import torch
import torch.nn as nn

class MyModule(nn.Module):
    def __init__(self):
        super().__init__()
        # This gets auto-registered as a parameter
        self.weight = nn.Parameter(torch.randn(2, 3))
        # A plain tensor won't be registered
        self.bias = torch.zeros(3)

    def forward(self, x):
        return x @ self.weight + self.bias

model = MyModule()
print(list(model.parameters()))  # Outputs: [Parameter containing: tensor(...)]
```

For more details, check the official docs: [Parameter — PyTorch 2.9 documentation](https://pytorch.org/docs/stable/generated/torch.nn.parameter.Parameter.html)
