---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Itorch 0.2.0: Sophisticated Update"
translated: false
type: note
---

Done — **itorch 0.2.0**, all three suites green. Here's what "more sophisticated" bought:

## What's new

**Engine** (`tensor.py`)

- `backward(retain_graph=True)` — frees the graph after the pass; a second `backward()` on a freed graph raises `RuntimeError` (torch-like), while leaf tensors remain reusable in new graphs
- `y.grad_fn` → `"matmul((3,4),(4,5)) -> (3,5)"` for debugging
- `no_grad` now doubles as a decorator (`@no_grad`)
- `gelu` op + `Tensor.__array__` so numpy interops cleanly (found two real shadowing bugs along the way: `Module.__call__` mis-slicing multi-arg forwards, and builtin-`sum` collisions with the functional API)

**Layers** (`nn.py`)

- Normalizations: `LayerNorm`, `GroupNorm`, `AvgPool2d` (plus existing BatchNorms)
- Recurrent: `LSTM` and `GRU` (batch-first, return `(outputs, state)`), unrolled straight through the autograd graph
- Attention: `MultiHeadAttention`, `TransformerBlock` (pre-norm + residuals), `Transformer` (causal stack), `causal_mask`, `GELU`
- `Module.freeze()/unfreeze()` (fixed the circular "frozen params invisible to unfreeze" trap), `nn.Sequential` etc.

**Training**

- `schedulers/`: `StepLR`, `MultiStepLR`, `CosineAnnealingLR`, `ReduceLROnPlateau`
- Losses: `l1`, `huber`, `nll_loss`; `cross_entropy` refactored on top of `nll_loss`
- `count_parameters`, `DataLoader(drop_last=...)`

**Showpiece**: `examples/04_tiny_gpt.py` — a ~40k-param char-level GPT (token+positional embeddings → 2 causal transformer blocks → LM head) trained in seconds:

```
step   20  loss=2.37  →  step 400  loss=0.13
"to be or not tr be, thanoure is the questististion..."  ← Shakespeare-sounding
```

## Verification

- `tests/test_sophisticated.py` (new): gradients of gelu/norms/pools/GRU/LSTM/attention/transformer/losses all checked against central finite differences; scheduler LR curves, retain-graph semantics, freeze/unfreeze, and a tiny-transformer training loop asserted
- All previous suites still pass — no regressions

Want me to commit and push this as v0.2.0?
