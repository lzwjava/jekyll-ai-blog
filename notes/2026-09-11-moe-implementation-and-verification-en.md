---
audio: false
generated: true
image: false
lang: en
layout: post
title: MoE Implementation and Verification
translated: false
type: note
---

Done — MoE is implemented and verified end-to-end (train → checkpoint → resume/sample).

## What was added to `train.py`

**`MoE` + `Expert` modules** (after `MLP`):
- **Router**: a linear gate produces `n_experts` logits per token; each token is routed to its **top-k** experts with softmax weights over the selected logits (GShard/Mixtral style).
- **Dispatch**: tokens are grouped per expert, each expert (an `Expert` MLP with the same `c_fc`/`c_proj` shape as the dense MLP, so the GPT-2 scaled `c_proj` init still applies) runs only on its assigned tokens, and outputs are combined with `index_add` — no wasted compute on non-selected experts.
- **Load balancing**: Switch-Transformer aux loss `E · Σᵢ fᵢ·Pᵢ` computed from assignment density vs. mean router probability, so the router is incentivized to use all experts evenly.

**`Block`**: uses `MoE` instead of `MLP` when `config.use_moe` is set.

**`GPT`**:
- `forward` sums the per-block aux losses and adds `moe_aux_loss_coef * aux` to the cross-entropy loss (so it flows through DDP/grad accumulation correctly).
- `get_num_params_active()` reports the parameters actually touched per token (only top-k experts active).
- `get_aux_loss()` exposes the last aux loss for logging.

**CLI** (checkpoint config round-trips automatically via `asdict`, and old dense checkpoints still resume since new fields default off):
- `--moe`, `--n_experts 8`, `--n_experts_active 2`, `--moe_expert_dim 4`, `--moe_aux_loss_coef 0.01`

## Verification

```
use_moe=False: loss=4.1965 params=104,256   active=104,256
use_moe=True:  loss=4.2058 aux=1.3167 params=303,296 active=170,944  (top-2/4)
```

Real run (`--moe` on tiny shakespeare, CPU):
```
model: 31.95M parameters
model: MoE top-2/4, 17.77M active parameters per token
iter 8: loss 3.5274 | aux 1.8717 | ...
```
All parameters receive gradients, generation works, and the per-iter log now includes the aux loss (should hover near `k` ≈ n_experts_active per layer when routing is balanced; if it climbs, experts are collapsing).

Usage: `python train.py --moe --n_experts 8 --n_experts_active 2`
