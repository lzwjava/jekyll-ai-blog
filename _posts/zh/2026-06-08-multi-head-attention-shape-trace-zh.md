---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多头注意力形状追踪
translated: true
type: note
---

以下是完整的注意力前向传播过程，其中穿插了代码和形状追踪：

```python
B, T, C = x.size()
  # x: (1, 5, 768)

q, k, v = self.c_attn(x).split(self.n_embd, dim=2)
  # q: (1, 5, 768)  k: (1, 5, 768)  v: (1, 5, 768)

k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
  # k: (1, 5, 12, 64) -> 转置 -> (1, 12, 5, 64)

q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
  # q: (1, 5, 12, 64) -> 转置 -> (1, 12, 5, 64)

v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
  # v: (1, 5, 12, 64) -> 转置 -> (1, 12, 5, 64)

# --- flash 路径 (CUDA/MPS) ---
y = scaled_dot_product_attention(q, k, v, is_causal=True)
  # y: (1, 12, 5, 64)   # (B, nh, T, hs)

# --- 手动路径 (CPU/回退) ---
att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
  # att: (1, 12, 5, 5)  # (B, nh, T, T) = (B,nh,T,hs) @ (B,nh,hs,T)

att = att.masked_fill(self.bias[:,:,:T,:T] == 0, float('-inf'))
  # att: (1, 12, 5, 5)  # 上三角填充为 -inf

att = F.softmax(att, dim=-1)
  # att: (1, 12, 5, 5)  # 行求和为1

att = self.attn_dropout(att)
  # att: (1, 12, 5, 5)

y = att @ v
  # y: (1, 12, 5, 64)   # (B,nh,T,T) @ (B,nh,T,hs) -> (B,nh,T,hs)

# --- 两条路径在此合并 ---
y = y.transpose(1, 2).contiguous().view(B, T, C)
  # y: (1, 12, 5, 64) -> 转置 -> (1, 5, 12, 64) -> view -> (1, 5, 768)

y = self.c_proj(y)
  # y: (1, 5, 768)      # (B, T, C) -> (B, T, C)

y = self.resid_dropout(y)
  # y: (1, 5, 768)

return y
```

关键的形状变换是多头重塑：`768 = 12 头 × 64 维度`。矩阵乘法 `q @ k^T` 正是产生 `(T, hs) @ (hs, T) -> (T, T)` 注意力分数的位置。
