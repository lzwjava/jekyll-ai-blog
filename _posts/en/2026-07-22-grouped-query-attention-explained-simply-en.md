---
audio: false
generated: true
image: false
lang: en
layout: post
title: Grouped-Query Attention Explained Simply
translated: false
type: note
---

Question: What is grouped-query attention (GQA)?

Answer: GQA is an interpolation between multi-head attention (MHA) and multi-query attention (MQA), used to cut KV-cache size and memory bandwidth during inference.

**Recap of the two extremes:**

- MHA: `n_heads` separate K/V projections, one per Q head. Best quality, largest KV cache.
- MQA: all Q heads share a *single* K/V head. Smallest KV cache, some quality loss.
- GQA: Q heads are split into `g` groups, each group shares one K/V head. `g=1` → MQA, `g=n_heads` → MHA.

**Why it matters:** at inference, KV cache size scales with `n_kv_heads`, not `n_heads`. Autoregressive decoding is memory-bandwidth bound (you reload the whole KV cache every token), so shrinking `n_kv_heads` directly speeds up decode and lets you fit longer context / bigger batch.

Minimal implementation (the only real change from MHA is repeating K/V heads before the dot product):

```python
import torch
import torch.nn.functional as F

def gqa(x, Wq, Wk, Wv, Wo, n_heads, n_kv_heads, head_dim):
    B, T, D = x.shape
    q = x @ Wq  # (B, T, n_heads*head_dim)
    k = x @ Wk  # (B, T, n_kv_heads*head_dim)
    v = x @ Wv

    q = q.view(B, T, n_heads, head_dim).transpose(1, 2)       # (B, n_heads, T, hd)
    k = k.view(B, T, n_kv_heads, head_dim).transpose(1, 2)    # (B, n_kv_heads, T, hd)
    v = v.view(B, T, n_kv_heads, head_dim).transpose(1, 2)

    # repeat each kv head for its group of q heads
    n_rep = n_heads // n_kv_heads
    k = k.repeat_interleave(n_rep, dim=1)  # (B, n_heads, T, hd)
    v = v.repeat_interleave(n_rep, dim=1)

    out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
    out = out.transpose(1, 2).reshape(B, T, n_heads * head_dim)
    return out @ Wo
```

That's it — same math as MHA, just `k`/`v` get `repeat_interleave`'d before the SDPA call. Everything else (RoPE, causal mask, softmax) is untouched.

**Numbers to anchor on:** Llama 2 70B uses `n_heads=64`, `n_kv_heads=8` (n_rep=8) — 8x KV cache reduction vs MHA with negligible quality drop. Mistral 7B: 32 heads, 8 kv heads.

**Training note:** you don't need to train from scratch — you can "uptrain" an existing MHA checkpoint into GQA by mean-pooling groups of K/V heads and fine-tuning briefly (this is literally how the GQA paper converted T5-XXL).

References:

- [GQA: Training Generalized Multi-Query Transformer Models (Ainslie et al., 2023)](https://arxiv.org/abs/2305.13245)
- [Llama 2 paper, §2.2 architecture](https://arxiv.org/abs/2307.09288)
- [Mistral 7B paper](https://arxiv.org/abs/2310.06825)
