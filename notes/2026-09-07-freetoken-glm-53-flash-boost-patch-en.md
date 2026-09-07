---
audio: false
generated: true
image: false
lang: en
layout: post
title: FreeToken GLM-5.3-Flash Boost Patch
translated: false
type: note
---

This is **freetoken-ox-boost** — a patch/plugin repository for [FreeToken](https://github.com/FlashML-org/FreeToken) v0.1.2, an inference server. It contains no upstream code, only patches and new files.

**What it does:** It adds GLM-5.3-Flash (MoE, NVFP4) support and a set of performance optimizations for running the model on a **single RTX PRO 6000 Blackwell 96 GB GPU** with expert weights offloaded to host memory over PCIe Gen5.

**Headline results:**
- Single-stream decode: **17.8 → 36.7 tok/s (~2×)** with zero quality loss (bit-exact vs HF reference, 48/48 steps)
- MoE expert cache hit rate ~84%, TTFT 0.59 s for small prompts, ~1030 tok/s prefill at 232K context
- Concurrency doesn't scale well (~49 tok/s aggregate at 4-way) because GLM-5.3-Flash's routing is very flat — concurrent requests can't share expert fetches, so PCIe bandwidth is the bottleneck

**Notable features:**
- **Vision support** (image + video input) via the checkpoint's 0.6B ViT tower, on OpenAI/Anthropic-style endpoints
- **Prefix caching** for media requests using pixel-content hashes in the radix cache key
- A documented **hybrid radix-cache corruption bug** that was root-caused (missing KDA track-snapshot write causing ~10% corrupted cache hits) and fixed with a recompute-based writer plus defenses

**Layout:**
- `patches/` — 53 per-file unified diffs against FreeToken v0.1.2
- `overlay/` — 19 new files (GLM-5.3-Flash model code, vision, 4 Triton kernels, prefetch/LFU cache)
- `install.sh` — version check → dry-run → apply → compile
- `examples/` — production launch script
- `MANIFEST.md` — feature → files → switches → measured numbers map

Licensed Apache-2.0, same as upstream.
