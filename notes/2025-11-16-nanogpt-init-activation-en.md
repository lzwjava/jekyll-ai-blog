---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: NanoGPT Initialization and Activation Details
translated: false
type: note
---

In Andrej Karpathy's **NanoGPT** (the popular minimal GPT implementation from late 2022 to 2025), the model does **not** use ReLU. It uses **GELU** (Gaussian Error Linear Unit) as the activation function, which is the standard choice in modern GPT-style models (same as GPT-2, GPT-3, Llama, etc.).

### Key parameter initialization ranges in NanoGPT (as of the latest 2025 version)

| Parameter / Component          | Initialization method                          | Typical scale / range                               | Notes |
|--------------------------------|------------------------------------------------|-----------------------------------------------------|-------|
| Embedding layer (token + position) | `nn.Embedding` → normal distribution         | std = 0.02                                          | Very small to keep initial logits small |
| Linear layers in FFN (proj)    | `nn.Linear` → default PyTorch init → then scaled | weight: std ≈ 0.02–0.03 after scaling               | Karpathy applies a scaling factor of `0.02 / sqrt(n_embd)` or similar in some configs |
| Final LM head (output projection) | Same as embeddings (weight tied)             | std = 0.02                                          | Tied with token embedding |
| LayerNorm bias                  | Zeros                                          | 0                                                   | Standard |
| LayerNorm weight                | Ones                                           | 1.0                                                 | Standard |
| Residual scaling (post-init)    | Weights multiplied by a small factor           | Often `weight *= 0.02` or `weight *= sqrt(2/n_layers)` | Crucial trick to stabilize training at init |
| Attention QKV projection        | Scaled as above                                | Effective std ≈ 0.02                                | Same scaling as other linears |
| Attention output projection    | Extra scaling: `cproj.weight *= 0.02` or similar | Even smaller (to compensate for residual path)     | Very important for deep models |

### Special initialization trick in NanoGPT
In `model.py`, after creating each `nn.Linear` layer, Karpathy does something like this (exact values depend on config):

```python
if isinstance(m, nn.Linear):
    torch.nn.init.normal_(m.weight, mean=0.0, std=0.02)
    if m.bias is not None:
        torch.nn.init.zeros_(m.bias)
    # Important residual scaling for deeper networks
    if "cproj" in name:          # output projection of attention or FFN
        m.weight.data *= 0.02    # or sometimes *= 1/sqrt(n_layer)
```

Or in the more recent versions (2024–2025), he uses a config-driven scaling:

```python
std = 0.02 / math.sqrt(2 * n_layer)   # helps with deeper models
```

This ensures the residual stream variance doesn’t explode or vanish as depth increases.

### Summary: NanoGPT does NOT use ReLU
- Activation: **GELU** (not ReLU)
- Main initialization std: **~0.02**
- Extra scaling on output projections: **0.02 or smaller** (especially important)
- No bias in most linear layers except LayerNorm

This very small initialization + residual scaling is why NanoGPT trains stably even without learning rate warm-up in the smallest configs.

If you're training your own NanoGPT from scratch, copy these exact init tricks — they matter a lot more than people think!
