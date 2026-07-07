---
audio: false
generated: true
image: false
lang: en
layout: post
title: Server Status and Limitations
translated: false
type: note
---

## Comprehensive Status

### Server Hardware

| Resource | Spec | Constraint |
|----------|------|------------|
| **GPU** | RTX 2000 Ada, 16 GB VRAM, CC 8.9 | Runs models up to 7-8B FP16 or 30B-34B INT4 |
| **CPU** | AMD EPYC 7443, 48 threads | Fine |
| **RAM** | 251 GB | Fine |
| **/dev/shm** | 14 GB tmpfs | Limited — filled up during model download |
| **/workspace** | 2.1 PB MooseFS FUSE | **~10 GB quota** — the bottleneck |

### Installed Software

| Component | Version | Status |
|-----------|---------|--------|
| **SGLang** | 0.5.14 | ✅ Installed, supports `gemma4_causal` |
| **SGLang kernel** | 0.4.4 | ✅ Working (needs `LD_LIBRARY_PATH` for CUDA 13 libs) |
| **Python** | 3.11.10 | ✅ |
| **CUDA** | 12.4 (driver 580 — CUDA 13.0) | ✅ |
| **Node.js** | 22.23.1 | ✅ Installed |
| **MongoDB** | 7.0.37 | ✅ Running on port 27017 |
| **LibreChat** | latest | ✅ Cloned to `/workspace/LibreChat/` |

### Model Download Status: Gemma 4 26B A4B AWQ (cyankiwi)

| Shard | Size | Status |
|-------|------|--------|
| `model-00001-of-00004.safetensors` | 5.1 GB | ✅ Complete |
| `model-00002-of-00004.safetensors` | 2.1 / 5.1 GB | ❌ Partial |
| `model-00003-of-00004.safetensors` | 1.5 / 5.1 GB | ❌ Partial |
| `model-00004-of-00004.safetensors` | 0 / 1 GB | ❌ Missing |

**Total model size: ~20 GB. Workspace quota: ~10 GB.** — Incompatible.

### The Real Limitation

The RunPod network volume (`/workspace`) has a **per-pod quota of ~10 GB**. This is enforced by the MooseFS FUSE server, not the filesystem itself (which reports 328 TB free). Once writes accumulate past ~10 GB, all new writes fail with `EDQUOT (Disk quota exceeded)`. This is a **server-side quota** — I can't override it from the pod.

Cleaning up old files (SEC-EDGAR-GPT model, pip caches, llama.cpp artifacts) freed enough space for partial downloads, but the full 20 GB model simply won't fit.

### What Works

**Two approaches that work right now:**

1. **Serve a smaller AWQ model** — Fits in the 10 GB quota. Examples:
   - `Qwen2.5-7B-Instruct-AWQ` (~4 GB) — good quality, lots of headroom
   - `Qwen2.5-14B-Instruct-AWQ` (~8 GB) — better quality, tight fit
   - Supports 128K context, strong coding, reasoning

2. **Increase the volume quota** — If you bump it to 20+ GB in RunPod dashboard, I can re-download Gemma 4 26B A4B AWQ cleanly and serve it.

### What's Left to Do After Model is Ready

Regardless of model choice, the remaining setup is:
1. **Start SGLang server** — serving the model on port 30000 with OpenAI-compatible API
2. **Configure LibreChat** — write `.env` file with `MONGO_URI` and `librechat.yaml` pointing to the SGLang endpoint as a custom OpenAI provider
3. **Build LibreChat** — `npm run frontend`
4. **Start LibreChat** — `npm run backend`
5. **Access** — LibreChat on port 3080, configured to use the local SGLang model

Which path? Option 1 (smaller model now) or option 2 (increase quota for Gemma 4)?
