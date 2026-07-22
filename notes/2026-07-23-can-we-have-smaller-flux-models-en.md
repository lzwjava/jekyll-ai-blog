---
audio: false
generated: true
image: false
lang: en
layout: post
title: Can we have smaller FLUX models
translated: false
type: note
---

## Question: Can we have smaller FLUX models?

## Answer:

Yes, but **not officially from Black Forest Labs for the main FLUX family**. The original FLUX.1 models are intentionally large:

| Model          | Params | Purpose                       |
| -------------- | -----: | ----------------------------- |
| FLUX.1-pro     |   ~12B | best quality, API             |
| FLUX.1-dev     |   ~12B | open weights for research/dev |
| FLUX.1-schnell |   ~12B | distilled fast inference      |

The core transformer is still around **12B parameters**. There is no official "FLUX-3B" or "FLUX-1B" equivalent.

But the ecosystem has created smaller variants.

---

## 1. Quantized FLUX (same model, smaller memory)

This is the easiest path.

Original:

```
12B params
BF16

12B * 2 bytes ≈ 24GB
+ activations
+ text encoder
+ VAE
```

Need:

```
24GB+ VRAM
```

Quantized:

```
FP8:
12B * 1 byte ≈ 12GB

INT8:
≈12GB

4-bit:
≈6GB
```

So RTX 4070 12GB becomes much more realistic.

Examples:

* FP8 FLUX
* NF4 / bitsandbytes
* GGUF FLUX variants

Architecture unchanged:

```
12B Transformer
      |
   quantized weights
      |
  RTX 4070
```

---

## 2. FLUX LoRA (small adapter)

A very common approach:

Instead of training:

```
12B model
all weights
```

train:

```
12B frozen model
+
50MB-500MB LoRA
```

Example:

```
FLUX.1-dev
      |
      + LoRA
          |
          special style/person/object
```

This is how many creators customize FLUX.

---

## 3. Distilled / community smaller models

The open-source community is moving toward:

```
12B FLUX teacher
        |
        | distillation
        v

3B / 2B student
```

Similar to LLMs:

```
DeepSeek-V3
       |
       v
 distilled 7B model
```

but image models are harder because:

* visual space is huge
* quality drops quickly
* text rendering suffers

---

## 4. Other small models with similar philosophy

If the goal is **learning image transformers**, smaller models exist:

### Stable Diffusion 1.5

```
~860M params
```

Runs easily:

```
RTX 4070
8GB VRAM
```

Architecture:

```
UNet + cross attention
```

Good for learning diffusion.

---

### SDXL

```
~2.6B params
```

RTX 4070:

```
works with optimization
```

Closer quality to FLUX.

---

### PixArt-α / PixArt-Sigma

Transformer diffusion:

```
~0.6B-0.9B
```

Architecture closer to FLUX:

```
text encoder
      |
      v
Diffusion Transformer
      |
      v
VAE
```

Good research model.

---

## 5. The interesting research direction

The future probably looks like:

```
2024:

FLUX 12B
Stable Diffusion XL 2.6B


2026+:

Image foundation model
       |
       + 12B teacher
       |
       + 3B edge model
       |
       + 700M mobile model
```

Same trend as LLMs:

```
GPT-4
 |
 + GPT-4o-mini
 + distilled models
 + local 7B models
```

---

For your RTX 4070 (12GB), I would rank experiments:

1. **FLUX.1-schnell FP8/quantized** → learn current frontier
2. **SDXL** → understand diffusion engineering
3. **PixArt-Sigma** → understand DiT/Transformer image models
4. Train a tiny DiT yourself → closest equivalent to your nanoGPT experiments

The most educational path is probably **PixArt-Sigma + your nanoGPT knowledge**, because the forward pass is much closer to LLM-style transformer training.