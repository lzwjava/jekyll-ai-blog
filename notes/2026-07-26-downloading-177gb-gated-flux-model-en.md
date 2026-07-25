---
audio: false
generated: true
image: false
lang: en
layout: post
title: Downloading 177GB Gated FLUX Model
translated: false
type: note
---

`hf-mirror.com` is reachable! The model is **177 GB** total. Here's what I found:

---

## 📦 FLUX.2-dev — Model Info

| Property | Value |
|----------|-------|
| **Model** | `black-forest-labs/FLUX.2-dev` |
| **Pipeline** | `Flux2Pipeline` (diffusers) |
| **Total size** | **177 GB** |
| **Gated** | ✅ Yes — needs HF token + license acceptance |
| **Disk space** | 2.9T available ✅ |
| **Mirror** | `hf-mirror.com` (reachable ✅) |

### Files breakdown:
- `ae.safetensors` — Autoencoder
- `flux2-dev.safetensors` — Main FLUX model
- `text_encoder/model-00001~10-of-00010.safetensors` — T5 text encoder (~10 shards)
- `transformer/diffusion_pytorch_model-00001~07-of-00007.safetensors` — Transformer (~7 shards)
- `vae/diffusion_pytorch_model.safetensors` — VAE

### Issue: The model is **gated**

You need to:
1. Go to https://huggingface.co/black-forest-labs/FLUX.2-dev and **accept the license** (click "Agree")
2. Get a **HF token** (read-only is enough) from https://huggingface.co/settings/tokens
3. Pass it to us so we can log in via `huggingface-cli login --token YOUR_TOKEN`

Do you have a HuggingFace token ready? If so, I'll:
1. Set up a `tmux` session
2. Write the download script with `HF_ENDPOINT=https://hf-mirror.com`
3. Start the download to `/root/FLUX.2-dev`
