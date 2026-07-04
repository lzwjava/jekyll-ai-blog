---
audio: false
generated: true
image: false
lang: en
layout: post
title: Grouped Query Attention Explained
translated: false
type: note
---

**Question:** What is Grouped Query Attention (GQA)?

**Answer:**

GQA is a middle ground between Multi-Head Attention (MHA) and Multi-Query Attention (MQA). The whole point is shrinking the **KV cache** at inference time while losing almost no quality.

**The core idea**

In standard MHA with `n_head` heads, you project Q, K, V into `n_head` separate heads each. In MQA (Shazeer 2019), all query heads share **one** K/V head. GQA (Ainslie et al. 2023, the paper behind Llama 2 70B) generalizes: `n_kv_head` K/V heads, where each K/V head is shared by a **group** of `n_head / n_kv_head` query heads.

```
MHA:  n_kv_head = n_head       (e.g. 32 Q heads, 32 KV heads)
GQA:  n_kv_head = n_head / g   (e.g. 32 Q heads,  8 KV heads)
MQA:  n_kv_head = 1            (e.g. 32 Q heads,  1 KV head)
```

**Why it matters: KV cache math**

KV cache size per token = `2 × n_layer × n_kv_head × head_dim × bytes`. For a Llama-2-70B-like config (80 layers, 64 heads, head_dim 128, fp16):

- MHA: `2 × 80 × 64 × 128 × 2` = 2.6 MB/token → 4K context ≈ 10.7 GB per sequence
- GQA-8: `2 × 80 × 8 × 128 × 2` = 0.33 MB/token → 4K context ≈ 1.3 GB

That's an 8× cut, which directly translates to bigger batch sizes and longer contexts at inference, since decoding is memory-bandwidth bound (each step re-reads the whole KV cache). Quality-wise, the GQA paper shows GQA-8 matches MHA on downstream tasks while MQA degrades noticeably.

**Minimal implementation (the nanoGPT-style diff)**

The only trick is projecting K/V to fewer heads, then broadcasting them across query groups with `repeat_interleave` (or letting `scaled_dot_product_attention(enable_gqa=True)` handle it in PyTorch ≥ 2.5):

```python
import torch, torch.nn as nn
import torch.nn.functional as F

class GQAttention(nn.Module):
    def __init__(self, dim=4096, n_head=32, n_kv_head=8):
        super().__init__()
        self.n_head, self.n_kv_head = n_head, n_kv_head
        self.head_dim = dim // n_head
        self.q_proj = nn.Linear(dim, n_head * self.head_dim, bias=False)
        self.k_proj = nn.Linear(dim, n_kv_head * self.head_dim, bias=False)  # smaller!
        self.v_proj = nn.Linear(dim, n_kv_head * self.head_dim, bias=False)  # smaller!
        self.o_proj = nn.Linear(dim, dim, bias=False)

    def forward(self, x):
        B, T, _ = x.shape
        q = self.q_proj(x).view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, T, self.n_kv_head, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, T, self.n_kv_head, self.head_dim).transpose(1, 2)

        # broadcast each KV head to its group of query heads
        g = self.n_head // self.n_kv_head
        k = k.repeat_interleave(g, dim=1)   # (B, n_head, T, hd)
        v = v.repeat_interleave(g, dim=1)

        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.o_proj(y.transpose(1, 2).reshape(B, T, -1))
```

Note what changed vs MHA: only the **shapes of k_proj/v_proj** and the broadcast. Attention math is identical. Parameter savings are minor (~a few % of the model); the win is almost entirely the KV cache and memory bandwidth at decode time.

**Two things worth knowing beyond the basics**

1. **Uptraining, not retraining.** The GQA paper converted existing MHA checkpoints by **mean-pooling** the K/V head weights within each group, then fine-tuning for ~5% of the original pretraining compute. That's why it caught on so fast — no from-scratch retrain needed.

2. **GQA vs MLA.** Since you're into DeepSeek: DeepSeek's MLA (Multi-head Latent Attention) attacks the same KV-cache problem differently — it compresses K/V into a low-rank latent (`c_kv` of dim ~512) and caches only that, then up-projects at compute time. MLA compresses more aggressively than GQA-8 while keeping per-head expressiveness, at the cost of extra matmuls and RoPE gymnastics (the decoupled RoPE keys). GQA reduces the *number* of KV heads; MLA reduces the *rank* of the KV representation.

Who uses what: Llama 2 70B / Llama 3 (GQA-8), Mistral, Qwen, Gemma 2 → GQA. DeepSeek V2/V3 → MLA. Original GPT-2/nanoGPT → plain MHA, which is why adding GQA to nanoGPT is a nice ~20-line exercise if you want to feel the KV cache shrink yourself.

References:

- [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints (Ainslie et al., 2023)](https://arxiv.org/abs/2305.13245)
- [Fast Transformer Decoding: One Write-Head is All You Need (Shazeer, 2019 — MQA)](https://arxiv.org/abs/1911.02150)
- [DeepSeek-V2 paper (MLA)](https://arxiv.org/abs/2405.04434)
