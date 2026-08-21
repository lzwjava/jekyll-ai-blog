---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch argmax Explained
translated: false
type: note
---

Question: What does `torch.argmax` do in PyTorch?

Answer:

`torch.argmax` returns the **index** of the maximum value in a tensor — not the value itself, but *where* it is.

**Signature:**

```python
torch.argmax(input, dim=None, keepdim=False)
```

**Parameters:**

- `input` — the input tensor
- `dim` — the dimension to reduce along. If `None`, operates on the flattened tensor
- `keepdim` — whether to keep the reduced dimension

**Examples:**

```python
import torch

x = torch.tensor([3, 1, 4, 1, 5, 9, 2, 6])
torch.argmax(x)  # → tensor(5)  (index of value 9)
```

```python
# Along a specific dimension
x = torch.tensor([[1, 3, 2],
                   [4, 0, 5]])

torch.argmax(x, dim=0)  # → tensor([1, 0, 1])  (row index of max per column)
torch.argmax(x, dim=1)  # → tensor([1, 2])     (col index of max per row)
```

**Common use case — classification:**

```python
logits = model(inputs)          # shape: [batch, num_classes]
preds = torch.argmax(logits, dim=1)  # predicted class index per sample
```

It's essentially the PyTorch equivalent of NumPy's `np.argmax`.

References:

- [torch.argmax — PyTorch Docs](https://pytorch.org/docs/stable/generated/torch.argmax.html)
