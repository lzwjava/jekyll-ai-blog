---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diffusion vs Iterative Refinement
translated: false
type: note
---

**Question:** Does "diffusion in Transformers" mean generating an image, then feeding it back in repeatedly to generate again and again?

**Answer:**

Not quite — you're conflating two different things. Let me untangle them.

## Diffusion (the process)

Diffusion models work in **two phases**:

**Forward process (training time):** Take a real image, add Gaussian noise step by step over T steps until it's pure noise. This is fixed/analytical — no network needed.

**Reverse process (inference time):** Start from pure noise, and iteratively *denoise* it — each step predicts and removes a small amount of noise.

```
x_T (pure noise) → x_{T-1} → x_{T-2} → ... → x_0 (clean image)
```

So yes, you're running the model ~50-1000 times, but **each step is denoising, not regenerating from scratch**. The model predicts the noise component ε at each step, not the final image directly.

The core formula (DDPM):

```
x_{t-1} = 1/√α_t * (x_t - (1-α_t)/√(1-ᾱ_t) * ε_θ(x_t, t)) + σ_t * z
```

where `ε_θ` is the neural network (U-Net or Transformer).

---

## Where Transformers fit in

**DiT (Diffusion Transformer, Peebles & Xie 2022)** replaces the U-Net backbone with a Transformer. The architecture:

1. Patchify the noisy latent `x_t` into tokens
2. Condition on timestep `t` and class label via **adaLN** (adaptive layer norm)
3. Run standard Transformer blocks (self-attention + FFN)
4. Unpatchify back to latent shape

```python
# DiT forward pass sketch
def forward(self, x, t, y):
    x = self.patchify(x)           # [B, N, D]
    x = x + self.pos_embed         # positional encoding
    c = self.adaln_embed(t, y)     # timestep + class conditioning
    for block in self.blocks:
        x = block(x, c)            # transformer + adaLN
    x = self.unpatchify(x)         # predict noise ε
    return x
```

This is used in **Stable Diffusion 3**, **FLUX**, **Sora** — all replaced U-Net with DiT.

---

## The actual loop at inference

```python
x = torch.randn(latent_shape)   # start from noise

for t in reversed(range(T)):    # e.g. T=50 with DDIM
    eps = model(x, t, conditioning)   # transformer predicts noise
    x = denoise_step(x, eps, t)       # scheduler removes that noise

image = vae.decode(x)           # decode latent to pixel space
```

Each iteration: same model, different `t`, progressively cleaner `x`. It's not "generate image → use image as prompt" — it's "denoise latent → denoise again."

---

## What you might be thinking of (iterative refinement)

There *are* models that do something closer to your description:

- **Consistency Models** — distill diffusion into fewer steps, can do 1-shot
- **Flow Matching** (used in SD3, FLUX) — straight trajectories instead of diffusion
- **Autoregressive image models** (like LlamaGen, VAR) — predict image tokens sequentially, more like language modeling

VAR (Visual AutoRegressive) is especially interesting — generates at coarse resolution first, then refines at finer scales. That's closer to "generate image → use it to generate again."

---

## TL;DR

| Concept | What actually happens |
|---|---|
| Diffusion | Iterative **denoising** of noise → image |
| DiT | Transformer as the denoising backbone |
| Your description | Closer to iterative refinement / VAR |

The Transformer in DiT isn't doing anything architecturally special for diffusion — it's just a better backbone than U-Net for the same denoising job, because self-attention captures long-range spatial dependencies that convolutional U-Nets struggle with at scale.

**References:**

- [DiT paper — Scalable Diffusion Models with Transformers](https://arxiv.org/abs/2212.09748)
- [DDPM — Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)
- [VAR — Visual AutoRegressive Modeling](https://arxiv.org/abs/2404.02905)
