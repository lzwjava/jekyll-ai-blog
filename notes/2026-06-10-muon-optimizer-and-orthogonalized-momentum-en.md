---
audio: false
generated: true
image: false
lang: en
layout: post
title: Muon Optimizer and Orthogonalized Momentum
translated: false
type: note
---

**Question:** What is the Muon optimizer, and why does nanochat use it (with Newton-Schulz iteration) for weight matrices instead of AdamW?

**Answer:**

## The one-line idea

Muon (**M**oment**U**m **O**rthogonalized by **N**ewton-Schulz, by Keller Jordan, late 2024) takes the standard SGD-momentum update for a 2D weight matrix, **orthogonalizes** it (replaces the update matrix with the nearest semi-orthogonal matrix), then applies it. That's it. It only applies to hidden-layer weight matrices — embeddings, `lm_head`, norms, and biases still use AdamW, which is exactly the split you see in nanochat's `setup_optimizers`.

## Why orthogonalize the update?

Take the momentum-smoothed gradient `G ∈ R^{m×n}` and its SVD:

```
G = U S Vᵀ
```

Empirically, `G` for transformer weights is very **low-rank-ish**: a few large singular values dominate. Plain SGD/Adam updates therefore keep pushing the weights along the same few directions, while "rare" directions barely move. Orthogonalization replaces `G` with

```
O = U Vᵀ        (i.e., set all singular values to 1)
```

so every direction in the update gets equal magnitude. Geometrically, `UVᵀ` is the solution to:

```
O = argmin ‖O - G‖_F   s.t.  OᵀO = I
```

Theoretically, this is **steepest descent under the spectral norm** rather than the Frobenius/Euclidean norm — a better-matched geometry for matrices that act as linear maps, since the spectral norm controls how much a layer can stretch activations. This is the same lineage as Shampoo: Muon's update is what you get from Shampoo's preconditioner `(GGᵀ)^{-1/4} G (GᵀG)^{-1/4}` in the no-accumulation limit, which equals `UVᵀ` exactly.

## Newton-Schulz: orthogonalizing without SVD

SVD on every weight matrix every step is too slow. Newton-Schulz is an iterative polynomial method that converges to `UVᵀ` using only matmuls, so it runs in bfloat16 on GPU. The quintic iteration used in Muon/nanochat:

```python
def zeropower_via_newtonschulz5(G, steps=5):
    a, b, c = (3.4445, -4.7750, 2.0315)
    X = G.bfloat16()
    if G.size(-2) > G.size(-1):
        X = X.mT                      # work on the wide orientation
    X = X / (X.norm(dim=(-2, -1), keepdim=True) + 1e-7)  # ensure ||X||_2 <= 1
    for _ in range(steps):
        A = X @ X.mT
        B = b * A + c * A @ A
        X = a * X + B @ X             # X <- aX + b(XXᵀ)X + c(XXᵀ)²X
    if G.size(-2) > G.size(-1):
        X = X.mT
    return X
```

What's happening: each iteration applies an odd polynomial `p(x) = a·x + b·x³ + c·x⁵` to the **singular values** of `X` (the `U`, `V` factors are untouched by polynomials in `XXᵀ` times `X`). The coefficients are tuned so that `p` maps `(0, 1] → ≈1` aggressively — after 5 iterations, all singular values are squashed into roughly `[0.7, 1.2]`. It doesn't converge to exactly 1, and that's fine: you don't need exact orthogonality, just equalized directions. The aggressive coefficients trade precision for speed (fewer iterations), and bf16 is sufficient because the iteration is self-correcting.

Cost: 5 iterations × a few matmuls on `m×n` matrices ≈ **<1% wall-clock overhead** vs AdamW at GPT-2 scale.

## The full Muon step

```python
class Muon(torch.optim.Optimizer):
    def __init__(self, params, lr=0.02, momentum=0.95, nesterov=True, ns_steps=5):
        super().__init__(params, dict(lr=lr, momentum=momentum,
                                      nesterov=nesterov, ns_steps=ns_steps))

    @torch.no_grad()
    def step(self):
        for group in self.param_groups:
            for p in group["params"]:
                g = p.grad
                state = self.state[p]
                if "buf" not in state:
                    state["buf"] = torch.zeros_like(g)
                buf = state["buf"]
                buf.lerp_(g, 1 - group["momentum"])          # momentum EMA
                g = g.lerp_(buf, group["momentum"]) if group["nesterov"] else buf
                g = zeropower_via_newtonschulz5(g, group["ns_steps"])
                # shape-aware scale so update RMS is consistent across matrix shapes
                scale = max(1, p.size(-2) / p.size(-1)) ** 0.5
                p.add_(g, alpha=-group["lr"] * scale)
```

Key details:

1. **Momentum first, then orthogonalize** — orthogonalizing the momentum buffer works much better than momentum-ing orthogonalized gradients.
2. **Shape-aware scaling** `sqrt(max(1, m/n))` — a semi-orthogonal `m×n` update has RMS `≈ 1/sqrt(max(m,n))`; the scale normalizes effective step size across differently-shaped matrices (attention vs MLP), so one LR works for all of them. This is also why Muon's LR (~0.02) looks huge next to AdamW's (~3e-4) — the update is unit-spectral-norm, not raw-gradient-magnitude.
3. **Only 2D hidden matrices.** Embeddings aren't really "linear maps" (they're lookup tables — spectral geometry is the wrong norm), `lm_head` is sensitive to its output scale, and 1D params (norms/biases) can't be orthogonalized. Hence the AdamW/Muon split in nanochat. Conv filters get flattened to 2D if you use them.

## Why it converges faster

- **NanoGPT speedrun**: Muon cut GPT-2 (124M) training to the same val loss by ~35% wall-clock vs tuned AdamW, and it's been the backbone of every speedrun record since.
- **Sample efficiency**: roughly ~2× the compute efficiency of AdamW at small-to-mid scale; Moonshot's Moonlight work showed it holds up at 3B/16B-MoE scale with two fixes — adding weight decay and matching update RMS to Adam's (~0.2) so it slots into existing LR schedules.
- **Memory**: one momentum buffer per param vs Adam's two (no second moment), so optimizer state is halved for the matrices it covers.

Intuition for *why*: equalizing singular values means the optimizer keeps making progress in directions Adam would starve, and the spectral-norm geometry bounds how much any single step can distort a layer's input-output map — you get bigger stable steps.

## Mapping to nanochat specifically

In nanochat you'll see exactly this structure: `Muon` for `transformer.h.*` matrix params (attention QKV/proj, MLP), `AdamW` for `wte`, `lm_head`, and scalar/vector params, with the NS5 iteration above (often `torch.compile`d, and distributed via a ZeRO-style sharded Muon where each rank orthogonalizes a slice of the params and all-gathers).

**References:**

- [Muon: An optimizer for hidden layers in neural networks — Keller Jordan](https://kellerjordan.github.io/posts/muon/)
- [Muon is Scalable for LLM Training (Moonlight, arXiv:2502.16982)](https://arxiv.org/abs/2502.16982)
- [modded-nanogpt speedrun repo (Muon origin)](https://github.com/KellerJordan/modded-nanogpt)
- [nanochat](https://github.com/karpathy/nanochat)
