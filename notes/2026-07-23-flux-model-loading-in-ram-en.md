---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flux Model Loading in RAM
translated: false
type: note
---

## Question: Explain this `stable-diffusion.cpp` Flux model loading log

This is a **FLUX.1-schnell inference log using stable-diffusion.cpp / ggml backend**. It shows:

1. Model architecture detected
2. Quantized weights loaded
3. Text encoder loaded
4. VAE loaded
5. Flux transformer loaded
6. Sampling started

The interesting part: **the whole Flux model is running mostly in RAM, not VRAM**.

---

## 1. Weight type statistics

```
Conditioner weight type stat:          f16: 196
Diffusion model weight type stat:     q4_0: 776
VAE weight type stat:                  f32: 244
```

FLUX pipeline has three major components:

```
Prompt
 |
 v
Text Encoder (CLIP + T5)
 |
 v
Flux Transformer (denoiser)
 |
 v
VAE Decoder
 |
 v
Image
```

### Conditioner

```
f16: 196
```

This is the text conditioning model.

Usually:

* CLIP-L
* T5-XXL (optional)

Here:

```
clip_l.safetensors
```

is loaded.

---

### Diffusion model

```
q4_0: 776
```

This is the big Flux transformer.

Original:

```
FLUX.1-schnell
~12B parameters
```

Normally:

```
BF16:
~23-24 GB
```

Here:

```
Q4_0 quantization
```

means:

* 4-bit weights
* ggml format
* much smaller memory

Approx:

```
12B * 4 bits
=
6 GB
```

Matches:

```
diffusion_model 6389.02MB
```

So this is the main memory saving.

---

### VAE

```
f32: 244
```

VAE decoder is small.

Memory:

```
160 MB
```

It converts latent space:

```
latent tensor
      |
      v
 VAE decoder
      |
      v
 RGB image
```

---

# 2. Warning

```
t5xxl text encoder not found!
Prompt adherence might be degraded.
```

Important.

Full FLUX uses:

```
CLIP-L
+
T5-XXL
```

Architecture:

```
Prompt
 |
 +--> CLIP-L
 |
 +--> T5-XXL
          |
          v
       Flux transformer
```

You only have:

```
CLIP-L
```

Missing:

```
T5-XXL
```

Effect:

* image quality still works
* prompt following worse
* complex descriptions worse

Example:

Prompt:

> "A red dragon flying above a medieval city, cinematic lighting, detailed scales"

Without T5:

Maybe:

```
dragon + city
```

With T5:

More likely:

```
red dragon
medieval architecture
lighting
scale details
composition
```

---

# 3. Flux architecture

```
flux:
depth = 19
depth_single_blocks = 38
guidance_embed = false
context_in_dim = 4096
hidden_size = 3072
num_heads = 24
```

This describes the Transformer.

Similar to LLM:

```
Input tokens
    |
    v
Transformer blocks
    |
    v
latent image tokens
```

---

## hidden_size

```
hidden_size = 3072
```

Equivalent to LLM embedding dimension.

For comparison:

GPT-2 1.5B:

```
hidden=1600
```

Llama 7B:

```
hidden=4096
```

Flux:

```
3072
```

---

## Attention heads

```
num_heads=24
```

Each head:

```
3072 / 24

=128 dimensions/head
```

Same pattern as LLMs.

---

## Depth

```
depth=19
depth_single_blocks=38
```

Total transformer blocks:

```
19 double blocks
+
38 single blocks
```

Very deep network.

---

# 4. Memory allocation

Important line:

```
total params memory size =
6784.08MB

VRAM 0.00MB
RAM 6784.08MB
```

Meaning:

```
GPU:
0 MB

CPU RAM:
6.8 GB
```

Your model is not on GPU.

The backend is doing CPU inference.

Architecture:

```
CPU RAM
 |
 | weights
 |
Flux Q4 model
 |
CPU compute
 |
image
```

No CUDA acceleration.

---

# 5. Flux FLOW mode

```
running in Flux FLOW mode
```

FLUX uses a different diffusion process.

Classic Stable Diffusion:

```
noise
 |
UNet
 |
noise prediction
 |
many steps
 |
image
```

Flux:

```
noise
 |
Transformer
 |
flow matching
 |
few steps
 |
image
```

Flow matching:

```
x(t)
=
(1-t)*noise + t*image
```

The model learns the velocity:

```
dx/dt
```

instead of noise.

---

# 6. Image generation

```
generate_image 1024x1024
```

Resolution:

```
1024 × 1024

= 1,048,576 pixels
```

---

# 7. Flux scheduler

```
image_seq_len=16384
steps=4
mu=3.230
```

Interesting.

For Flux:

Image becomes tokens.

1024x1024:

latent size:

```
128x128
```

Flux patching:

```
128*128
=
16384 tokens
```

So:

```
image_seq_len=16384
```

is the transformer sequence length.

Similar to LLM:

```
text tokens:
8192 tokens

image tokens:
16384 tokens
```

---

# 8. Euler sampling

```
sampling using Euler method
```

Numerical ODE solver.

Flow matching:

Model predicts:

```
velocity v(x,t)
```

Euler:

```
x_next =
x + step * v(x,t)
```

Only:

```
4 steps
```

because:

```
FLUX.1-schnell
```

is optimized for speed.

---

# 9. Prompt tokenization

```
"a cyberpunk street at night, neon reflections"
```

CLIP BPE:

```
[
a</w>,
cyberpunk</w>,
street</w>,
at</w>,
night</w>,
,
neon</w>,
reflections</w>
]
```

CLIP vocabulary:

```
vocab size: 49408
```

This is OpenAI CLIP tokenizer.

---

# 10. Loading CLIP

```
loading 196/196 tensors

clip_l.safetensors

112.36MB/s
```

Loaded:

```
235 MB RAM
```

Time:

```
2 seconds
```

---

# 11. Loading Flux transformer

```
loading 776/776 tensors

flux1-schnell-Q4_0.gguf
```

Memory:

```
6389 MB
```

Time:

```
0.4 seconds
```

Very fast because:

```
GGUF mmap + sequential read
```

---

# 12. Compute buffer

```
flux compute buffer size:
2361.25 MB
```

This is temporary working memory.

During inference:

```
weights:
6.4GB

+
activation:
2.3GB

+
VAE:
160MB

+
text:
235MB

----------------

~9GB RAM
```

---

# Overall architecture

Your setup:

```
                 Prompt
                   |
                   v
              CLIP-L f16
              235MB RAM
                   |
                   |
                   v
        Flux Transformer Q4_0
        12B params
        6.4GB RAM
                   |
                   |
                   v
             VAE decoder
             160MB
                   |
                   v

              1024x1024 image
```

---

# Why this works on small hardware

Because:

Original:

```
FLUX.1-schnell BF16

~24GB VRAM
```

Your version:

```
Q4_0

~6.4GB RAM
```

Tradeoff:

|          | BF16       | Q4                |
| -------- | ---------- | ----------------- |
| Memory   | huge       | small             |
| Speed    | faster GPU | slower CPU        |
| Quality  | best       | slightly lower    |
| Hardware | H100/4090  | laptop/server CPU |

---

Given your RTX 4070 (12GB), this Q4 model is actually a good fit. A CUDA ggml backend could probably move:

```
Flux weights:
6.4GB

+
compute:
2.3GB

≈ 9GB VRAM
```

and leave room for VAE/CLIP, so GPU acceleration should be possible if your build has CUDA enabled.