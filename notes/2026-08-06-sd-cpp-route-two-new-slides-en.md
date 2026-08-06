---
audio: false
generated: true
image: false
lang: en
layout: post
title: "sd-cpp Route: Two New Slides"
translated: false
type: note
---

Done. Summary of what changed in `submission/02_slides.md`:

**New slides added (after Pipeline Overview):**

1. **"The sd-cpp Route — Quantized Fast Path"** (slide 4)
   - Native C++ `sd-cli` engine, no torch/diffusers in the loop
   - The 4-component FLUX load (Q4_0 transformer + VAE on GPU, CLIP-L/T5-XXL text encoders on CPU)
   - Fresh-process-per-image design, GPU-serializing mutex, backend-agnostic `ImageProvider` API

2. **"sd-cpp Optimizations"** (slide 5)
   - The win-per-flag table: Q4_0 (→ ~8.75 GB/run on 12 GB), 4-step distilled, `--vae-tiling`, `--max-vram 10`, backend offload, `--cfg-scale 1.0`, 4:3 960×720, fixed seed
   - Honest trade-off callout: model-load cost per image in exchange for zero memory growth / crash isolation

**Small tweaks to existing slides:**

- Pipeline diagram: `Q4_0 GGUF (4-bit)` → `Q4_0 GGUF · sd-cpp`
- Model Strategy table: Q4_0 row now says "**4-bit GGUF** via **sd-cpp**"
- AMD Optimizations slide: added pointer `> Items 1–5 are realized by the sd-cpp route — see the deep dive above.`
- Demo Flow step 7: "Quantized Q4_0 **sd-cpp** path + measured latency"

Deck is now 11 slides: cover → problem → pipeline → **sd-cpp deep dive ×2** → capabilities → model strategy → AMD optimizations → demo → results → thanks. Render check with marp: `npx @marp-team/marp-cli submission/02_slides.md` if you want a preview.
