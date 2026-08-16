---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sliding Window GQA Attention
translated: false
type: note
---

Question: How does `_sdpa_attention(q, k, v, window_size, enable_gqa)` work when `q, k, v` are `(B, H, T, D)`?

Answer:

This is basically a thin wrapper around **PyTorch's `scaled_dot_product_attention` (SDPA)**, with two extra features:

1. **Sliding-window attention** — each token only attends to nearby tokens.
2. **GQA** — query heads can be more numerous than KV heads.

The conceptual operation is:

[
\text{Attention}(Q,K,V)
=======================

\operatorname{softmax}\left(\frac{QK^T}{\sqrt D} + M\right)V
]

where `M` is the attention mask.

### 1. Normal SDPA

Suppose:

```python
q.shape = (B, Hq, Tq, D)
k.shape = (B, Hk, Tk, D)
v.shape = (B, Hk, Tk, D)
```

PyTorch expects:

```python
F.scaled_dot_product_attention(
    q, k, v,
    ...
)
```

and internally does roughly:

```python
scores = q @ k.transpose(-2, -1)
scores = scores / sqrt(D)

scores += mask

attn = softmax(scores, dim=-1)

out = attn @ v
```

So the important shape transformation is:

```text
q:      (B, Hq, Tq, D)
k.T:    (B, Hk, D, Tk)

                 ↓ matmul

scores: (B, Hq, Tq, Tk)

                 ↓ softmax

attn:   (B, Hq, Tq, Tk)

                 ↓ @ V

out:    (B, Hq, Tq, D)
```

For autoregressive LLM attention, usually `Tq = Tk = T`.

---

## 2. What does `window_size` do?

Imagine:

```text
tokens:

0 1 2 3 4 5 6 7 8 9
```

Normal causal attention at token 7:

```text
0 1 2 3 4 5 6 7
              ↑
```

Token 7 can attend to **everything before it**.

With a sliding window of 4:

```text
0 1 2 3 4 5 6 7 8 9
        └───┘ ↑
```

token 7 only attends to:

```text
4 5 6 7
```

So the attention matrix becomes approximately:

```text
        K →
       0 1 2 3 4 5 6 7
Q 0    1
  1    1 1
  2    1 1 1
  3    1 1 1 1
  4        1 1 1 1
  5          1 1 1 1
  6            1 1 1 1
  7              1 1 1 1
```

The key point:

**window attention is implemented through the mask, not by changing the fundamental attention equation.**

Conceptually:

```python
mask = causal_mask & sliding_window_mask

F.scaled_dot_product_attention(
    q, k, v,
    attn_mask=mask,
)
```

Recent PyTorch SDPA implementations can also represent causal/sliding-window behavior more efficiently without explicitly materializing the entire `T × T` mask, depending on the backend.

---

## 3. What does `enable_gqa` mean?

This is about **Grouped Query Attention**.

For example:

```text
Q heads = 32
K heads = 8
V heads = 8
```

Instead of storing 32 independent K/V heads, we share each KV head across 4 Q heads:

```text
Q0  Q1  Q2  Q3  → K0 V0
Q4  Q5  Q6  Q7  → K1 V1
...
```

Hence:

```python
Hq = 32
Hkv = 8
```

and:

```python
Hq / Hkv = 4
```

With GQA, K/V are effectively repeated:

```python
k = repeat_interleave(k, Hq // Hkv, dim=1)
v = repeat_interleave(v, Hq // Hkv, dim=1)
```

Conceptually:

```text
K:

before:

K0 K1 K2 K3 K4 K5 K6 K7

after:

K0 K0 K0 K0 K1 K1 K1 K1 K2 K2 K2 K2 ...
```

But a good SDPA backend can avoid literally materializing all those copies.

That's the reason for:

```python
enable_gqa=True
```

---

## 4. So `_sdpa_attention` is probably very small

A typical implementation is conceptually:

```python
import torch.nn.functional as F

def _sdpa_attention(q, k, v, window_size, enable_gqa):
    """
    q, k, v: (B, H, T, D)
    """

    return F.scaled_dot_product_attention(
        q,
        k,
        v,
        is_causal=True,
        enable_gqa=enable_gqa,
        # sliding-window mask here
    )
```

The interesting part isn't the Python function.

**The real work happens inside SDPA's kernel.**

Depending on your GPU/PyTorch combination, SDPA may dispatch to things like:

```text
PyTorch
   │
   ▼
scaled_dot_product_attention
   │
   ├── FlashAttention-style kernel
   ├── memory-efficient attention
   └── math/reference implementation
```

This is why SDPA is so useful: your model code says

```python
F.scaled_dot_product_attention(q, k, v)
```

while PyTorch chooses a highly optimized implementation underneath.

---

## 5. Why SDPA is much faster than writing this yourself

Naive Python/PyTorch:

```python
scores = q @ k.transpose(-2, -1)
scores = scores / math.sqrt(q.size(-1))

scores = scores.masked_fill(mask == 0, float("-inf"))

probs = scores.softmax(dim=-1)

out = probs @ v
```

For sequence length `T`, this creates:

```text
QKᵀ
(B, H, T, T)
```

which can be enormous.

For:

```text
B = 1
H = 32
T = 8192
```

the attention matrix contains:

```text
32 × 8192 × 8192
≈ 2.15 billion elements
```

At FP16 that's roughly:

```text
4.3 GB
```

just for one attention matrix.

FlashAttention/SDPA avoids materializing the full `T × T` matrix in HBM. It computes attention in tiles:

```text
             K/V
       ┌────┬────┬────┬────┐
       │    │    │    │    │
       ├────┼────┼────┼────┤
 Q     │tile│tile│tile│tile│
       ├────┼────┼────┼────┤
       │tile│tile│tile│tile│
       └────┴────┴────┴────┘
```

and performs the softmax incrementally.

That's the core idea behind **FlashAttention**.

So if you're reading this inside an LLM inference implementation, `_sdpa_attention()` is essentially the abstraction boundary:

```text
                    LLM layer
                       │
                       ▼
              _sdpa_attention()
                       │
                       ▼
        scaled_dot_product_attention()
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        causal mask          GQA / MQA
             │                   │
             └─────────┬─────────┘
                       ▼
                optimized GPU
                   attention
```

If you paste the **full `_sdpa_attention` implementation**, especially the code that constructs `window_size`, I can walk through it **line-by-line with actual tensor shapes**, including exactly how the sliding-window mask works.
