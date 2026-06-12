---
audio: false
generated: true
image: false
lang: en
layout: post
title: Jane Street’s Attention Research Explained
translated: false
type: note
---

**Question:** How does Jane Street publish its transformer/attention research, and what does that research actually say?

**Answer:**

## How they publish

Jane Street doesn't publish papers at NeurIPS/ICML the way a lab would — they publish through their **tech blog** (blog.janestreet.com), which has a dedicated machine learning section. It's a thin but high-signal channel: the ML category currently contains only a handful of posts — "Using group theory to explore the space of positional encodings for attention" (Apr 2026), "Deep-Learning the Hardest Go Problem in the World" (2019), "Accelerating Self-Play Learning in Go" (2019), "L2 Regularization and Batch Norm" (2019), and "Does batch size matter?" (2017). They also run ML "capture-the-flag" style puzzles — a recent post studies neural networks with theoretical visualization tools under the framing "can you reverse-engineer our neural network" — plus the Signals & Threads podcast, tech talks on YouTube, and Kaggle competitions (they've released anonymized market-data forecasting datasets). The pattern: they publish *foundational/theoretical* ML insights and recreational research, never their actual alpha-generating models. The blog is partly a recruiting funnel.

## What the attention post actually says

The flagship attention piece is by Alok Puranik (ML researcher there since 2020). The core question: attention's query-key dot product says nothing about sequence position, so you perturb it with a positional encoding — and the post asks: what is the complete space of valid positional encodings?

The derivation, condensed:

**Setup.** Encode position by transforming queries/keys with time-dependent matrices: `q'(t) = F(t)q(t)`, `k'(s) = G(s)k(s)`, so the attention score becomes `qᵀ F(t)ᵀG(s) k`. Three axioms:

1. **Linearity** — F, G are linear maps (matrices)
2. **Translation invariance** — `F(t)ᵀG(s)` depends only on `t−s` (relative position only; this is what lets you generalize past training length)
3. **Continuity** in time

**Key move.** Define `A(t−s) = F(t)ᵀG(s)`. The axioms force `A(0) = I` and `A(t₁)A(t₂) = A(t₁+t₂)` — i.e., the matrices A(t) form a one-parameter group, which means every valid encoding has the form A(t) = exp(tL) for some fixed generator matrix L. Now enumeration reduces to classifying generators:

- **Diagonalizable L, eigenvalue analysis per subspace:** real eigenvalue α > 0 blows up exponentially (discard); α = 0 recovers NoPE; α < 0 gives the exponential decay common in linear-attention variants (and gated models like Mamba should be viewed as learning how far to advance time, not changing the decay rate). Complex-conjugate eigenvalue pairs give 2D rotation blocks — you've derived RoPE, with an exponential damping factor; this damped RoPE is exactly what RetNet and Mamba-3 use.
- **Defective (non-diagonalizable) L:** Jordan blocks produce **polynomial** terms in time — a technically legal but unexplored class with no found literature and probably no practical application. An addendum shows ALiBi's `−m(t−s)` penalty is actually realizable via a defective 2×2 nilpotent generator with augmented q/k.

**The punchline:** there are only a few families of valid positional encodings, and all the sensible ones — NoPE, decay, RoPE, damped RoPE — are already in use, so there's no undiscovered perfect encoding to find. Note the framing leak about their work: they work with sequential models (market time series) and explicitly handle continuous or irregularly sampled time, not just integer token indices — that's the quant-finance fingerprint on the math.

## Minimal implementation of the punchline (damped RoPE)

The whole taxonomy collapses to one parameterization — per 2D subspace, a frequency ω and a decay α ≤ 0:

```python
import torch

def damped_rope(x, t, omega, alpha):
    """x: (..., T, d), t: (T,), omega/alpha: (d//2,)
    A(t) = exp(tL); L = block-diag of [[alpha, -omega],[omega, alpha]]
    => per-pair: e^{alpha*t} * rotation(omega*t)
    alpha = 0          -> vanilla RoPE
    omega = 0, alpha<0 -> RetNet/linear-attn decay
    both 0             -> NoPE
    """
    x1, x2 = x[..., 0::2], x[..., 1::2]
    theta = t[:, None] * omega[None, :]            # (T, d//2)
    scale = torch.exp(t[:, None] * alpha[None, :]) # decay for q; use -alpha for k
    cos, sin = torch.cos(theta), torch.sin(theta)
    out = torch.empty_like(x)
    out[..., 0::2] = scale * (x1 * cos - x2 * sin)
    out[..., 1::2] = scale * (x1 * sin + x2 * cos)
    return out
```

Apply with `+alpha·t` scaling on queries and `−alpha·s` on keys so the dot product picks up `e^{alpha(t−s)}` — decay in relative time only (causal masking required, or far-future keys explode).

For your nanoGPT/nanochat work this is directly useful: it tells you the RoPE-vs-ALiBi-vs-decay design space is *closed* under reasonable axioms, so encoding experiments should focus on frequency schedules and learned/data-dependent time advancement (the Mamba-style gating view) rather than hunting for novel functional forms.

**References:**

- [Using group theory to explore the space of positional encodings for attention — Jane Street Blog](https://blog.janestreet.com/using-group-theory-to-explore-positional-encodings-attention/)
- [Jane Street Blog — Machine Learning category](https://blog.janestreet.com/machine-learning/)
- [RetNet paper (exponentially damped rotation)](https://arxiv.org/abs/2307.08621)
- [GRAPE: Group Representational Positional Encoding (Zhang et al.) — the closely related paper the post acknowledges](https://arxiv.org/abs/2512.07805)
