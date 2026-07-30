---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RoPE 实现详解
translated: true
type: note
---

以下是 RoPE（旋转位置编码）实现的详细解析：

---

## `apply_rotary_emb` — 核心旋转函数

```python
def apply_rotary_emb(x, cos, sin):
    x1, x2 = torch.chunk(x.float(), 2, dim=-1)
    y1 = x1 * cos - x2 * sin
    y2 = x2 * cos + x1 * sin
    return torch.cat((y1, y2), dim=-1).to(x.dtype)
```

**功能：** 对输入中每一对维度应用二维旋转。

- 将最后一个维度分成两半：`x1`（偶数索引维度）和 `x2`（奇数索引维度）
- 应用旋转矩阵：
  ```
  [y1]   = [cos  -sin] [x1]
  [y2]     [sin   cos] [x2]
  ```
- 转换为 float32 以保证精度，然后恢复为原始 dtype

这样，每一对连续的维度 `(d, d+1)` 都根据位置旋转了一个角度，使模型能够通过旋转后的查询和键的点积来编码相对位置信息。

---

## `RotaryEmbedding.__init__` — 预计算缓存

```python
inv_freq = 1.0 / (base**(torch.arange(0, rotary_dim, 2, dtype=torch.float) / rotary_dim))
```

计算每一对维度的**逆频率**。对于 `rotary_dim = 64`，得到 32 个频带：

```
inv_freq[i] = 1.0 / base^(2i / rotary_dim)
```

这些频率呈几何级数递减——前几对旋转快（高频），后几对旋转慢（低频）。

```python
t = torch.arange(max_position_embeddings, dtype=torch.float)
freqs = torch.einsum("i,j -> ij", t, inv_freq)
```

位置索引 × 频率的外积 → 形状 `[max_pos, rotary_dim/2]`。这为每个位置 × 频率对赋予旋转角度。

```python
cos = freqs.cos()
sin = freqs.sin()
cache = torch.cat((cos, sin), dim=-1).unsqueeze_(1)
```

计算 cos/sin 并拼接：形状 `[max_pos, 1, rotary_dim]`。`unsqueeze_(1)` 添加一个虚拟的 head 维度，使其可在各 head 间广播。

```
self.register_buffer("cos_sin_cache", cache, persistent=False)
```

注册为非持久性 buffer（不会保存在 `state_dict` 中），因为它可以从配置中重新计算。

---

## `RotaryEmbedding.forward` — 在给定位置应用

```python
cos_sin = self.cos_sin_cache[positions]    # [batch, 1, rotary_dim]
cos, sin = cos_sin.chunk(2, dim=-1)        # [batch, 1, rotary_dim/2] each
query = apply_rotary_emb(query, cos, sin)
key = apply_rotary_emb(key, cos, sin)
```

- 根据给定位置索引预计算缓存
- 将缓存拆分为 cos/sin 两半
- 对查询和键同时进行旋转

---

## `get_rope` — 单例工厂

```python
@lru_cache(1)
def get_rope(head_size, rotary_dim, max_position, base):
    rotary_emb = RotaryEmbedding(head_size, rotary_dim, max_position, base)
    return rotary_emb
```

缓存工厂，确保每个唯一配置只会创建一个 `RotaryEmbedding` 实例。由于这些参数在整个模型中通常保持不变，因此实际上是单例模式。

---

## 数据流可视化总结

```
positions: [batch]                 query/key: [batch, heads, seq_len, head_size]
    │                                      │
    ▼                                      │
cos_sin_cache[max_pos, 1, dim]             │
    │                                      │
    ▼                                      ▼
cos_sin = cache[positions]  ──chunk──► cos, sin
  [batch, 1, dim]              [batch, 1, dim/2] each
                                       │
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
              query = rot(query, cos, sin)   key = rot(key, cos, sin)
```

关键点：因为 Q 和 K 都使用**相同**的与位置相关的角度进行旋转，所以位置 `(i, j)` 处的点积 `Q·K` 自然地编码了**相对**位置 `(i - j)`，这就是 RoPE 具有相对位置行为的原因。