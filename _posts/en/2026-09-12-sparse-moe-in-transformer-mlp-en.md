---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sparse MoE in Transformer MLP
translated: false
type: note
---

Here's a guided tour of the MoE code in `train.py`. The idea: **a Mixtral/Switch-style sparse MoE that swaps in for the MLP inside every transformer block.**

## 1. Where it plugs in

In `Block.__init__` (line ~354):

```python
if config.use_moe:
    self.moe = MoE(config)
else:
    self.mlp = MLP(config)
```

So attention is untouched; only the feed-forward half of each block becomes "N experts + a router". `--moe` flips this on. Knobs (lines 227–232, 524–527):

| arg | meaning |
|---|---|
| `n_experts` | how many expert FFNs per block |
| `n_experts_active` | top-k experts each token is sent to |
| `moe_expert_dim` | expert hidden size = `moe_expert_dim * n_embd` (4 = same as dense MLP) |
| `moe_aux_loss_coef` | weight on the load-balancing loss |

## 2. One expert = one small MLP

`Expert` (line 290) is just the dense `MLP` again, with a configurable hidden size:

```python
x -> Linear(C -> dim*C) -> GELU -> Linear(dim*C -> C)
```

## 3. The router + dispatch (`MoE.forward`, line 323)

Shapes with `N = B*T` tokens, `C = n_embd`, `E = n_experts`, `k = n_experts_active`:

```python
flat = x.view(-1, C)                          # (N, C)  flatten batch+time
router_logits = self.gate(flat)              # (N, E)  a plain Linear, no bias
topk_logits, topk_idx = torch.topk(router_logits, k, dim=-1)   # (N, k)
weights = F.softmax(topk_logits, dim=-1)     # (N, k)  renormalized over the k chosen
```

Note it softmaxes **over only the top-k logits** (Mixtral behavior), not the full E-way softmax then gather (GShard). That's why gradients only flow to the chosen experts' routing weights.

Then the dispatch loop (lines 331–341) avoids a dense `N x E` matmul by gathering tokens per expert:

```python
flat_idx  = topk_idx.reshape(-1)                                  # (N*k,) which expert each slot wants
flat_w    = weights.reshape(-1, 1)                                # (N*k, 1) gate weight per slot
token_idx = arange(N).repeat_interleave(k)                        # (N*k,) which token each slot belongs to
for e, expert in enumerate(self.experts):
    mask  = flat_idx == e                                         # slots routed to expert e
    slot  = mask.nonzero(...)
    out   = expert(flat[token_idx[slot]])                         # run expert only on those tokens
    y = y.index_add(0, token_idx[slot], out * flat_w[slot])       # weighted scatter back
```

`token_idx` is the key mapping: slot `s = token*k + j` belongs to token `token_idx[s]` and used the `j`-th of that token's top-k choices. `index_add` accumulates the k contributions into each token's output row. Every token is processed — there is **no capacity limit / token dropping** here, unlike full Switch Transformer.

## 4. Auxiliary load-balancing loss (lines 343–349)

Without a nudge, the router collapses onto a few experts. The Switch-Transformer loss is `L_aux = E * Σᵢ fᵢ · Pᵢ`:

```python
router_probs = F.softmax(router_logits, dim=-1)                        # full (N, E) softmax
gathered   = torch.gather(router_probs, 1, topk_idx)                   # (N, k) prob of chosen
one_hot    = F.one_hot(flat_idx, E)                                    # (N*k, E)
density    = one_hot.mean(0)                                           # f_i: fraction of slots -> expert i
mean_prob  = (one_hot * gathered.reshape(-1,1)).sum(0) / N             # P_i: avg router prob for i
self.aux_loss = E * (density * mean_prob).sum()
```

- `f_i` (density) = share of the `N*k` slots dispatched to expert i.
- `P_i` (mean_prob) = mean routing probability mass expert i receives.
- The sum is minimized when both are uniform (`f_i = 1/E`, giving `E * Σ (1/E)(1/E) = 1/E`), maximized when one expert takes everything. So it pushes toward balanced routing. It's differentiable through `router_probs`/`gathered`, training the gate.

## 5. Wiring back into the model

`GPT.forward` (lines 445–459) accumulates aux loss across blocks and adds it to the LM loss:

```python
aux_loss = x.new_zeros(())
for block in ...:
    x = block(x)
    if block has moe: aux_loss += block.moe.aux_loss
...
loss = F.cross_entropy(logits, targets) + config.moe_aux_loss_coef * aux_loss
```

`get_aux_loss()` (line 422) just detaches and sums the per-block values for logging — you'll see it in the log line at line 845 as `aux X.XXXX`.

## 6. Parameter accounting

`get_num_params_active()` (line 408) reports the "activated" parameter count for the MFU/flops intuition:

```python
expert_params = sum(params of all experts)
frac_active = k / E
n -= expert_params * (1 - frac_active)
```

i.e. total params stay large, but each token only touches `k/E` of the expert weights plus all the shared weights. Both totals are printed at model construction.

## How to read it as a whole

1. `Expert` = a swappable MLP.
2. `gate` = linear router producing `E` logits per token.
3. top-k + softmax picks and weights `k` experts per token (Mixtral routing).
4. Per-expert gather → expert → weighted `index_add` scatter (sparse compute, dense output).
5. Aux loss keeps the router from collapsing.
6. `Block`/`GPT` thread the aux loss into the total loss and expose active-param stats.

Things to keep in mind when experimenting:
- No capacity factor / dropping, so memory/throughput scales with how skewed the routing is (a very imbalanced router still runs all tokens, just unevenly per expert).
- `self.aux_loss = torch.zeros(())` in `__init__` is CPU/float32 but always overwritten in `forward`, so it's fine; it only matters if you call `get_aux_loss()` before any forward.
- The aux-loss `density` is computed over slots (`N*k`), so with `k>1` a token counts once per chosen expert — consistent with the slot-based `P_i` normalization here, but not identical in scale to the original top-1 formulation.
- `moe_expert_dim` controls expert size; with `n_experts=k` (all active) MoE degenerates to a wider dense MLP.

Want me to add a tiny runnable example or a shape-trace printout so you can see the routing live?
