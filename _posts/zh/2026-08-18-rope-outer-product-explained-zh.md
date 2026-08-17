---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RoPE外积详解
translated: true
type: note
---

问题：在大型语言模型的RoPE（旋转位置编码）中，`torch.outer(t, inv_freq)` 表示什么？

答案：

`torch.outer(t, inv_freq)` 计算两个一维张量的**外积**：

- **`t`** — 表示词元位置的张量：`[0, 1, 2, ..., seq_len-1]`
- **`inv_freq`** — 表示逆频率的张量：对于每个维度对 `i`，值为 `1 / (10000^(2i/d))`

外积运算生成形状为 `[seq_len, d/2]` 的二维矩阵：

```
         维度0      维度1      维度2    ...
位置0 : [ 0·f0,    0·f1,    0·f2,   ... ]
位置1 : [ 1·f0,    1·f1,    1·f2,   ... ]
位置2 : [ 2·f0,    2·f1,    2·f2,   ... ]
...
```

每个单元 `[m, i]` = 位置 `m` × 频率 `fᵢ`，该值成为用于旋转查询/键向量的**角度**。

**这在RoPE中的重要性：**

RoPE通过在二维子空间中旋转Q/K向量来编码位置信息。每个维度对按角度 `θ = m · fᵢ` 旋转，其中：
- `m` = 词元位置（位置越远 → 角度越大）
- `fᵢ` = 频率（低维度旋转较慢，高维度旋转较快）

该矩阵随后扩展为 `cos` 和 `sin` 表：

```python
freqs = torch.outer(t, inv_freq)        # [seq_len, d/2]
emb   = torch.cat([freqs, freqs], dim=-1)  # [seq_len, d]
cos   = emb.cos()
sin   = emb.sin()
```

这些值被应用于Q和K，以注入位置信息，**无需额外**添加单独的位置嵌入向量——位置信息直接编码在旋转过程中。

参考文献：
- [RoFormer: Enhanced Transformer with Rotary Position Embedding (arxiv)](https://arxiv.org/abs/2104.09864)
- [torch.outer — PyTorch文档](https://pytorch.org/docs/stable/generated/torch.outer.html)