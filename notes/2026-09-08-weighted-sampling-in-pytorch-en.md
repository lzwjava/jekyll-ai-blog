---
audio: false
generated: true
image: false
lang: en
layout: post
title: Weighted Sampling in PyTorch
translated: false
type: note
---

Question: What does `torch.multinomial` do in PyTorch?

Answer:

`torch.multinomial` samples indices from a probability distribution defined by a weight tensor. Think of it like a weighted lottery — items with higher weights are more likely to be picked.

**Signature:**
```python
torch.multinomial(input, num_samples, replacement=False, *, generator=None)
```

**Parameters:**

| Parameter | Description |
|---|---|
| `input` | A 1D or 2D tensor of weights (doesn't need to sum to 1) |
| `num_samples` | How many indices to draw |
| `replacement` | If `True`, the same index can be picked multiple times |

**Simple Example:**
```python
import torch

weights = torch.tensor([1.0, 2.0, 7.0])  # index 2 is most likely
samples = torch.multinomial(weights, num_samples=5, replacement=True)
# e.g., tensor([2, 2, 1, 2, 0])  — index 2 appears most often
```

**What it's used for:**

- **Language models** — sampling the next token based on logit probabilities
- **Reinforcement learning** — sampling actions from a policy distribution
- **Data augmentation** — weighted random sampling of data points
- **Monte Carlo methods** — drawing samples from a custom distribution

**2D input (batch mode):**
```python
weights = torch.tensor([[1.0, 9.0],   # row 0: strongly prefers index 1
                         [5.0, 5.0]]) # row 1: equal probability
samples = torch.multinomial(weights, num_samples=3, replacement=True)
# shape: (2, 3) — each row is independently sampled
```

Each row is treated as an independent distribution, and the output shape is `(batch_size, num_samples)`.

References:
- [torch.multinomial — PyTorch Docs](https://pytorch.org/docs/stable/generated/torch.multinomial.html)