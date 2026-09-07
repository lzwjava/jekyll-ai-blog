---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KV缓存预填充复制
translated: true
type: note
---

问题：这个 KV 缓存实现中的 `prefill` 方法有什么作用？

答案：

该方法**将缓存的 Key-Value 数据从一个缓存复制到另一个缓存**，从而在共享的 prefill 之后实现高效的并行采样。

## 背景：为什么存在这个方法

一种常见的推理优化模式：

1. 在 prompt 上**运行一次 prefill**（batch=1）——成本高，但只需要一次
2. 将该 KV 缓存**复制**到 N 个独立的缓存中
3. 运行 **N 个并行解码流**（不同的样本/温度）——每个都从相同的 prompt 状态开始

---

## 逐步分解

```python
assert self.get_pos() == 0
```

目标缓存必须为**空**——你不能向一个已使用过的缓存中做 prefill。

```python
assert self.n_layers == other.n_layers and self.n_heads == other.n_heads and self.head_dim == other.head_dim
```

健全性检查——两个缓存必须具有**兼容的架构维度**。

```python
assert self.max_seq_len >= other.max_seq_len
```

目标缓存必须具有**至少与源缓存相同的容量**。

```python
other_pos = other.get_pos()
self.k_cache[:, :, :other_pos, :, :] = other.k_cache[:, :, :other_pos, :, :]
self.v_cache[:, :, :other_pos, :, :] = other.v_cache[:, :, :other_pos, :, :]
```

只复制源 K 和 V 张量的**已填充部分**（截至 `other_pos`），其余部分保持不变。张量形状可能为 `[batch, n_layers, seq_len, n_heads, head_dim]`。

```python
self.cache_seqlens.fill_(other_pos)
```

告诉目标缓存中的**每个 batch 槽位**，它当前持有 `other_pos` 个 token——因此解码会从正确的位置继续。

```python
if other.prev_embedding is not None:
    self.prev_embedding = other.prev_embedding.expand(self.batch_size, -1, -1).clone()
```

处理一种“smear”操作：源缓存是 batch=1，但目标缓存有 `num_samples` 个 batch 槽位。`.expand()` 将单个 embedding 广播到所有 batch 槽位，然后 `.clone()` 使其成为一个具体的（非视图）张量，从而每个样本可以独立地分叉。

---

## 可视化流程

```
Source Cache (batch=1, after prompt prefill)
  k_cache: [1, layers, prompt_len, heads, dim]
  v_cache: [1, layers, prompt_len, heads, dim]
         │
         │  prefill()
         ▼
Dest Cache (batch=N, now ready to generate)
  k_cache: [N, layers, prompt_len, heads, dim]  ← same prompt KV for all N
  v_cache: [N, layers, prompt_len, heads, dim]
  cache_seqlens: [prompt_len, prompt_len, ..., prompt_len]  ← N slots
```

这 N 个解码流随后都会从这个共享起点开始**独立地追加新 token**。
