---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分组查询注意力详解
translated: true
type: note
---

**问题：** 什么是分组查询注意力（GQA）？

**答案：**

GQA 是多头注意力（MHA）和多查询注意力（MQA）之间的折中方案。其核心目标是在推理时缩减 **KV 缓存** 的大小，同时几乎不损失质量。

**核心思想**

在标准的 MHA 中，`n_head` 个头分别独立地对 Q、K、V 进行投影。在 MQA（Shazeer 2019）中，所有查询头共享 **一个** K/V 头。GQA（Ainslie 等人，2023，Llama 2 70B 的论文）将其推广：使用 `n_kv_head` 个 K/V 头，每个 K/V 头由一组 `n_head / n_kv_head` 个查询头共享。

```
MHA:  n_kv_head = n_head       （例如 32 个 Q 头，32 个 KV 头）
GQA:  n_kv_head = n_head / g   （例如 32 个 Q 头， 8 个 KV 头）
MQA:  n_kv_head = 1            （例如 32 个 Q 头， 1 个 KV 头）
```

**为何重要：KV 缓存计算**

每个 token 的 KV 缓存大小 = `2 × n_layer × n_kv_head × head_dim × bytes`。以类似 Llama-2-70B 的配置（80 层，64 个头，head_dim 128，fp16）为例：

- MHA：`2 × 80 × 64 × 128 × 2` = 2.6 MB/token → 4K 上下文 ≈ 10.7 GB/序列
- GQA-8：`2 × 80 × 8 × 128 × 2` = 0.33 MB/token → 4K 上下文 ≈ 1.3 GB

这实现了 8 倍的缩减，在推理时直接转化为更大的批处理大小和更长的上下文，因为解码过程受内存带宽约束（每一步都要重新读取整个 KV 缓存）。在质量方面，GQA 论文表明 GQA-8 在下游任务上与 MHA 持平，而 MQA 则明显退化。

**最小化实现（nanoGPT 风格差异）**

唯一的技巧是将 K/V 投影到更少的头上，然后通过 `repeat_interleave` 将它们广播到查询组（或者在 PyTorch ≥ 2.5 中使用 `scaled_dot_product_attention(enable_gqa=True)` 处理）：

```python
import torch, torch.nn as nn
import torch.nn.functional as F

class GQAttention(nn.Module):
    def __init__(self, dim=4096, n_head=32, n_kv_head=8):
        super().__init__()
        self.n_head, self.n_kv_head = n_head, n_kv_head
        self.head_dim = dim // n_head
        self.q_proj = nn.Linear(dim, n_head * self.head_dim, bias=False)
        self.k_proj = nn.Linear(dim, n_kv_head * self.head_dim, bias=False)  # 更小的投影！
        self.v_proj = nn.Linear(dim, n_kv_head * self.head_dim, bias=False)  # 更小的投影！
        self.o_proj = nn.Linear(dim, dim, bias=False)

    def forward(self, x):
        B, T, _ = x.shape
        q = self.q_proj(x).view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, T, self.n_kv_head, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, T, self.n_kv_head, self.head_dim).transpose(1, 2)

        # 将每个 KV 头广播到其对应的查询头组
        g = self.n_head // self.n_kv_head
        k = k.repeat_interleave(g, dim=1)   # (B, n_head, T, hd)
        v = v.repeat_interleave(g, dim=1)

        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.o_proj(y.transpose(1, 2).reshape(B, T, -1))
```

注意与 MHA 相比的变化：仅仅是 **k_proj/v_proj 的形状** 以及广播操作。注意力计算本身是完全相同的。参数节省量很小（约占模型的几个百分点）；其优势几乎完全体现在解码时的 KV 缓存和内存带宽上。

**值得了解的两点额外知识**

1. **提升训练（Uptraining），而非重新训练。** GQA 论文通过 **平均池化** 每组内的 K/V 头权重，将现有的 MHA 检查点转换为 GQA 格式，然后进行约原始预训练计算量 5% 的微调。这就是它迅速流行的原因——不需要从头重新训练。

2. **GQA 与 MLA 的对比。** 既然你对 DeepSeek 感兴趣：DeepSeek 的 MLA（多头潜在注意力）以不同方式解决相同的 KV 缓存问题——它将 K/V 压缩为低秩潜在表示（`c_kv`，维度约 512），只缓存该表示，然后在计算时进行上投影。MLA 比 GQA-8 压缩得更激进，同时保持每个头的表达能力，代价是额外的矩阵乘法和 RoPE 处理（解耦的 RoPE 键）。GQA 减少了 KV 头的 **数量**；MLA 减少了 KV 表示的 **秩**。

谁在使用什么：Llama 2 70B / Llama 3（GQA-8）、Mistral、Qwen、Gemma 2 → GQA。DeepSeek V2/V3 → MLA。原始的 GPT-2/nanoGPT → 普通 MHA，这就是为什么在 nanoGPT 中添加 GQA 是一个很好的约 20 行练习，如果你想让 KV 缓存规模自己缩小的话。

参考文献：

- [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints (Ainslie et al., 2023)](https://arxiv.org/abs/2305.13245)
- [Fast Transformer Decoding: One Write-Head is All You Need (Shazeer, 2019 — MQA)](https://arxiv.org/abs/1911.02150)
- [DeepSeek-V2 paper (MLA)](https://arxiv.org/abs/2405.04434)