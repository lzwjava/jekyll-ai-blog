---
audio: false
generated: true
image: false
lang: en
layout: post
title: Itorch Status and Next Steps
translated: false
type: note
---

Good moment to take stock. Here's where itorch stands and what I'd do next:

## Where we are
- **Engine**: full autograd (25+ ops, im2col/col2im, broadcasting, slicing, gather), `grad_fn`, `retain_graph`, `tt.grad`
- **Layers**: CNN / Transformer / RNN / VAE toolkits all verified by finite-difference gradchecks
- **7 optimizers + 4 schedulers**, losses, DataLoader, `nn.init`, save/load
- **4 test suites, 5 examples** (98.3% MNIST CNN, char-GPT, digit-generating VAE)

## What's genuinely missing — prioritized

**1. Performance (biggest gap). Eager autograd rebuilds op metadata every step.**
- `@tt.jit` — tinygrad-style: trace a forward pass once, cache the op plan, reuse it every iteration with new leaf data. Easy 2–5× on training loops.
- `tt.profile(ops=True)` — per-op timing in backward.

**2. Autograd completeness (unlocks real SOTA model ports).**
- `einsum` op (one op = batched matmul/attention/contractions, with proper gradients),
- `scatter`/`index_put_`/`masked_fill`/`repeat`/`tile` (+ `nn.Parameter` for torch parity).

**3. Adversarial training proof (it's the last big training regime untested).**
- **DCGAN on MNIST** — generator built on the existing `ConvTranspose2d`, BCE + actual min-max optimization, sampling grid. If GANs train, the engine is really general.

**4. Portrait + DX.**
- `tt.autograd.gradcheck()` exported so users can validate custom layers,
- CIFAR-10 loader + augmentation example with `ReduceLROnPlateau`,
- `nn.Parameter`, model FLOP counter.

## My recommendation
Do **1 + 3 + gradcheck** next (`@tt.jit` + DCGAN + the utility) — it's the highest-leverage combo: performance, a new training paradigm, and a user-facing debug tool. Then **2** (einsum/scatter) for completeness.

Want me to go with that?
