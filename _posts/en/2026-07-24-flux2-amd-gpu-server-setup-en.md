---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX.2 AMD GPU Server Setup
translated: false
type: note
---

## ✅ Comprehensive Summary

### Server Setup

| Step | Status |
| ------ | -------- |
| SSH connection test | ✅ Connected |
| GPU detection (ROCm) | ✅ AMD Radeon GPU, 48GB VRAM |
| tmux installed | ✅ |
| Python venv created (`/root/flux_env`) | ✅ |

### GPU Specs

- **GPU**: AMD RDNA 3 (gfx1100) — 48GB VRAM (Samsung)
- **ROCm**: v7.2.1, HIP 7.2.53211
- **CPU**: AMD EPYC 9334, 128 threads
- **RAM**: 503 GB
- **Disk**: 3.5T (2.9T free)

### Software Installed

| Package | Version | Notes |
| --------- | --------- | ------- |
| PyTorch | 2.13.0+rocm7.2 | ROCm 7.2 compatible |
| diffusers | 0.39.0 | Latest |
| transformers | 4.57.6 | Downgraded from 5.x for compatibility |
| accelerate | 1.14.0 | For CPU offloading |
| sentencepiece | 0.2.2 | Tokenizer |
| huggingface-hub | logged in with token | HF mirror configured |

### Issues Encountered & Fixes

1. **No network to huggingface.co** → Used `HF_ENDPOINT=https://hf-mirror.com` (Tsinghua mirror)

2. **Transformers 5.x incompatible with diffusers** → Downgraded to `transformers==4.57.6`

3. **Wrong pipeline class** → FLUX.2-dev uses `Flux2Pipeline` (not `FluxPipeline`)

4. **OOM on `pipe.to("cuda")`** → Model ~35GB in bf16, tried to load all at once into 48GB VRAM → Fixed with `pipe.enable_model_cpu_offload()` (keeps only one component on GPU at a time)

### Final Script (`/root/run_flux.py`)

- Loads FLUX.2-dev with CPU offloading
- Generates "A cute cat holding a sign that says hello world" at 1024×1024
- 28 inference steps
- Saves result to `test_flux.png`

### How to Run

```bash
ssh -p 31145 root@36.150.116.206
tmux new -s flux
source /root/flux_env/bin/activate
python3 /root/run_flux.py
```

Detach with `Ctrl+B, D` · Re-attach with `tmux attach -t flux`
