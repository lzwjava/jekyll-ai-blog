---
audio: false
generated: true
image: false
lang: en
layout: post
title: RoFormer's Rotational Positional Encoding
translated: false
type: note
---

Question: Intro to RoFormer / RoPE (arxiv 2104.09864)

Answer:

## Core idea

Standard position encoding is additive: `x_i + p_i`. RoPE is multiplicative: rotate the query/key vectors by an angle proportional to position. Rotation naturally gives you relative position for free, because a dot product between two rotated vectors only depends on the *difference* of their rotation angles.

## The 2D case (this is the whole trick)

Pick pair of dims, treat as complex number. For position `m`, rotate by `mθ`:

```
f(x, m) = x * e^(imθ)   # complex mult = 2D rotation
```

Then for query at pos `m`, key at pos `n`:

```
<f(q,m), f(k,n)> = Re[q * conj(k) * e^(i(m-n)θ)]
```

Result only depends on `m - n`, i.e. **relative position emerges from absolute rotation**. That's the entire derivation in Section 3.4.1 — it's an algebra exercise, nothing deep.

## Generalize to d dims

Split `d` into `d/2` pairs, each pair gets its own frequency:

```
θ_i = 10000^(-2(i-1)/d),  i = 1..d/2
```

Same frequency schedule as sinusoidal PE (Vaswani), but instead of adding `sin/cos` vectors to `x`, you rotate `x` block-diagonally:

```
R_Θ,m = blockdiag(R(mθ_1), R(mθ_2), ..., R(mθ_{d/2}))
q_m = R_Θ,m @ (W_q x_m)
k_n = R_Θ,n @ (W_k x_n)
```

Attention score `q_m^T k_n = x_m^T W_q^T R_Θ,(n-m) W_k x_n` — pure function of `n-m`.

## Minimal implementation (this is what's actually in every modern LLM: LLaMA, GPT-NeoX, Qwen, etc.)

```python
import torch

def rope_freqs(dim, seq_len, base=10000.0, device="cpu"):
    theta = 1.0 / (base ** (torch.arange(0, dim, 2, device=device).float() / dim))
    pos = torch.arange(seq_len, device=device).float()
    freqs = torch.outer(pos, theta)  # [seq_len, dim/2]
    return torch.cos(freqs), torch.sin(freqs)

def apply_rope(x, cos, sin):
    # x: [batch, heads, seq, dim]
    x1, x2 = x[..., ::2], x[..., 1::2]
    cos = cos[None, None, :, :]
    sin = sin[None, None, :, :]
    rotated = torch.stack([x1 * cos - x2 * sin,
                            x1 * sin + x2 * cos], dim=-1)
    return rotated.flatten(-2)

# usage
dim, seq_len = 64, 128
cos, sin = rope_freqs(dim, seq_len)
q = torch.randn(1, 8, seq_len, dim)
k = torch.randn(1, 8, seq_len, dim)
q_rot = apply_rope(q, cos, sin)
k_rot = apply_rope(k, cos, sin)
scores = q_rot @ k_rot.transpose(-2, -1)  # relative-position-aware attention
```

That's Eq. 34 in the paper (the sparse/efficient realization) — no need to materialize the full block-diagonal rotation matrix, just elementwise multiply-and-swap on pairs.

## Why it stuck (properties, Section 3.3)

- **Long-term decay**: `θ_i = 10000^(-2i/d)` makes high-frequency pairs decay dot-product contribution as `|m-n|` grows — matches the intuition that far-apart tokens should attend less (Fig 2 in paper, empirically validated not proven tight).
- **Sequence length flexibility**: no learned position table, works at any length since it's just a function of `m`. This is the real reason it won — extrapolation/interpolation (later work: NTK-aware scaling, YaRN, linear scaling) all build on this because RoPE has a closed-form angle you can rescale.
- **Composable with linear attention**: since rotation preserves norm, you can rotate `ϕ(q)`/`φ(k)` outputs directly (Eq 19) — this is why Performer+RoPE works.
- No extra parameters, no added compute beyond the rotation.

## What it's missing (paper's own limitations section)

No theoretical explanation for *why* it converges faster or generalizes better on long text — just empirical (BLEU +0.2, faster BERT MLM convergence, long-text CAIL2019-SCM gains). The math only proves the *mechanism* (rotation → relative position), not the *training dynamics* benefit.

## What came after (you'll want this more than the original paper)

- **NTK-aware / YaRN scaling** — extending context length by rescaling `θ_i` instead of retraining.
- **ALiBi** — competing approach, additive bias instead of rotation, simpler but less commonly used now.
- Every modern open model (LLaMA, Qwen, DeepSeek, Mistral) uses RoPE as default — worth checking their `θ` base value choices (LLaMA uses 10000, some long-context models push base to 500k–1M for extrapolation).

References:

- [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/pdf/2104.09864)
- [EleutherAI RoPE blog (good visual walkthrough)](https://blog.eleuther.ai/rotary-embeddings/)
