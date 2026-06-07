---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-Head Attention Shape Trace
translated: false
type: note
---

Here's the full attention forward pass with code + shape trace interleaved:

```python
B, T, C = x.size()
  # x: (1, 5, 768)

q, k, v = self.c_attn(x).split(self.n_embd, dim=2)
  # q: (1, 5, 768)  k: (1, 5, 768)  v: (1, 5, 768)

k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
  # k: (1, 5, 12, 64) -> transpose -> (1, 12, 5, 64)

q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
  # q: (1, 5, 12, 64) -> transpose -> (1, 12, 5, 64)

v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
  # v: (1, 5, 12, 64) -> transpose -> (1, 12, 5, 64)

# --- flash path (CUDA/MPS) ---
y = scaled_dot_product_attention(q, k, v, is_causal=True)
  # y: (1, 12, 5, 64)   # (B, nh, T, hs)

# --- manual path (CPU/fallback) ---
att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
  # att: (1, 12, 5, 5)  # (B, nh, T, T) = (B,nh,T,hs) @ (B,nh,hs,T)

att = att.masked_fill(self.bias[:,:,:T,:T] == 0, float('-inf'))
  # att: (1, 12, 5, 5)  # upper triangle filled with -inf

att = F.softmax(att, dim=-1)
  # att: (1, 12, 5, 5)  # rows sum to 1

att = self.attn_dropout(att)
  # att: (1, 12, 5, 5)

y = att @ v
  # y: (1, 12, 5, 64)   # (B,nh,T,T) @ (B,nh,T,hs) -> (B,nh,T,hs)

# --- both paths merge here ---
y = y.transpose(1, 2).contiguous().view(B, T, C)
  # y: (1, 12, 5, 64) -> transpose -> (1, 5, 12, 64) -> view -> (1, 5, 768)

y = self.c_proj(y)
  # y: (1, 5, 768)      # (B, T, C) -> (B, T, C)

y = self.resid_dropout(y)
  # y: (1, 5, 768)

return y
```

The key shape transformation is the multi-head reshape: `768 = 12 heads × 64 dim`. The matmul `q @ k^T` is where the `(T, hs) @ (hs, T) -> (T, T)` attention scores happen.
