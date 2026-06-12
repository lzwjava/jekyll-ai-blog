---
audio: false
generated: true
image: false
lang: en
layout: post
title: Single AdamW and MuonAdamW Hybrid
translated: false
type: note
---

**Question:** In the nanochat/nanoGPT-style optimizer config, what do "Single AdamW" and "MuonAdamW (Muon for matrices, AdamW for embeddings/scalars)" mean?

**Answer:**

This table is describing two optimizer setups, the second being the hybrid scheme Karpathy uses in nanochat and the modded-nanogpt speedruns.

## AdamW (the baseline)

Adam with decoupled weight decay. Per-parameter adaptive learning rates from running moment estimates:

```python
m = beta1 * m + (1 - beta1) * g          # 1st moment (momentum)
v = beta2 * v + (1 - beta2) * g**2       # 2nd moment (per-param variance)
update = lr * m_hat / (v_hat.sqrt() + eps)
p -= update + lr * wd * p                # decoupled weight decay
```

"Single AdamW" = one optimizer for every parameter in the model. Simple, robust, 2 extra state tensors per param (m, v).

## Muon (MomentUm Orthogonalized by Newton-Schulz)

Muon only makes sense for **2D weight matrices** (attention projections, MLP weights). The core idea: take the momentum-SGD update and **orthogonalize** it before applying. If the momentum buffer has SVD `M = U S Vᵀ`, Muon replaces it with `U Vᵀ` — i.e., it sets all singular values to 1.

Why? A raw gradient update is typically dominated by a few large singular directions, so most of the matrix's "directions" barely get updated. Orthogonalizing spreads the update energy uniformly across all directions — every rank-1 component of the weight matrix moves at the same rate. Empirically this trains transformers ~1.3–2x more compute-efficiently than AdamW at small-to-mid scale, and Moonshot validated it at scale (Kimi K2 was trained with MuonClip).

Computing the SVD exactly is too slow, so Muon approximates `UVᵀ` with ~5 iterations of a quintic **Newton–Schulz** polynomial in bfloat16:

```python
import torch

def zeropower_via_newtonschulz5(G, steps=5):
    # Approximates UV^T for G = U S V^T, i.e. orthogonalizes G
    a, b, c = (3.4445, -4.7750, 2.0315)
    X = G.bfloat16()
    if G.size(-2) > G.size(-1):
        X = X.mT
    X = X / (X.norm(dim=(-2, -1), keepdim=True) + 1e-7)  # spectral norm <= 1
    for _ in range(steps):
        A = X @ X.mT
        B = b * A + c * A @ A
        X = a * X + B @ X        # quintic: pushes singular values -> 1
    if G.size(-2) > G.size(-1):
        X = X.mT
    return X

class Muon(torch.optim.Optimizer):
    def __init__(self, params, lr=0.02, momentum=0.95):
        super().__init__(params, dict(lr=lr, momentum=momentum))

    @torch.no_grad()
    def step(self):
        for group in self.param_groups:
            for p in group["params"]:
                g = p.grad
                state = self.state[p]
                if "buf" not in state:
                    state["buf"] = torch.zeros_like(g)
                buf = state["buf"]
                buf.mul_(group["momentum"]).add_(g)
                g = g.add(buf, alpha=group["momentum"])   # nesterov
                O = zeropower_via_newtonschulz5(g)
                # scale so update RMS is shape-independent
                scale = max(1, p.size(-2) / p.size(-1)) ** 0.5
                p.add_(O, alpha=-group["lr"] * scale)
```

Note the polynomial only needs matmuls — GPU-friendly, and the FLOP overhead is small relative to the backward pass. State is just 1 momentum buffer per matrix (vs 2 for AdamW), so it's also lighter on memory.

## Why the hybrid (MuonAdamW)

Orthogonalization is only meaningful for dense 2D matrices acting as linear maps. So nanochat splits parameters:

```python
matrix_params = [p for p in model.parameters() if p.ndim == 2 and not is_embedding(p)]
other_params  = [p for p in model.parameters() if p not in matrix_params]
# embeddings, lm_head, norms/scalars/biases

opts = [
    Muon(matrix_params, lr=0.02, momentum=0.95),
    torch.optim.AdamW(other_params, lr=3e-4, betas=(0.9, 0.95)),
]
for opt in opts: opt.step()
```

Embeddings get sparse, row-wise gradients (only tokens in the batch get signal), so a global orthogonalization of the embedding matrix is the wrong operation — AdamW's per-parameter adaptivity handles that regime much better. Same for the lm_head, and 1D params (LayerNorm gains, biases) can't be orthogonalized at all.

So the table is contrasting: the boring-but-safe single-optimizer config vs. the speedrun-proven config where the bulk of the FLOPs (the transformer's weight matrices) get Muon and everything else stays on AdamW.

If you're running nanochat on the MI300X, the hybrid is the one to use — it's the default for a reason, and Newton-Schulz is pure matmul so ROCm handles it fine.

**References:**

- [Muon: An optimizer for hidden layers in neural networks — Keller Jordan](https://kellerjordan.github.io/posts/muon/)
- [modded-nanogpt (speedrun repo where Muon emerged)](https://github.com/KellerJordan/modded-nanogpt)
- [Muon is Scalable for LLM Training (Moonlight, Moonshot AI)](https://arxiv.org/abs/2502.02982)
- [nanochat](https://github.com/karpathy/nanochat)
