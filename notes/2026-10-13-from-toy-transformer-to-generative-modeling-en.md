---
audio: false
generated: true
image: false
lang: en
layout: post
title: From Toy Transformer to Generative Modeling
translated: false
type: note
---

All green. **Round 3 → itorch 0.3.0** — this round took it from "transformer/RNN toy" to "generative modeling":

## What's new

**Engine**
- **`col2im`** op — the exact autograd transpose of `im2col` (overlap-add fold, backward = unfold of the gradient). This unlocks transposed convolutions without any new math.
- `sin`, `cos`, `silu` (Swish), `softplus`, `zeros_like/ones_like/randn_like/rand_like` (reparameterization trick), torch-style method aliases (`x.mul(y)`, `.add`, `.div`, ...)
- `tt.grad(outputs, inputs)` — direct gradient API
- numerically stable `sigmoid` (was overflowing to NaN on extreme logits — caught by the VAE)

**Layers**
- `nn.ConvTranspose2d` — built on `col2im`; verified by a **conjugate/adjoint identity** test (`sum(y·conv(x,w)) == sum(convT(y,w)·x)`) plus finite-difference gradchecks
- `nn.init` (`kaiming_*`, `xavier_*`, `normal_/uniform_`, `zeros_/ones_`)
- Class-based losses: `nn.MSELoss`, `nn.L1Loss`, `nn.HuberLoss`, `nn.BCELoss`, `nn.BCEWithLogitsLoss`, `nn.CrossEntropyLoss`, `nn.NLLLoss`

**Optimizers** — 4 more: `Adagrad`, `RMSprop`, `Adamax`, `Lion` (all verified to converge on a 1-D quadratic + decrease a regression loss)

**Showpiece: `examples/05_vae_mnist.py`** — a convolutional VAE (~219k params) using Conv2d/ConvTranspose2d, SiLU, the reparameterization trick, `CosineAnnealingLR`, and a 10×10 generated digit grid. In development I hit textbook **posterior collapse** (`μ→0`, `var→1` — the encoder gave up) and fixed it with **free-bits KL**, which took latent samples from 1/100 healthy digits → **284/300 healthy digits**:

```
epoch 1/2  recon=0.2205  kl=0.0019
epoch 2/2  recon=0.2107  kl=0.0018   → writes examples/grid_vae.png
```

## Verification
- `tests/test_round3.py` (new, ~200 lines): gradchecks for sin/cos/silu/softplus/col2im-round-trip/ConvTranspose2d, the adjoint identity, optimizer convergence, loss-class ↔ functional parity, init correctness, `autograd.grad`, and a VAE training smoke test
- All 4 suites pass; total ~3,175 lines of Python

Ready to commit as v0.3.0?
