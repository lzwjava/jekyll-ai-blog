---
audio: false
generated: true
image: false
lang: en
layout: post
title: No vLLM/SGLang on WX 9100
translated: false
type: note
---

Short answer: **No — not practically.** The WX 9100 (Vega 10, `gfx900`) is outside the supported hardware for both vLLM and SGLang, and this machine's ROCm 7.1 lacks the kernels they depend on.

## Evidence

**1. vLLM's official ROCm support list** (from upstream docs):
> GPU: MI200s (gfx90a), MI300 (gfx942), MI350 (gfx950), Radeon RX 7900 (gfx1100/1101), RX 9000 (gfx1200/1201), Ryzen AI MAX / AI 300 (gfx1151/1150)

`gfx900` is not on it. SGLang's ROCm path is likewise CDNA-only (MI210/250/300) plus RDNA3.

**2. rocBLAS on this box has no gfx900 kernels** — we already hit this exact wall with llama.cpp:
```
available TensileLibrary: gfx908, gfx90a, gfx942, gfx1030, gfx1100, gfx1101, gfx1151, gfx1200, gfx1201
```
No `gfx900`. vLLM/SGLang sit on PyTorch → hipBLAS/rocBLAS, so they'd fail the same way (or earlier).

**3. No PyTorch ROCm wheel for gfx900.** Official `torch` ROCm wheels don't include `gfx900`, so even plain PyTorch-on-GPU isn't available out of the box here (confirmed: no `torch` installed).

**4. No matrix cores.** MFMA (matrix engines) arrived with `gfx908`/CDNA1; WMMA with RDNA. Vega's GCN has **neither**, and vLLM/SGLang's paged-attention and GEMM kernels are written for those units. Even a source build wouldn't produce working kernels.

## What this means

| Option | WX 9100 (gfx900) |
|--------|------------------|
| llama.cpp (HIP, MMQ) | ✅ **already working** |
| Ollama | ✅ (it's llama.cpp under the hood) |
| vLLM | ❌ unsupported |
| SGLang | ❌ unsupported |
| PyTorch GPU (official wheels) | ❌ no gfx900 build |
| PyTorch built from source + old ROCm | ⚠️ possible but large effort, still no vLLM |

The good news: the `llama-server` you're already running **is** the vLLM-style serving path for this GPU — it gives you an OpenAI-compatible `/v1` API, the web UI, continuous batching (multiple slots), and 32K context. That covers the practical use case.

If you specifically need vLLM/SGLang (paged attention, very high concurrency, tensor parallel across many GPUs), you'd need to swap in a **CDNA card** — MI210/MI250 (gfx90a) or MI300 (gfx942). The MI25 you mentioned is also `gfx900`, so it would have the *same* limitation despite the "Instinct" name.