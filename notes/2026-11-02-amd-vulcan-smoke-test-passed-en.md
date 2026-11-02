---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Vulcan Smoke Test Passed
translated: false
type: note
---

Smoke test passed. Here's the summary:

## Result

Generated image: `smoke-out/fox_512_vulkan1.png` (512×512, 20 steps) on the **AMD Radeon Pro WX 9100** via Vulkan.

## What I did

1. **Found the build** — `build/bin/sd-cli` already built with `SD_VULKAN=ON`.
2. **Detected GPUs** — `--list-devices`:
   - `Vulkan0` Intel HD Graphics 530 (iGPU)
   - `Vulkan1` AMD Radeon Pro WX 9100 (discrete, 16 GB)
   - `CPU` Intel i5-6500
3. **Fixed the model** — `models/sd15-q4_0.gguf` was a truncated download (48 MB missing, causing `tensor ... extends beyond its model file`). Resumed it from `second-state/stable-diffusion-v1-5-GGUF` to the full 1,566,768,416 bytes.
4. **Ran the smoke test** on all three backends.

## Working GPU command

```bash
GGML_VK_DISABLE_FUSION=1 ./build/bin/sd-cli \
  -m models/sd15-q4_0.gguf \
  -p "a red fox in a snowy forest, highly detailed, cinematic lighting" \
  -n "blurry, low quality" \
  -W 512 -H 512 --steps 20 --seed 42 --cfg-scale 7.0 \
  --backend "diffusion=vulkan1,vae=vulkan1,te=vulkan1" \
  -o smoke-out/fox_512_vulkan1.png
```

**Performance:** 11.51 s sampling + 1.13 s VAE decode = **12.98 s** for 20 steps at 512×512.

## Important finding

The AMD GPU **crashes with a Vulkan device-lost error** (`vk::Queue::submit: ErrorDeviceLost`) when ggml Vulkan **fusion is enabled** (the default). Setting `GGML_VK_DISABLE_FUSION=1` makes it stable. This is a RADV/Vega10 driver issue, not a project bug.

Other backends verified:
- `Vulkan0` (Intel iGPU): works without the env var, but slower (~4.2 s/it vs ~0.6 s/it on AMD).
- `CPU`: works, ~3.9 s/it at 256×256.

Outputs are in `smoke-out/`: `fox_512_vulkan1.png`, `smoke_vulkan1.png`, `smoke_vulkan0.png`, `smoke_cpu.png`. No source files were modified.