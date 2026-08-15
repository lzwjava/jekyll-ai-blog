---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX Model Files and Parameters
translated: false
type: note
---

Question: What do the `FLUX` model files and `sd-cli` parameters mean, and what are the optional parameters?

Answer:

In your command, **FLUX is not one single model file**. It is a pipeline composed of several neural-network components:

```text
                    prompt
                      │
          ┌───────────┴───────────┐
          │                       │
       CLIP-L                  T5-XXL
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
               FLUX Transformer
                flux1-schnell
                      │
                      ▼
                    VAE
                      │
                      ▼
                 PNG image
```

### 1. `flux1-schnell-Q4_0.gguf`

```bash
--model flux1-schnell-Q4_0.gguf
```

This is the **main FLUX transformer**.

For FLUX.1:

* `flux1-schnell` = FLUX.1 Schnell
* `schnell` means **fast**
* It was designed for very few sampling steps, typically around **1–4 steps**
* `Q4_0` = 4-bit quantization
* `.gguf` = the GGUF model format commonly used by `llama.cpp`-style C/C++ inference projects, including `stable-diffusion.cpp`

Conceptually, this is the largest/most important part:

```text
text conditioning
       ↓
FLUX Transformer
       ↓
latent representation
```

The transformer predicts how the noisy latent should be transformed toward the final image.

`Q4_0` reduces memory substantially compared with FP16:

```text
FP16:
  ~16 bits / weight

Q8:
  ~8 bits / weight

Q4:
  ~4 bits / weight
```

The tradeoff is some quality/accuracy loss.

---

### 2. `ae.safetensors`

```bash
--vae ae.safetensors
```

This is the **VAE / Autoencoder**.

For FLUX, `ae.safetensors` is essentially the component that converts between:

```text
image ↔ latent
```

During generation:

```text
FLUX transformer
       ↓
latent
       ↓
VAE decoder
       ↓
RGB image
```

So the VAE is **not generating the image semantics**.

The transformer decides things like:

> cat + astronaut + rocket

while the VAE turns the resulting latent representation into actual pixels.

---

### 3. `clip_l.safetensors`

```bash
--clip_l clip_l.safetensors
```

This is **CLIP-L**, the CLIP text encoder.

Your prompt:

```text
"a cat astronaut riding a rocket"
```

gets converted into numerical representations by the text encoders.

CLIP-L is one of the two text-conditioning systems used by original FLUX.

Very roughly:

```text
"a cat astronaut riding a rocket"
             ↓
          CLIP-L
             ↓
      text embeddings
```

---

### 4. `t5xxl_fp16.safetensors`

```bash
--t5xxl t5xxl_fp16.safetensors
```

This is the second text encoder:

**T5-XXL**.

FLUX uses both:

```text
                 prompt
                   │
          ┌────────┴────────┐
          ↓                 ↓
       CLIP-L             T5-XXL
          │                 │
          └────────┬────────┘
                   ↓
             FLUX Transformer
```

This is an important design choice in FLUX.

T5-XXL is a very large language model/text encoder, giving FLUX considerably richer text conditioning than simply using CLIP.

And notice:

```text
t5xxl_fp16
```

is **FP16**, not quantized.

So even though your main FLUX model is:

```text
Q4_0
```

you are still loading a potentially large T5-XXL model.

If VRAM/RAM is your concern, **T5-XXL can be a significant part of the memory footprint**.

---

# Your generation parameters

### `--cfg-scale 1.0`

```bash
--cfg-scale 1.0
```

CFG = **Classifier-Free Guidance**.

Traditional diffusion models often use something like:

```text
CFG = 5
CFG = 7
CFG = 7.5
```

Higher CFG generally pushes the image more strongly toward the prompt, but can introduce artifacts/overcooking.

For **FLUX.1 Schnell**, `1.0` is normal because Schnell was designed around a different guidance formulation / low-step generation.

So:

```bash
--cfg-scale 1.0
```

is not equivalent to saying "weak prompt".

It's basically appropriate for this Schnell setup.

---

### `--steps 4`

```bash
--steps 4
```

This is the number of diffusion/flow integration steps.

For Schnell:

```text
1 step  → extremely fast
2 steps → fast
4 steps → common
```

Compare this conceptually with older Stable Diffusion:

```text
SD 1.5:
20–50 steps

SDXL:
20–50 steps

FLUX.1 Schnell:
~1–4 steps
```

That's one of the major reasons Schnell is interesting.

---

### `--width 768 --height 768`

```bash
--width 768
--height 768
```

Output resolution:

```text
768 × 768
```

Number of pixels:

```text
768 × 768 = 589,824 pixels
```

Increasing resolution increases compute/memory roughly with the number of latent tokens.

For example:

```text
768²  =   589K pixels
1024² = 1.05M pixels
```

So 1024×1024 has roughly:

```text
1.05M / 0.59M ≈ 1.78×
```

as many pixels.

---

### `--output flux_out.png`

Just the output filename:

```bash
--output flux_out.png
```

---

### `--prompt`

```bash
--prompt "a cat astronaut riding a rocket"
```

Your text condition.

---

# The important distinction

Think of your files as:

| File                      | Role                                  |
| ------------------------- | ------------------------------------- |
| `flux1-schnell-Q4_0.gguf` | **Main image-generation transformer** |
| `t5xxl_fp16.safetensors`  | **Large text encoder**                |
| `clip_l.safetensors`      | **CLIP text encoder**                 |
| `ae.safetensors`          | **VAE / image ↔ latent conversion**   |

So if you delete the VAE:

```text
transformer → latent → ??? 
```

you can't decode the latent into an image.

If you delete T5:

```text
prompt → incomplete conditioning
```

and FLUX won't work in the intended configuration.

---

# What "Schnell" vs "Dev" means

This is probably the most useful distinction if you're experimenting with FLUX.

### FLUX.1 Schnell

```text
FLUX.1-schnell
      ↓
few steps
      ↓
very fast generation
```

Good for:

* local inference
* interactive applications
* agents
* image generation where latency matters

### FLUX.1 Dev

```text
FLUX.1-dev
      ↓
more computation
      ↓
generally better quality / adherence
```

It normally requires significantly more computation than Schnell.

So your current setup:

```bash
flux1-schnell-Q4_0.gguf
--steps 4
```

is basically optimized for:

> **"Give me a decent FLUX image extremely quickly on relatively limited hardware."**

---

# Other useful `sd-cli` options

The exact options depend on the version/build of `stable-diffusion.cpp`, so check your binary directly:

```bash
/mnt/data/zz/flux/sd_cpp/build/bin/sd-cli --help
```

Typical controls include things like:

```bash
--seed
--steps
--cfg-scale
--width
--height
--output
--prompt
```

For reproducibility:

```bash
--seed 12345
```

Then the same model + prompt + parameters should produce the same/similar result.

For example:

```bash
sd-cli \
  --model flux1-schnell-Q4_0.gguf \
  --vae ae.safetensors \
  --clip_l clip_l.safetensors \
  --t5xxl t5xxl_fp16.safetensors \
  --steps 4 \
  --cfg-scale 1.0 \
  --width 768 \
  --height 768 \
  --seed 42 \
  --output cat.png \
  --prompt "a cat astronaut riding a rocket"
```

The **most interesting thing to inspect next is actually the memory architecture**: how much RAM/VRAM each of `FLUX Q4`, `T5-XXL`, `CLIP-L`, and the VAE consumes, and which components `stable-diffusion.cpp` keeps on GPU vs CPU. That explains why a quantized FLUX model can run on a 12–16 GB GPU while still needing substantial system RAM.
