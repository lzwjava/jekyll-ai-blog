---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Incompatibility with sglang
translated: false
type: note
---

I cloned it, but I need to stop here and give you a straight answer before burning a 10–15 GB install that can't work.

## What I did
- ✅ Cloned to `~/projects/sglang` (via HTTPS — the `git@` SSH clone hung, likely no GitHub SSH key configured on that box).

## Verdict: sglang cannot run on this GPU

The card is a **Tesla M40 = Maxwell, compute capability 5.2**. sglang's install and runtime are hard-wired to much newer hardware:

| sglang requirement (from `python/pyproject.toml`) | Min. GPU it supports | M40 (sm_52) |
|---|---|---|
| `flashinfer_python[cu13]==0.7.0` | Ampere (sm_80+) | ❌ |
| `flash-attn-4>=4.0.0b18` | Ampere (sm_80+) | ❌ |
| `nvidia-cutlass-dsl[cu13]==4.8.0` | sm_80/90 targets | ❌ |
| Triton (transitive) | Volta+ (sm_70+, effectively sm_80+) | ❌ |
| `torch==2.13.0` (cu13) | sm_80-class builds | ❌/⚠️ |

The entire codebase and docs target **Hopper (sm_90) / Blackwell (sm_100/120)**; even Ampere is now "legacy" there. A Maxwell M40 is 3–4 generations behind the minimum.

On top of that:
- **M40 has no real FP16/BF16 throughput** (Maxwell does FP16 at ~1/64 rate). Modern LLM serving is FP16/BF16-based, so even a "fallback" would be absurdly slow.
- **12 GB VRAM** limits you to ~7B-4bit models even on compatible hardware.
- The box also has no sudo and only Python 3.14 (sglang/torch cu13 wheels target 3.10–3.13).

The burn test worked earlier because I compiled a plain FP32 sm_52 kernel via NVRTC — but sglang's fast kernels (FlashInfer/FA3/FA4/CUTLASS/Triton) have no sm_52 code paths at all. It would fail at the first kernel launch, guaranteed.

## Realistic options for this M40
1. **llama.cpp** — the only mainstream LLM runtime that still runs on Maxwell (its CUDA backend uses simple kernels + FP32/quantized fallbacks). I can set that up and actually serve a small model (e.g., Qwen2.5-1.5B/3B, Llama-3.2-3B) — slow but real.
2. **Use the M40 as FP32 compute** (like the burn test) — training/math workloads, not LLM serving.
3. If you want sglang specifically, it needs **any Ampere+ card** (RTX 3060 12GB or better is the cheapest realistic entry point).

Want me to (a) still attempt the full install anyway so you can see the failure yourself, or (b) pivot to llama.cpp and get an actual model serving on the M40?