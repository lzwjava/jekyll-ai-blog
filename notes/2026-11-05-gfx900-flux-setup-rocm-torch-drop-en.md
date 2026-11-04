---
audio: false
generated: true
image: false
lang: en
layout: post
title: "gfx900 FLUX Setup: ROCm Torch Drop"
translated: false
type: note
---

Status so far:

**Done**

| Step | Result |
| --- | --- |
| Env | `.venv` (py3.12) + `fluxreel -e .` installed |
| ffmpeg | via `imageio-ffmpeg` → `~/.local/bin/ffmpeg` (has libx264) |
| Pipeline smoke test | ✅ passed — 1080×1920, 30 fps, 15.00 s, H.264+AAC, CJK slide rendered |
| Server | ✅ `fluxreel server --port 8000` → `/health` ok, `/` 24 KB SPA |
| GPU found | AMD Radeon Pro WX 9100 (gfx900, Vega 10), 17.2 GB VRAM, ROCm 7.1 |
| ROCm torch | ✅ torch 2.2.2+rocm5.7 works on gfx900 (needed execstack fix); torch 2.13+rocm7.1 **fails** — no gfx900 kernels |
| HIP on gfx900 | ✅ `hipcc --offload-arch=gfx900` compiles + runs |
| sd.cpp Vulkan | ✅ built, sees `AMD Radeon Pro WX 9100 (RADV VEGA10)` |
| sd.cpp HIP | 🔄 building (59%) |
| Models | 🔄 flux1-schnell-Q4_0 3.2/6.8 GB, t5-xxl-Q4 2.8/3.1 GB; ae + clip_l done |

**Key finding:** PyTorch's current ROCm wheels (6.3/6.4/7.x) dropped gfx900, so the `local` diffusers provider can't run on this card with a modern torch. Two working paths remain: sd.cpp on **HIP/ROCm** (building now) or sd.cpp on **Vulkan** (already built), both using the repo's `sdcpp` provider.

Next: finish the HIP build + FLUX download, then run `tests/smoke_test.py --provider sdcpp` for real GPU image generation.
