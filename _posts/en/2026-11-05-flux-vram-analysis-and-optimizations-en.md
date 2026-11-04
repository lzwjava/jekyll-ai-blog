---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX VRAM Analysis and Optimizations
translated: false
type: note
---

## Summary of what I found

**Machine:** RTX 4070 (Ada, CUDA 13, driver 580), **12,282 MiB total**, ~1.35 GB held by the desktop → **~10.5 GB free**. torch 2.10.0+cu128 with `cuda.is_available() = True`, ffmpeg/ffprobe present, diffusers 0.39.0.

**The repo is AMD-targeted:** `--provider local` hardcodes `/root/FLUX.*` (remote ROCm box). The only GPU path that actually works here is `--provider sdcpp` (stable-diffusion.cpp CUDA build in `/mnt/data/zz/flux`), which is already CUDA-compiled.

**I ran the real sd-cli twice:**

| Attempt | Result |
| --- | --- |
| Everything on GPU (no `--backend`) | **OOM** — `cudaMalloc failed` for the 6,389 MB diffusion model |
| `--backend diffusion=cuda,clip=cpu,vae=cuda,t5xxl=cpu` | ✅ **Works** — 512×384, 2 steps, 60 s total |

## VRAM requirement (measured, FLUX.1-schnell Q4_0 GGUF)

Weight footprint reported by sd-cli:

| Component | Size | Placement |
| --- | --- | --- |
| T5-XXL fp16 | 9,318.83 MB | CPU (must offload) |
| FLUX Q4_0 diffusion | 6,389.02 MB | GPU |
| VAE | 160 MB | GPU |
| CLIP-L | ~246 MB (inside text_encoders) | CPU |
| **Total** | **15,867.85 MB** | |

| Mode | VRAM weights | + activations @960×720 | Peak need | Verdict on this 4070 |
| --- | --- | --- | --- | --- |
| Full GPU | 15.9 GB | ~1.5–2.5 GB | **~18 GB** | ❌ OOM (confirmed) |
| T5/CLIP on CPU | 6.55 GB | ~1.5–2 GB | **~8–8.5 GB** | ✅ fits in 10.5 GB free |
| Full GPU w/ fp8 T5 | ~11.3 GB | ~1.5–2 GB | ~13 GB | ⚠️ still too tight |

**Rules of thumb:**

- **Minimum:** ~7 GB VRAM + ~10 GB system RAM (T5 offloaded) → works on 8 GB cards at ≤768×576.
- **Comfortable for this card:** **8–9 GB free VRAM**, `--max-vram 9`, 960×720. Keep the desktop under ~2 GB.
- **Full-GPU (no offload):** needs **≥18 GB** (16 GB cards still need T5 offloaded; 24 GB is comfortable).
- **diffusers `local` path (bf16 FLUX, 12B params):** ~24 GB weights — only viable with sequential CPU offload on 12 GB, and you don't have those weights locally (only GGUF).

**Cost note:** each `sd-cli` run reloads the 6.4 GB diffusion model (~50 s of the 60 s). A 5-scene video ≈ **5 min**, nearly all of it model loading. A persistent `sd-server` (the binary is right there) would cut that to seconds per scene.

## What the change should be

1. **`smoke_test.py` + `fluxreel smoke`** — staged checks: deps/ffmpeg → GPU probe (`nvidia-smi` + CUDA) → sd-cli/model files → one tiny 512×384 image on the GPU → slide frame → 3 s 1080×1920 ffmpeg clip → ffprobe validation. `--quick` skips the GPU, `--full` runs the whole 5-scene pipeline.
2. **Offline scene planner** — `_generate_scenes()` currently *requires* OpenRouter; add a deterministic markdown-derived fallback (`--offline`) so the smoke test and video generation work with no network/cost.
3. **`sdcpp` provider → first-class local GPU backend** — auto-detect the CUDA build/models, pick the split backend by default (T5 on CPU), expose `--width/--height/--max-vram`, and report the GPU in logs. Optionally wrap `sd-server` to kill the 50 s/scene reload.
4. **Fix `local` (diffusers) for CUDA** — env-configurable model dir, `cuda` + bf16, model-CPU-offload instead of the ROCm-only assumptions, so it works if you ever download the full FLUX weights.
5. README/pyproject updates.

Want me to implement 1–3 now (smoke test + offline planner + CUDA-ready sdcpp defaults), and leave the `sd-server` speedup as a follow-up?
