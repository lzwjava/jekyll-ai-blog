---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stability AI Image Models Intro
translated: false
type: note
---

Question: Intro to Stability AI image models

Answer:

![Image](https://images.openai.com/static-rsc-4/tQ-e95Wvn-WA5b4l91HYdrn_blXKteFffX7HGDkn00jJRb5eAWoS6AllKK2256hmyGX3-ASq2pJER6DwsXbfAZYHjxuCjG7oX_ZmpiPO4WKbc_YayIeX1fKqW3S_51B0a2oru5f0oHPNtRF9xVBvzv_wdKBvcVjKQZxtNELMuzndkZf94SH492TEg-usdcF3?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pDNn1-0rRuClKspbkb0_12iqyVgFJPXjmzNp_0e7vodSKnAVIrQovmvK2gQk-vPlRhhzv3i03I816dn-7Dpd7O1WAHiXf_A-4nmHHJslXQCFIN9bMpn5W_pog1MObWUymWNk0k53iVxs8Lc9cOaWma0JliWKlj-rm3L3XHSimDITPRZBnIvUUEHA0EakhwYr?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/DSuXA7xXXlXiYahmYRyH0VJjC47wBXFJojPYOrt7MyL1yDlv__8jsf15xmOXVPiFv2iIJmo_X_aYx0IflmsU4ipGDaorIg5hGro12YRqKlrooxEpEb6hhtEcyfTKKxkbRKr3ctbh4JExldZVhYR66Ka10WeTc5HZ63N47UuFpXEh6F-zQ9ZjNqU8JkSRb2Ut?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Dzp2HlIHgUnOF9bwYH4yFve0ExE_Kx9LOQUwNPvzCtomjWI_YjHxIqsUmH3gQ7519I9P-rZxgijDXHudIDT9aey5CrESxoCrV0QYBNm692156TZ-qhs4vu7U7R7NiPzZ1BKTDdMGhS60okaugXL8BvGEgXtgd1qIBxTbX_BMmGbSmF8Zqf_UvmYVQm0_3l60?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/uOevt2wXn6acXlqWDYoYXnzJN37riFWAnJFgx6JIG2ydfHGd1ijaAF6oIqghwKMRFVi1rro05MRf5B63TChK3uItJ66JeA3b0LH220fhnYtFdYzme8jXhfCOCD65jWuMBxtu0So0CxgpbaokH-m9YS6HXWYTlMpoq2mRCZ8RKOeWeQMcROsMMIScxX63IRXo?purpose=fullsize)

**Stability AI** is one of the most influential companies in open generative image models. Their flagship technology is **Stable Diffusion**, which made high-quality text-to-image generation available to researchers, developers, and local users.

The key idea:

> Instead of generating pixels directly, Stable Diffusion learns to remove noise from a compressed image representation.

Mathematically:

```
random noise z_T
      |
      v
 U-Net / DiT denoiser
      |
      v
clean latent image z_0
      |
      v
VAE decoder
      |
      v
RGB image
```

---

## 1. History

### Before Stable Diffusion

Early image generation:

* GANs (2014-2020)

  * StyleGAN
  * BigGAN

Problems:

* difficult training
* limited control
* mode collapse

Then diffusion models appeared.

Important papers:

* Denoising Diffusion Probabilistic Models
* High-Resolution Image Synthesis with Latent Diffusion Models

Latent diffusion was the breakthrough.

---

## 2. Stable Diffusion (2022)

The original model:

Stability AI released:

* Stable Diffusion 1.0
* Stable Diffusion 1.5

Architecture:

```
Text prompt
    |
CLIP text encoder
    |
text embedding
    |
    v
+----------------+
| U-Net          |
| diffusion      |
| model          |
+----------------+
    |
latent image
    |
VAE decoder
    |
image
```

Example:

Prompt:

```
a robot walking in Tokyo at night,
cinematic lighting
```

The model does:

```
noise image

step 1:
noise -> slightly recognizable shapes

step 20:
objects appear

step 50:
details appear
```

---

## 3. Why Stable Diffusion changed the world

Before:

```
AI image generation
=
big company API only
```

After Stable Diffusion:

```
AI image generation
=
download model
+
run locally
+
fine tune yourself
```

This created:

* ComfyUI ecosystem
* LoRA fine-tuning
* DreamBooth
* ControlNet
* thousands of community models

---

## 4. Major Stability models

### Stable Diffusion 1.x

Parameters:

~860M

Strength:

* lightweight
* huge ecosystem
* runs on consumer GPUs

Example:

RTX 3060/4060:

```
512x512 generation
possible
```

---

### Stable Diffusion XL (SDXL)

Released 2023.

Much larger:

```
SD 1.5:
~860M params

SDXL:
~3.5B params
```

Improvements:

* better composition
* better typography
* higher resolution
* better human anatomy

Pipeline:

```
Prompt
 |
Dual CLIP encoders
 |
Base diffusion model
 |
Refiner model
 |
VAE
 |
Image
```

---

### SDXL Turbo

A major optimization.

Normal diffusion:

```
50 steps
```

Turbo:

```
1-4 steps
```

Uses:

* Adversarial Diffusion Distillation (ADD)

Tradeoff:

```
speed ↑↑↑
quality slightly ↓
```

Good for:

* real-time apps
* interactive generation

---

### Stable Diffusion 3 / 3.5

Newer generation.

Architecture moves toward:

```
U-Net
  |
  v
Transformer diffusion (DiT style)
```

Similar direction as:

* OpenAI Sora
* FLUX
* Imagen

Uses:

* better text understanding
* better prompt following
* improved typography

---

## 5. How training works

Simplified:

Take image:

```
x0 = real image
```

Add noise:

```
x_t = sqrt(alpha)*x0 + sqrt(1-alpha)*epsilon
```

where:

```
epsilon = random Gaussian noise
```

Train model:

Input:

```
(noisy image, timestep, text)
```

Predict:

```
noise epsilon
```

Loss:

```
L = ||epsilon - epsilon_theta(x_t,t,c)||^2
```

The model learns:

"Given noisy image + text, what noise should I remove?"

---

## 6. Ecosystem

The biggest impact is not only the base model.

### ComfyUI

Node-based workflow:

```
Checkpoint
    |
CLIP
    |
Sampler
    |
ControlNet
    |
LoRA
    |
VAE
    |
Output
```

It became the "Linux terminal" of image generation.

---

### LoRA

Small adapters:

Base model:

```
3.5B parameters
```

LoRA:

```
10MB-200MB
```

Train:

```
new style
new character
new product
```

without full fine-tuning.

---

### ControlNet

Adds control:

Input:

```
edge map
pose
depth
sketch
```

Output:

same composition but generated style.

---

## 7. Comparison with other image models

| Model            | Company           | Strength              |
| ---------------- | ----------------- | --------------------- |
| Stable Diffusion | Stability AI      | open ecosystem        |
| SDXL             | Stability AI      | quality + community   |
| SD3.5            | Stability AI      | better understanding  |
| FLUX             | Black Forest Labs | very high quality     |
| Midjourney       | Midjourney        | artistic quality      |
| Imagen           | Google            | photorealism          |
| DALL-E           | OpenAI            | instruction following |

---

## 8. Why engineers like Stable Diffusion

For an AI engineer:

It is similar to Linux.

Closed models:

```
call API
```

Stable Diffusion:

```
download checkpoint
inspect architecture
modify scheduler
train LoRA
build pipeline
deploy locally
```

You can experiment with:

* attention
* VAE
* samplers
* quantization
* distillation
* inference optimization

---

## 9. Current trend

The field is moving:

```
GAN
 |
v
Diffusion U-Net
 |
v
Latent Diffusion
 |
v
Diffusion Transformer (DiT)
 |
v
Multimodal foundation models
```

Stable Diffusion was the point where image generation became an open engineering ecosystem.

For someone already working with LLMs, the interesting connection is:

```
LLM:
token space -> transformer -> next token

Image diffusion:
latent space -> transformer/U-Net -> denoise step
```

Both are large-scale representation learning systems; only the prediction objective differs.

References:

* [Stable Diffusion paper (Latent Diffusion Models)](https://arxiv.org/abs/2112.10752?utm_source=chatgpt.com)
* [Stable Diffusion 3 paper](https://arxiv.org/abs/2403.03206?utm_source=chatgpt.com)
* [Stability AI official site](https://stability.ai?utm_source=chatgpt.com)
* [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI?utm_source=chatgpt.com)
