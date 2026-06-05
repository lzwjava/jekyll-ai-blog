---
audio: false
generated: true
image: false
lang: en
layout: post
title: Embedding versus Head Dimension Explained
translated: false
type: note
---

**Question:** In nanoGPT/nanochat with embedding dim 768 and head dim 128, what's the difference between these two dimensions?

**Answer:**

They're not alternatives — they're **related dimensions in multi-head attention**:

- **Embedding dim (768)** = total hidden state size for every token
- **Head dim (128)** = the slice size of that embedding that each attention head operates on

With 768 embedding dim and 128 head dim, you have **768 / 128 = 6 attention heads**.

Here's the flow:

```python
batch_size, seq_len = 2, 10
embed_dim = 768
num_heads = 6
head_dim = embed_dim // num_heads  # 128

# Token embeddings
x = torch.randn(batch_size, seq_len, embed_dim)  # (2, 10, 768)

# Linear projections to Q, K, V
W_q = torch.randn(embed_dim, embed_dim)
Q = x @ W_q  # (2, 10, 768)

# Reshape to separate heads
Q = Q.reshape(batch_size, seq_len, num_heads, head_dim)  # (2, 10, 6, 128)
Q = Q.transpose(1, 2)  # (2, 6, 10, 128) — now we have 6 heads, each operating on 128-dim

# Each head computes attention independently
K = x @ W_k  # (2, 10, 768)
K = K.reshape(batch_size, seq_len, num_heads, head_dim).transpose(1, 2)  # (2, 6, 10, 128)

# Attention: (Q @ K^T) @ V, all in 128-dim space per head
scores = Q @ K.transpose(-2, -1)  # (2, 6, 10, 10) — attention logits
attn_weights = softmax(scores / sqrt(128), dim=-1)  # scale by sqrt(head_dim)

V = x @ W_v
V = V.reshape(batch_size, seq_len, num_heads, head_dim).transpose(1, 2)  # (2, 6, 10, 128)

out = attn_weights @ V  # (2, 6, 10, 128) — each head outputs 128-dim

# Concatenate all heads back
out = out.transpose(1, 2)  # (2, 10, 6, 128)
out = out.reshape(batch_size, seq_len, embed_dim)  # (2, 10, 768)
```

**Key insight:** Each head attends independently on its 128-dim projection, then you concatenate all 6 heads' outputs to recover the full 768-dim representation. This gives you **parallel, diverse attention patterns** without increasing compute (6 heads × 128-dim = 768-dim total, same as a single 768-dim attention).

The `sqrt(head_dim)` scaling in attention is crucial — it stabilizes gradients across different head dimensions.

For nanoGPT scale (768-dim, 6 heads), this is typical. Larger models like GPT-3 use 12,288-dim with 96 heads (128-dim per head) — same ratio.
