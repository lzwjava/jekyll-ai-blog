---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Weight Decay in GPT Model Training
translated: false
type: note
---

Weight decay is a common regularization technique used when training GPT models (and almost all large language models) to prevent overfitting and improve generalization.

### What it actually does
Weight decay adds a penalty term to the loss function that pushes the model’s weights toward smaller values. Mathematically, if your original loss is ℒ (e.g., cross-entropy), with weight decay you optimize:

ℒ_total = ℒ + (λ / 2) × ||w||²

where:
- w are the model parameters (weights)
- ||w||² is the squared L2 norm of the weights
- λ (lambda) is the weight decay coefficient (typically 0.01 ~ 0.1 in GPT-style training)

This extra term discourages the model from learning very large weights unless they significantly reduce the original loss.

### How it’s implemented in practice (AdamW)
In most GPT training runs (OpenAI’s GPT-2, GPT-3, LLaMA, Mistral, etc.), people do NOT use plain Adam with standard L2 regularization. Instead they use AdamW (Adam with decoupled weight decay).

The key difference:
- Standard L2 regularization in Adam adds the penalty directly into the gradient.
- AdamW decouples it: it applies the weight decay as a separate update step, which works much better with adaptive optimizers like Adam.

So when you see something like this in training configs:

```python
optimizer = AdamW(model.parameters(), lr=5e-5, weight_decay=0.1)
```

That 0.1 is the λ above, and it’s using the correct decoupled version.

### Typical values in real GPT-style models

| Model / Paper        | Weight Decay | Notes                                   |
|----------------------|--------------|-----------------------------------------|
| GPT-2 (OpenAI)       | 0.01         |                                         |
| GPT-3 (OpenAI)       | 0.1          | Brown et al. 2020                       |
| LLaMA 1 & 2 (Meta)   | 0.1          | Often combined with no decay on norms/biases |
| PaLM (Google)        | 0.1          |                                         |
| Grok-1 (xAI)         | 0.1          | From the open-release config            |
| Mistral / Mixtral    | 0.1          |                                         |

### Important nuance: which parameters get weight decay?
Modern practice (since LLaMA) is to apply weight decay only to certain layers:
- Yes: Linear layers (weight matrices), embedding matrix
- No: Bias terms, LayerNorm weights, any 1D parameters

This is usually done with PyTorch parameter groups:

```python
decay = set()
no_decay = set()
for name, param in model.named_parameters():
    if "bias" in name or "layer_norm" in name or param.ndim == 1:
        no_decay.add(param)
    else:
        decay.add(param)

optimizer = AdamW([
    {"params": list(decay),   "weight_decay": 0.1},
    {"params": list(no_decay), "weight_decay": 0.0}
], lr=...)
```

### Why it matters for GPT-scale models
At billions or hundreds of billions of parameters, models can easily memorize training data. Weight decay is one of the simplest and most effective tools (along with dropout, stochastic depth, etc.) to keep the effective capacity in check and improve downstream performance.

In short: weight decay ≈ L2 regularization, but properly implemented via AdamW and selectively applied, is a standard ingredient in virtually all modern GPT-style pretraining recipes.
