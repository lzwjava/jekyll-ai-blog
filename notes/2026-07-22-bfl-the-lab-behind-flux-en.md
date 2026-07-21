---
audio: false
generated: true
image: false
lang: en
layout: post
title: "BFL: The Lab Behind FLUX"
translated: false
type: note
---

Question: Intro to Black Forest Labs (BFL), the lab behind FLUX models.

Answer:

Black Forest Labs (BFL) is a German AI research lab focused on **visual intelligence** — building foundation models that understand and generate images (and eventually broader visual worlds). Their slogan “Powering visual intelligence everywhere” refers to the goal of moving beyond simple image generation into systems that can perceive, reason about, and create visual content. ([Black Forest Labs][1])

The important history:

```
Latent Diffusion research
        |
        v
Stable Diffusion (2022)
        |
        v
Black Forest Labs (2024)
        |
        v
FLUX.1 / FLUX.2 models
```

The founding team came from the original Stable Diffusion research ecosystem, including researchers such as Robin Rombach, Andreas Blattmann, and Patrick Esser. They previously worked on latent diffusion models that became the foundation of Stable Diffusion. ([Black Forest Labs][1])

## Why BFL matters

Before FLUX, the major open image generation players were:

* Stable Diffusion / SDXL
* Midjourney
* DALL·E

BFL entered with FLUX.1 in 2024 and pushed image generation quality significantly, especially:

* prompt following
* human anatomy
* typography/text rendering
* complex scenes
* photorealism

FLUX.1 models use a **12B parameter hybrid diffusion transformer architecture** based on flow matching ideas rather than the older U-Net style diffusion pipeline. ([Black Forest Labs][2])

High-level architecture:

```
Text prompt
    |
    v
Text encoder
    |
    v
Conditioning embeddings
    |
    v
Diffusion Transformer (DiT)
    |
    v
Latent image representation
    |
    v
VAE decoder
    |
    v
Generated image
```

Similar to LLM evolution:

```
GPT:
tokens -> Transformer -> next token

FLUX:
noise latent -> Transformer -> denoise latent -> image
```

The core idea is also Transformer scaling, but instead of predicting tokens, the model predicts the denoising trajectory of image latents.

---

## FLUX model family

Original FLUX.1:

| Model            | Purpose                               |
| ---------------- | ------------------------------------- |
| FLUX.1 [pro]     | Best quality, API/commercial          |
| FLUX.1 [dev]     | Open weights, research/non-commercial |
| FLUX.1 [schnell] | Fast local inference                  |

([Black Forest Labs][2])

For local GPU users:

```
FLUX.1-schnell
    |
    +-- RTX 4090 / 3090 possible
    +-- 12GB VRAM difficult
    +-- quantization/offload helps

FLUX.1-dev
    |
    +-- much heavier
    +-- usually 24GB+ VRAM
```

Your RTX 4070 12GB can run FLUX with optimizations, but it is a tight fit. Typical tricks:

```bash
--cpu-offload
--vae-cpu-offload
fp8 weights
quantized transformers
```

---

## BFL vs OpenAI / Google / Midjourney

A rough map:

| Company               | Main visual AI                    |
| --------------------- | --------------------------------- |
| OpenAI                | DALL·E / GPT vision ecosystem     |
| Google DeepMind       | Imagen, Gemini vision             |
| Midjourney            | closed creative image model       |
| Stability AI          | Stable Diffusion                  |
| **Black Forest Labs** | **FLUX visual foundation models** |

BFL's interesting position is:

```
Academic research
       +
Open model philosophy
       +
Startup execution
       =
FLUX ecosystem
```

They are closer culturally to early OpenAI + early Stability AI: publish strong research, release usable models, attract developers. ([Black Forest Labs][2])

---

## Why AI engineers care

For LLM people, FLUX is interesting because it shows the same scaling trend:

LLMs:

```
Transformer
+
more parameters
+
more data
+
better alignment
=
GPT class models
```

Visual models:

```
Diffusion Transformer
+
more image/video data
+
better conditioning
+
larger compute
=
visual intelligence models
```

BFL's longer-term vision is not only "generate pictures":

```
image generation
        |
        v
image editing
        |
        v
video generation
        |
        v
world understanding
        |
        v
embodied AI / robotics
```

They describe their goal as building infrastructure for visual intelligence, not only creative tools. ([Black Forest Labs][1])

---

References:

* Black Forest Labs — About ([Black Forest Labs][1])
* Announcing Black Forest Labs / FLUX.1 release ([Black Forest Labs][2])
* Black Forest Labs Series B announcement ([Black Forest Labs][3])
* FLUX model overview ([docs.bfl.ml][4])

[1]: https://bfl.ai/about?utm_source=chatgpt.com "About | Black Forest Labs"
[2]: https://bfl.ai/blog/24-08-01-bfl?utm_source=chatgpt.com "Announcing Black Forest Labs | Black Forest Labs"
[3]: https://bfl.ai/blog/our-300m-series-b?utm_source=chatgpt.com "Laying the Foundations for Visual Intelligence—Our $300M Series B | Black Forest Labs"
[4]: https://docs.bfl.ml/?trk=public_post_main-feed-card-text&utm_source=chatgpt.com "Welcome to BFL Documentation! - Black Forest Labs"
