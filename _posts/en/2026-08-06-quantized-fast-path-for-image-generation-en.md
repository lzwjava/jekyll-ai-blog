---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quantized Fast Path for Image Generation
translated: false
type: note
---

Here's a walkthrough of the **sd-cpp route** in `fluxreel/gen_video/providers/sd_cpp_provider.py` — the quantized fast path for image generation.

## What it is

A thin Python wrapper around **stable-diffusion.cpp's `sd-cli` binary** running **FLUX.1-schnell Q4_0 (4-bit GGUF)**. No torch, no diffusers, no Python inference — all the heavy compute happens inside a native C++ process. It plugs into the same `ImageProvider` ABC (`generate_image(prompt, scene_index) -> path | None`) as the OpenRouter and local diffusers providers, so the rest of the pipeline (scene planner → 5 images → ffmpeg assembly) doesn't care which backend produced the image.

## How the route works

**1. Model files** (`MODEL_FILES`) — FLUX is decomposed into 4 components, loaded separately:

- `flux1-schnell-Q4_0.gguf` — the 12B diffusion transformer, quantized to 4-bit (Q4_0)
- `ae.safetensors` — the VAE (latent ⇄ pixel decoder)
- `clip_l.safetensors` — the smaller text encoder
- `t5xxl_fp16.safetensors` — the big T5-XXL text encoder

**2. Validation** (`_check_files`) — every generation first verifies the binary and all 4 model files exist; fails fast with a readable message instead of a cryptic subprocess error.

**3. Generation** (`generate_image`) — builds a `subprocess.run` command to `sd-cli`:

```
sd-cli --diffusion-model flux1-schnell-Q4_0.gguf --vae ae.safetensors
       --clip_l ... --t5xxl ... --prompt "<prompt>" --cfg-scale 1.0
       --sampling-method euler --steps 4 --width 960 --height 720
       --seed 42 --output <tmp>/scene_000.png --vae-tiling
       --max-vram 10 --backend diffusion=cuda,clip=cpu,vae=cuda,t5xxl=cpu
```

Each image goes to a fresh `tempfile.mkdtemp`, so every call is self-contained and idempotent (5 parallel scene threads each get their own dir).

**4. Serialization** — the whole subprocess runs under a `threading.Lock()`. 5 scenes are submitted in parallel threads, but only one sd-cli run touches the GPU at a time.

**5. Error handling** — nonzero exit → greps stderr for `ERROR`/`error`/`failed` and prints the tail; also double-checks the PNG actually exists even on rc=0.

## Optimizations (the slide-worthy points)

| Optimization | What it does | Why it matters |
| --- | --- | --- |
| **Q4_0 4-bit quantization** | Diffusion model is GGUF Q4_0 instead of fp16/bf16 | ~4× smaller weights, far less VRAM per run (~8.75 GB), faster memory-bound decode |
| **4-step distilled inference** | `--steps 4` on FLUX.1-schnell (a distilled model) | ~7× fewer denoising steps vs. the 28-step dev variant |
| **VAE tiling** (`--vae-tiling`) | Decodes latent in tiles rather than one big image | Avoids OOM on the 12 GB card, especially at higher res |
| **`--max-vram 10` budget** | Tells sd.cpp to cap/plan allocations to 10 GB | Keeps the desktop (~2.9 GB) alive while sd-cli runs — stable on 12 GB-class cards |
| **Smart backend offload** | `diffusion=cuda, clip=cpu, vae=cuda, t5xxl=cpu` | Only the expensive transformer + VAE hit the GPU; the two text encoders run on CPU to save VRAM |
| **Process-per-image + lock** | Fresh sd-cli per generation, serialized by a mutex | No persistent pipeline = no memory leaks / VRAM fragmentation; lock prevents concurrent runs from exhausting VRAM |
| **4:3 sized output (960×720)** | Matches the video slide layout | Fewer pixels than 1024² → less GPU time, and no wasted upscaling in the slide composer |
| **Seeded determinism** | Fixed `seed=42` | Reproducible outputs across runs; caching-friendly |
| **`--cfg-scale 1.0`** | No classifier-free guidance for schnell | Saves ~2× compute (CFG doubles the batch) — correct because schnell is distilled |

## Config surface

Everything is env-var overridable (`SDCPP_BIN`, `SDCPP_MODEL_DIR`, `SDCPP_WIDTH/HEIGHT/STEPS/MAX_VRAM`, `SDCPP_BACKEND`) with sensible defaults, so the same code runs on the RTX 4070 desktop, on an AMD/ROCm machine, or even a Vulkan build (empty `SDCPP_BACKEND` omits the flag for newer sd.cpp builds where the backend is compiled in).

## Where it sits in FluxReel

```
Topic → LLM script → 5 scenes → [sdcpp] 5× sd-cli runs (serialized, Q4_0, 4 steps)
                                     → 5× 960×720 PNGs → title bars + captions
                                     → per-slide H.264 segments → concat → 15 s MP4
```

One honest trade-off worth noting: because each call spawns a fresh process (model load ~ every time) the per-image latency includes load overhead — that's the price of the zero-persistence simplicity, and it's why the lock only serializes the GPU, not the whole pipeline.

Want me to draft a slide (or 2–3 slides) for `submission/02_slides.md` specifically on this sd-cpp route — e.g. a "quantized fast path" architecture diagram plus a before/after latency table?
