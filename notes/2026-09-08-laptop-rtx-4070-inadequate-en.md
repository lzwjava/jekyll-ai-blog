---
audio: false
generated: true
image: false
lang: en
layout: post
title: Laptop RTX 4070 Inadequate
translated: false
type: note
---

Short answer: **not for these models, not realistically.** This repo is dimensioned for a 96 GB Blackwell card + 130–160 GB of host RAM. A laptop RTX 4070 (8 GB VRAM) is off by roughly an order of magnitude on every resource that actually matters here. Let me explain why with the project's own numbers, then give you options that actually work on a laptop.

## Why it won't run on an RTX 4070 laptop

Look at what this project *assumes* (from `README.md`, `MANIFEST.md`, and the serve scripts):

| Resource | What the repo needs | RTX 4070 laptop |
|---|---|---|
| VRAM | 96 GB (RTX PRO 6000); dense weights alone ~17 GB, 8 resident expert layers = ~31 GB, KV pool up to 262K+ tokens | **8 GB** |
| Host RAM | 129–137 GB of *pinned* banks, preflight requires 138–145 GB `MemAvailable` (`serve_full.sh`, `serve_dsv4.sh` both `FATAL` below that) | 16–64 GB typical |
| Checkpoint on disk | GLM-5.3-Flash-NVFP4 ≈ **181 GB of experts** + ~17 GB dense; DSV4 similar | no laptop disk/RAM |
| PCIe | Gen5 x16 ~50 GB/s (they bill *bytes*) | Gen4, ~14–30 GB/s effective |
| Tensor cores | Blackwell `fp4` (NVFP4 / ds_fp4 experts are 4-bit: packed uint8, 2 values/byte — see `experts_resident.py` shapes) | Ada has FP8 but **no FP4 MMA** (FP4 needs sm_100/120) |

The knock-on effects:

1. **The checkpoint doesn't even fit in laptop RAM.** You can't "adjust" your way out of 181 GB of expert weights when your machine has 16–64 GB of RAM and an 8 GB card. Host-pinning 129 GB is impossible.
2. **Even the non-expert weights don't fit in VRAM.** ~17 GB BF16 (≈ 8.5–9 GB FP8) > 8 GB. So unlike the repo's design — where dense weights + hot expert layers live on the GPU and only cold experts cross PCIe — *everything* would have to stream from host per token.
3. **The cache hit rate collapses, which is what the whole design depends on.** They reach ~84% hit rate with thousands of cache slots + resident layers on 96 GB. On 8 GB you'd have almost no slots, so nearly every token pays the full cold fetch. Cold bytes are roughly: top-8 of 288 experts × ~37 offload layers ≈ **~4 GB per token**. Even at desktop-grade PCIe that's seconds per token; on laptop Gen4 with no resident layers, you're at well under 1–2 tok/s. Worse than useless.
4. **The expert kernels are Blackwell FP4.** The NVFP4/ds_fp4 inline-dequant Triton kernels assume FP4 tensor cores. Ada can't run them natively — you'd need to dequantize to FP8/BF16 (not in these kernel sets), and that *doubles* the bytes you're already starving for.
5. **The tuned numbers (36–64 tok/s) are a *result* of the machine, not the code.** The entire optimization story — resident layers, speculative prefetch, on-demand prefill, concurrency analysis — is about saturating a Gen5 PCIe link. A laptop changes the physics, not just the config.

So: this is not a "change `--memory-ratio`" situation. All three resources (VRAM, RAM, bandwidth, plus FP4 hardware) are hard walls.

## What you *can* do

**A. If your goal is actually chatting/coding on the laptop — use the right-sized tool.**
The same core idea (keep hot MoE experts in VRAM, stream the rest from RAM) is exactly what **llama.cpp / Ollama** do, and they're tuned for your memory envelope:
- Fully-in-VRAM: a 7–9B dense model at Q4 (Llama-3.1-8B, Qwen2.5-7B/14B at low quant, DeepSeek-R1-Distill-* ) → 30–100+ tok/s on an 8 GB card.
- VRAM+RAM split MoE (closest spirit to this repo): Qwen3-30B-A3B / Qwen3-14B-A3B class at Q4 — tiny active params (3B), most experts stay in RAM, few GB fetch per token. Fast and feels like a frontier model.
That gives you the "expert offload" experience at laptop scale with sane speed.

**B. If your goal is to learn this repo's engine/kernels — you can smoke-test it.**
The code has dev caps exactly for exercising the path without the full beast:
- `FREETOKEN_GLM5_MAX_LAYERS` (e.g. `=5`: 3 dense + 2 MoE) skips pinning the 163 GB of experts.
- No resident layers, tiny `--kv-reserve-tokens`, and don't set host-bank pin budgets.
You can apply `install.sh` to a FreeToken v0.1.2 tree and boot on the 4070 to trace the decode path, watch the Triton kernels, study the offload cache — but treat it as a lab, not serving. Caveats: the repo targets CUDA 13 / Blackwell; your laptop will be on CUDA 12.x-era drivers, and the FP4 kernels have no Ada path, so stick to the smoke-test layers or expect kernel-level surgery. A lot of the Triton work (fused route, mHC norm, KDA gate, LFU cache kernel, radix-cache fixes) is pure PyTorch/Triton and would compile on Ada — but only for a model that fits.

**C. If your goal is these specific frontier models — get the machine they need.**
The cheapest honest path is renting (RunPod/Vast/cloud) a 96–192 GB GPU, or building a desktop with ≥ 160 GB RAM + a big card. The project is built around PCIe-byte billing; no laptop adjustment changes that.

**Bottom line:** the *ideas* in this repo are portable, but the *models and configuration* are not. For an 8 GB laptop, run a Qwen3-A3B-class MoE or a 7–9B dense model through llama.cpp/Ollama — that's the laptop-scale version of this project's philosophy, and it will actually be fast. Use this repo as a study reference, or revisit it when you have 100+ GB of host RAM and a GPU with the VRAM to match.