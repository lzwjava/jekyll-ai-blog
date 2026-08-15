---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flux Model Setup on GPU-Locked Laptop
translated: false
type: note
---

Found everything. Here's the full picture:

## Where FLUX.1-schnell lives on this laptop

**1. The official HuggingFace cache** (full diffusers format, 2.3 GB):

```
/home/lzw/.cache/huggingface/hub/models--black-forest-labs--FLUX.1-schnell
```

**2. The working setup you actually run** (stable-diffusion.cpp with quantized GGUF):

```
Binary:  /mnt/data/zz/flux/sd_cpp/build/bin/sd-cli
Models:  /mnt/data/zz/flux/models/
  ├── flux1-schnell-Q4_0.gguf      (6.3G — the model)
  ├── ae.safetensors               (320M — VAE)
  ├── clip_l.safetensors           (235M — text encoder)
  └── t5xxl_fp16.safetensors       (9.2G — text encoder)
```

Plus your own CLI wrapper, `fluxreel` (installed at `~/.local/bin/fluxreel`), which wraps the sd-cli setup.

## How to run it

```bash
# easiest — your wrapper
fluxreel img "a cat astronaut riding a rocket"

# or directly via sd-cli
/mnt/data/zz/flux/sd_cpp/build/bin/sd-cli \
  --model /mnt/data/zz/flux/models/flux1-schnell-Q4_0.gguf \
  --vae /mnt/data/zz/flux/models/ae.safetensors \
  --clip_l /mnt/data/zz/flux/models/clip_l.safetensors \
  --t5xxl /mnt/data/zz/flux/models/t5xxl_fp16.safetensors \
  --cfg-scale 1.0 --steps 4 --width 768 --height 768 \
  --output flux_out.png --prompt "a cat astronaut riding a rocket"
```

## ⚠️ The blocker right now

Your **RTX 4070 (12 GB) is fully occupied** by a training job:

```
PID 522494  python3.12 train.py config/train_bilingual.py   (running 22h 53m)
cwd: /mnt/data/nanoGPT
GPU: 8.7 GB VRAM used, GPU util 100%  →  only ~1.7 GB free
```

`fluxreel img` needs ~10 GB VRAM budget (4 GB model + text encoders), so it will OOM or fail while that job runs.

**Your options:**

1. Wait for the nanoGPT training to finish (~1.7 GB free isn't enough), or
2. Stop the training job and then run flux.

Want me to kill the nanoGPT training process (PID 522494) so you can generate images? It's been running ~23 hours, so you may want to check its checkpoint progress in `/mnt/data/nanoGPT` first.
