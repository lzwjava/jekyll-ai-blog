---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Understanding PyTorch Broadcasting in NanoGPT
translated: false
type: note
---

Great question! This is a very common point of confusion when first looking at the NanoGPT or GPT-2 code.

Let's look at the shapes carefully:

```python
tok_emb = self.transformer.wte(idx)    # Shape: (B, T, n_embd)
pos_emb = self.transformer.wpe(pos)    # Shape: (T, n_embd)   ← only 1D!
```

How can you add `(B, T, n_embd)` + `(T, n_embd)`?

**Answer: PyTorch automatically broadcasts the position embeddings across the batch dimension.**

When PyTorch sees:
```python
tok_emb + pos_emb
```
it treats `pos_emb` (shape `(T, n_embd)`) as if it were `(1, T, n_embd)` and then **broadcasts** it to match `(B, T, n_embd)`.

So this addition becomes:
```
(B, T, n_embd)
     +
(1, T, n_embd)   ← automatically added by broadcasting
     =
(B, T, n_embd)
```

This is exactly how the original GPT-2 and all modern transformer implementations work — position embeddings are shared across all sequences in the batch.

You can verify this works in Python:

```python
import torch
B, T, C = 2, 3, 768
tok_emb = torch.randn(B, T, C)
pos_emb = torch.randn(T, C)

result = tok_emb + pos_emb
print(result.shape)  # → torch.Size([2, 3, 768])
```

No error, works perfectly.

So in NanoGPT (and the original GPT-2), this line is 100% correct and intentional:

```python
x = self.transformer.drop(tok_emb + pos_emb)
```

It's relying on PyTorch's broadcasting — clean, efficient, and standard practice.

No need for `pos_emb.unsqueeze(0)` or anything else. Broadcasting does the job elegantly.
