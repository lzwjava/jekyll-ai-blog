---
audio: false
generated: true
image: false
lang: en
layout: post
title: VAE and Stable Diffusion Overview
translated: false
type: note
---

Question: How does a VAE (Variational Autoencoder) work, and how is it used in Stable Diffusion?

---

Answer:

## What is a VAE?

A **Variational Autoencoder** is a generative neural network with two parts — an **Encoder** and a **Decoder** — but with a key twist over regular autoencoders: instead of mapping input to a single point, it maps to a **probability distribution** in latent space.

---

## Core Architecture

Question: How does a VAE (Variational Autoencoder) work, and how is it used in Stable Diffusion?

---

Answer:

---

## How VAE Works — Step by Step

**1. Encoder → Distribution (not a point)**
A regular autoencoder maps input → single latent vector. A VAE maps input → a **Gaussian distribution** in latent space, outputting two vectors: **μ** (mean) and **σ** (standard deviation). This is the core difference.

**2. Reparameterization Trick**
To sample a point `z` from that distribution while keeping the computation differentiable:

```
z = μ + σ · ε,   where  ε ~ N(0, 1)
```

The randomness lives in `ε`, so gradients can flow cleanly back through `μ` and `σ` during backpropagation.

**3. Decoder → Reconstruction**
The sampled `z` is passed through the decoder, which reconstructs the original input as `x̂`.

**4. Two Loss Terms**

- **① KL Divergence** — regularizes the latent space so distributions don't drift far from `N(0, I)`. This makes the latent space smooth and continuous, enabling meaningful interpolation.
- **② Reconstruction Loss** — penalizes pixel-level difference between `x` and `x̂` (usually MSE or perceptual loss).
- **Total**: `L = Recon loss + β · KL`

---

## In Stable Diffusion (Latent Diffusion Model)

SD uses a VAE as a **compression wrapper** around the diffusion process. Why? Running diffusion directly on 512×512×3 = 786K pixels is expensive. The VAE squashes it to 64×64×4 = 16K values (~48× cheaper), so the U-Net denoiser trains and runs entirely in that compressed latent space.

| Component | Role |
| --- | --- |
| **VAE Encoder** (frozen) | Compresses pixel images → 64×64×4 latents (used in img2img) |
| **Diffusion U-Net** | Denoises latents step-by-step, guided by text via cross-attention |
| **VAE Decoder** (frozen) | Upsamples 64×64×4 clean latent → 512×512×3 pixel image |

The VAE in SD is **pre-trained** on a large image dataset and then **frozen** — only the U-Net learns to denoise in that fixed latent space.

> Click any box in the diagram to dive deeper into that component.

---

References:

- [Auto-Encoding Variational Bayes (Kingma & Welling, 2013)](https://arxiv.org/abs/1312.6114)
- [High-Resolution Image Synthesis with Latent Diffusion Models (Rombach et al., 2022)](https://arxiv.org/abs/2112.10752)
