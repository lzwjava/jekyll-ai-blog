---
audio: false
generated: true
image: false
lang: en
layout: post
title: F.embedding is Functional Embedding
translated: false
type: note
---

Question: Does `F.embedding` refer to `torch.nn.functional.embedding` when `F` is imported via `import torch.nn.functional as F`?

Answer: Yes. `F.embedding(input, weight, ...)` is the functional form of `nn.Embedding`. It's just an index/gather lookup into a weight matrix — no learnable state of its own, you pass the weight tensor in.

```python
import torch
import torch.nn.functional as F

weight = torch.randn(10, 4)  # vocab_size=10, embed_dim=4
input_ids = torch.tensor([1, 3, 5])

out = F.embedding(input_ids, weight)
# equivalent to: weight[input_ids]
print(out.shape)  # torch.Size([3, 4])
```

`nn.Embedding` is just a thin module wrapper that stores `weight` as an `nn.Parameter` and calls `F.embedding` internally in its `forward`:

```python
class Embedding(nn.Module):
    def forward(self, input):
        return F.embedding(input, self.weight, self.padding_idx, ...)
```

Signature: `F.embedding(input, weight, padding_idx=None, max_norm=None, norm_type=2.0, scale_grad_by_freq=False, sparse=False)`. Under the hood it's `torch.embedding`, a C++/CUDA op doing an index_select-style gather — not a matmul, since input is token indices not one-hot vectors.

References:

- [torch.nn.functional.embedding — PyTorch docs](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.embedding.html)
- [torch.nn.Embedding — PyTorch docs](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html)
