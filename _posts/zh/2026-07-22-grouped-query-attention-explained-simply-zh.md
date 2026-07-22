---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分组查询注意力机制简明解析
translated: true
type: note
---

**问题：什么是分组查询注意力（GQA）？**

**答案：** GQA 是多头注意力（MHA）和多查询注意力（MQA）之间的插值方法，用于在推理过程中减少 KV 缓存大小和内存带宽。

**回顾两种极端情况：**

- MHA：`n_heads` 个独立的 K/V 投影，每个 Q 头对应一个。质量最佳，KV 缓存最大。
- MQA：所有 Q 头共享*单个* K/V 头。KV 缓存最小，质量有所下降。
- GQA：Q 头被分成 `g` 个组，每个组共享一个 K/V 头。`g=1` → MQA，`g=n_heads` → MHA。

**为何重要：** 在推理时，KV 缓存的大小由 `n_kv_heads` 决定，而非 `n_heads`。自回归解码受内存带宽限制（每个 token 都需要重新加载整个 KV 缓存），因此减少 `n_kv_heads` 能直接加速解码，并允许适配更长的上下文或更大的批次。

最小实现（与 MHA 的唯一真正区别是在点积之前重复 K/V 头）：

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

    # 为每个 kv 头在其对应的 q 头组中重复
    n_rep = n_heads // n_kv_heads
    k = k.repeat_interleave(n_rep, dim=1)  # (B, n_heads, T, hd)
    v = v.repeat_interleave(n_rep, dim=1)

    out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
    out = out.transpose(1, 2).reshape(B, T, n_heads * head_dim)
    return out @ Wo
```

就是这样——与 MHA 的计算相同，只是在 SDPA 调用前对 `k`/`v` 进行了 `repeat_interleave`。其余部分（RoPE、因果掩码、softmax）保持不变。

**参考数据：** Llama 2 70B 使用 `n_heads=64`，`n_kv_heads=8`（n_rep=8）——相比 MHA，KV 缓存减少了 8 倍，且质量下降可忽略不计。Mistral 7B：32 个头，8 个 kv 头。

**训练说明：** 你不需要从头训练——可以通过对 K/V 头组进行均值池化并短暂微调，将现有的 MHA 检查点"升级训练"为 GQA（这实际上就是 GQA 论文转换 T5-XXL 的方法）。

参考文献：

- [GQA: 训练广义多查询 Transformer 模型（Ainslie 等，2023）](https://arxiv.org/abs/2305.13245)
- [Llama 2 论文，§2.2 架构](https://arxiv.org/abs/2307.09288)
- [Mistral 7B 论文](https://arxiv.org/abs/2310.06825)
