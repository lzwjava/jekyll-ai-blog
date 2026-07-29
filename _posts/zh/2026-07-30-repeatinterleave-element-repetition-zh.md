---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重复交织元素重复
translated: true
type: note
---

问题：`repeat_interleave` 在 PyTorch 中的作用是什么？

答案：沿指定维度连续重复张量的每个*元素*。与 `repeat`/`tile` 不同，后者将整个张量作为一个块重复。

```python
import torch

x = torch.tensor([1, 2, 3])

x.repeat_interleave(2)
# tensor([1, 1, 2, 2, 3, 3])   <- 每个元素在原位重复

x.repeat(2)
# tensor([1, 2, 3, 1, 2, 3])   <- 整个序列被平铺
```

在二维张量上按维度操作：

```python
x = torch.tensor([[1, 2], [3, 4]])

x.repeat_interleave(2, dim=0)
# tensor([[1, 2],
#         [1, 2],
#         [3, 4],
#         [3, 4]])

x.repeat_interleave(2, dim=1)
# tensor([[1, 1, 2, 2],
#         [3, 3, 4, 4]])
```

按元素的重复次数（不仅仅是标量）——传入一个张量：

```python
x = torch.tensor([1, 2, 3])
x.repeat_interleave(torch.tensor([1, 2, 3]))
# tensor([1, 2, 2, 3, 3, 3])
```

实际用例——这正好是 GQA（分组查询注意力）扩展 KV 头以匹配 Q 头的方式，无需通过 einsum 技巧为每个查询头创建副本：

```python
# kv: [batch, n_kv_heads, seq, head_dim]
# n_rep = n_q_heads // n_kv_heads
kv_expanded = kv.repeat_interleave(n_rep, dim=1)
# 现在形状为 [batch, n_q_heads, seq, head_dim]，每个 kv 头重复 n_rep 次
# 连续排列，以便与对应的 q 头块对齐
```

在 beam search 中也很常见（按 beam 数量扩展 batch 维度）以及在卷积层之前的上采样操作中。

参考文档：
- [torch.repeat_interleave 文档](https://docs.pytorch.org/docs/stable/generated/torch.repeat_interleave.html)