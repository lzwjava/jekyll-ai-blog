---
audio: false
generated: true
image: false
lang: en
layout: post
title: 33x Speedup with RTX 4070
translated: false
type: note
---

Done! Here's the full transformation:

---

### 🚀 Before vs After (RTX 4070)

| Stage | CPU (before) | GPU (now) | Speedup |
| ------- | :-----------: | :--------: | :-------: |
| Text encoding | 2.2s | **0.3s** | 7× |
| Flux diffusion (4 steps) | ~487s | **12.8s** | 38× |
| VAE decode | 37s | **2.7s** | 13× |
| **Total** | **526s** | **~16s** | **33×** |

### What was done

1. **Rebuilt `sd_cpp` with CUDA** — `cmake -DSD_CUDA=ON` detected your RTX 4070 (compute 8.9)
2. **Stopped `llama-server`** to free ~6 GB VRAM
3. **Key optimizations in `run.sh`**:
   - `--backend diffusion=cuda,clip=cpu,vae=cuda,t5xxl=cpu` — Flux + VAE on GPU, text encoders on CPU
   - `--vae-tiling` — VAE compute buffer dropped from **6.6 GB → 416 MB** with minimal speed loss
   - `--max-vram 10` — leaves headroom for desktop apps

### Issues found

- **T5XXL file** `t5xxl_fp16.safetensors` has corrupt tensors ("data offsets out of bounds"). Without it, prompt adherence is degraded. Re-download from [here](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp16.safetensors) to fix.

### Usage

```bash
cd /mnt/data/zz/flux
./run.sh "your prompt here"
```

Output saved to `outputs/flux_<timestamp>.png` (~1.7 MB).
