---
audio: false
generated: true
image: false
lang: en
layout: post
title: Per-Head Gated Value Embedding
translated: false
type: note
---

These two lines live in `CausalSelfAttention.__init__` (gpt.py:80-82) and implement the **gate for the "value embedding" (VE) mechanism** — a ResFormer-style value residual where a per-token lookup is injected into the V-pathway of attention. Here's what each does:

## `self.ve_gate_channels = 12`

A hardcoded hyperparameter: the gate reads only the **first 12 channels** of the residual stream instead of the full `n_embd=768`. This keeps the gate network tiny (a "cheap scalar-ish probe" of the hidden state, similar in spirit to the `smear_gate` on line 183 which reads `:24`).

## `self.ve_gate = Linear(12, n_kv_head, bias=False) if has_ve(...) else None`

A small linear layer mapping those 12 channels → `n_kv_head` scalars, one **gate value per KV head**. The conditional exists because the model doesn't use VE in every layer:

```python
def has_ve(layer_idx, n_layer):            # gpt.py:53
    return layer_idx % 2 == (n_layer - 1) % 2
```

This selects **alternating layers of the same parity as the last layer** — the last layer always gets VE, others are interleaved. Layers without VE have no gate module at all (`None` → no parameters, no compute), keeping the network lean.

## How it's used in `forward` (gpt.py:93-98)

```python
# ve: (B, T, n_kv_head * head_dim) from value_embeds[str(layer)](token_ids)
if ve is not None:
    ve = ve.view(B, T, self.n_kv_head, self.head_dim)          # one embedding per KV head
    gate = 3 * torch.sigmoid(self.ve_gate(x[..., :12]))        # (B, T, n_kv_head), range (0, 3)
    v = v + gate.unsqueeze(-1) * ve                            # gate is per-head, applied to all head_dim
```

So the pipeline is:

1. **Value embedding lookup**: `self.value_embeds[str(i)]` is an `nn.Embedding(vocab_size → kv_dim)` that maps the raw token id to a vector of the same shape as the V-stream projection (gpt.py:501, 192).
2. **Input-dependent gate**: the hidden state `x` (token, first 12 channels) is squashed through the gate linear + sigmoid, scaled ×3 to land in `(0, 3)`. Each KV head gets its own multiplier — the network learns *when/how much* to inject the token's value-embedding per head.
3. **Mix into V**: `v = v + gate * ve` adds the gated value-embedding to the projected values right before flash attention, so it participates in the attention output.

The gate is what makes VE *input-dependent*: rather than always adding a fixed per-token embedding to V (as in the original ResFormer), the model decides per position and per head how strongly to inject it. The `bias=False` + `Linear` subclass matches the rest of the model (weights stay fp32 for the optimizer but are cast to activation dtype at matmul time), and init at gpt.py:254-255 seeds the weights `uniform_(0.0, 0.02)` so the gate starts near its neutral operating point and learns from there.
