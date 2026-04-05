---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diffusion Models and Image Plausibility
translated: false
type: note
---

Question: Is it correct to say that diffusion models are primarily optimizing for image plausibility — and that because the conditional distribution in natural images is inherently one-to-many (a single prompt can correspond to many valid images), as long as the model lands on the high-probability visual manifold, the output will look good?

Answer:

Your intuition is **largely correct**, but there are important nuances worth unpacking carefully.

---

## The Core Claim: Mostly Right

Yes — diffusion models are fundamentally in the business of learning and sampling from a **data distribution**, specifically the distribution of natural-looking images. Abstractly, the idea of a diffusion model is to take an unknown probability distribution (the distribution of natural-looking images), then progressively convert it to a known distribution (a standard Gaussian), by building a continuous probability path connecting them.

So in a very real sense, "looking good" = "being on the high-probability manifold of natural images." We deem a diffusion model good if the field it implements nudges images toward the manifold of meaningful images; a bad model simply specifies currents that don't systematically lead toward that manifold.

---

## The One-to-Many Nature of Conditional Distributions: Correct

Your point about the conditional distribution being multi-modal is well-grounded. A text prompt like "a dog in a park" does not specify a unique image — it specifies a **distribution** over millions of valid images. Conditional image generation is essentially "translating from a textual language into a pictorial language" — we sample not from the whole distribution of images, but from a conditional distribution given the description.

This means:
- The conditional distribution `p(image | prompt)` is legitimately **multi-modal and high-dimensional**.
- Any sample from this distribution that looks plausible to a human is, by definition, a valid output.
- The model doesn't need to produce *the* correct image; it needs to produce *an* image that sits on the plausible visual manifold.

According to the manifold hypothesis, most real data concentrates on a low-dimensional manifold, even though the observed data appears arbitrarily high-dimensional. Diffusion models explicitly exploit this structure — the score function guides the denoising trajectory toward this manifold.

---

## What "Optimizing Image Plausibility" Actually Means Technically

Diffusion models learn a data distribution by gradually removing noise from a normally distributed variable. A special perceptual loss function ensures that reconstructions remain confined within the image manifold, reducing blurriness that would otherwise appear with pixel-space losses like L1/L2.

The autoencoder in latent diffusion models is trained using a combination of a perceptual loss and an adversarial patch-based loss, encouraging reconstructions to remain on the natural image manifold.

So there are actually **two layers** of "staying on the manifold":
1. The **autoencoder** is trained to reconstruct only manifold-valid images.
2. The **diffusion process** is trained to denoise toward the data distribution, not arbitrary pixel arrangements.

---

## Important Nuances: Where Your Statement Needs Qualification

Your claim is correct at a high level, but here are three places where it's incomplete:

### 1. "Looking good" ≠ "Faithfully following the prompt"
Falling on the high-probability visual manifold means the image looks photorealistic and natural — but it doesn't guarantee **semantic alignment** with the prompt. A model can produce a beautiful, realistic image that completely misses the instruction. This is why techniques like **classifier-free guidance (CFG)** exist: they push the model toward the *intersection* of the image manifold **and** the condition-specific region.

### 2. The manifold is not perfectly captured — mode coverage vs. quality tradeoff
Diffusion models can sometimes exhibit **mode dropping** or **mode imbalance**, similar to GANs. Certain high-probability regions of the visual manifold may be overrepresented. Guidance strength (CFG scale) trades off between diversity (covering more of the manifold) and fidelity (staying close to the prompt condition).

### 3. High-probability ≠ high-quality in edge cases
A diffusion model trained on irrelevant or poor-quality data can hinder rather than help generation, or worse, lead to high-quality-looking reconstructions that are inconsistent with reality — so-called hallucinations. The manifold the model learns is only as good as its training data.

---

## Summary

| Your Claim | Verdict |
|---|---|
| Diffusion models optimize image plausibility | ✅ Correct — they learn `p(image)` or `p(image \| condition)` |
| Conditional distributions are one-to-many | ✅ Correct — same prompt → many valid images |
| Landing on the visual manifold → looks good | ✅ Correct in the perceptual sense |
| That's all the model needs to do | ⚠️ Partially — also needs semantic alignment with the condition, not just manifold membership |

So your framing is a solid and accurate intuition for understanding why diffusion models produce such high-quality outputs without needing to solve any single "correct" image reconstruction problem.

References:

- [Diffusion model - Wikipedia](https://en.wikipedia.org/wiki/Diffusion_model)
- [What are Diffusion Models? | Lil'Log](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)
- [Stable Diffusion Models - Towards Data Science](https://towardsdatascience.com/what-are-stable-diffusion-models-and-why-are-they-a-step-forward-for-image-generation-aa1182801d46/)
- [Latent Diffusion Model - Medium](https://medium.com/@kdk199604/latent-diffusion-model-efficient-high-resolution-image-synthesis-without-compromise-1bec1bee5f8b)
- [Diffusion Models for Medical Image Reconstruction - Oxford BJR](https://academic.oup.com/bjrai/article/1/1/ubae013/7745314)