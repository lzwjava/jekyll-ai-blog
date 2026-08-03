---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX.1-schnell Running on AMD Vulkan
translated: false
type: note
---

All verified and working. Here's the complete rundown:

## ✅ Done — FLUX.1-schnell running on the AMD box via stable-diffusion.cpp (Vulkan)

### What was set up

| Component | Detail |
|---|---|
| **Project** | `/root/amd-hackathon-lzwjava/` — editable pip install into `/opt/venv`, `fluxreel` CLI available |
| **sd.cpp** | Built `sd-cli` + `sd-server` with **Vulkan backend** (github is blocked on that network — got the vendored source from the PyPI `stable-diffusion-cpp-python` 0.4.7 sdist instead) |
| **Models (17.2GB)** | `flux1-schnell-Q4_0.gguf` (6.8GB, unsloth), `t5xxl_fp16.safetensors` (9.8GB), `clip_l.safetensors`, `ae.safetensors` — downloaded via **hf-mirror.com** with your HF token (needed one resume after a dropped connection) |
| **Config** | `~/.config/fluxreel/.env` → `SDCPP_BIN`, `SDCPP_MODEL_DIR=/root/models`, `SDCPP_BACKEND=` (omit `--backend`; new sd.cpp has backend compiled in), 960×720, 4 steps |
| **Extras** | `ffmpeg` installed for the gen-video pipeline |

### Code fixes (committed as `fd713aa`)
1. **`cli.py`** — `load_env()` was never called in `main()`, so the `.env` config was ignored. Wired it up.
2. **`sd_cpp_provider.py`** — `--backend "diffusion=cuda,..."` was hardcoded; new sd.cpp rejects it. Added `SDCPP_BACKEND` env override (empty → omit flag → Vulkan auto-used; unset → old CUDA default preserved for your original setup).

### Verification — it works 🎉
- **Direct sd-cli**: 512×512 cat, 4 steps → **5.6s** on the AMD Radeon (RADV NAVI31, Vulkan 1.4, 51.5GB VRAM)
- **`fluxreel img`**: `"a cyberpunk city at night, neon reflections, rain"` → 960×720 PNG in **28.5s** (incl. 16s model load), saved to `/root/fluxreel_test.png`
- **`fluxreel -p 31329 info`** from your Mac: ROCm GPU, PyTorch 2.9.1 + HIP 7.2, 2.9TB free disk, 128 cores

### Notes
- GitHub direct is blocked on the box; hf-mirror.com works great (got ~10GB in ~3 min when the link held).
- Management commands (`info`/`download`/`tunnel`) run **from the Mac** against port **31329** (`fluxreel -p 31329 ...`); on the box itself, `fluxreel img` is the local-generation path.
- `gen-video --provider sdcpp` will use this local Vulkan FLUX for scene images; the LLM storyboarding step defaults to OpenRouter (needs your API key).

Sample commands on the remote:
```bash
/opt/venv/bin/fluxreel img "a dragon on a castle tower" --width 1024 --height 1024 --output /root/dragon.png
```
