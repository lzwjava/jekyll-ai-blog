---
audio: false
generated: true
image: false
lang: en
layout: post
title: vLLM cannot run on M40
translated: false
type: note
---

**No — vLLM cannot run on `.137`'s M40.** Official vLLM docs set the floor at:

> **GPU: compute capability 7.5 or higher (e.g., T4, RTX 20xx, A100, L4, H100, B200)**

The Tesla M40 is **compute capability 5.2 (Maxwell, 2015)** — two full generations below vLLM's minimum (it doesn't even reach the "7.0" cut they use for Volta-era cards; Maxwell/Pascal aren't on their supported table at all).

It fails on the same walls we've already hit empirically:

1. **GPU kernels** — vLLM's tensor-parallel/quant/attention kernels are compiled for SM 7.5+; none exist for 5.2. No code path can even execute.
2. **Software stack** — vLLM runs on modern torch (cu12x/cu130). We proved on the twin box (`.34`) that *any* torch CUDA init hangs the driver for this GPU (`nvidia_uvm` D-state wedge → reboot). `.137`'s driver 550 = CUDA 12.4 (≥12 = Maxwell kernels removed).
3. **fp16/bf16** — vLLM pipeline assumes half precision; M40 has **no native fp16/bf16**.

## What *can* actually serve LLMs on `.137` (realistic options)

| Option | How | Feasibility |
| --- | --- | --- |
| **llama.cpp / Ollama — CPU only** | GGUF quantized models, no GPU touch | ✅ **Zero risk, works today** — but 7.7 GB RAM limits to small models (Qwen2.5-3B/4B, Llama-3.2-3B, Gemma-2-2B at Q4 ≈ 2–3 GB), ~4–8 tok/s on the 4-core i5 |
| **llama.cpp — CUDA on the M40** | much more tolerant of old archs than vLLM | ⚠️ Unknown — the one risk-free way isn't; legacy CUDA on driver 550 *might* not wedge (device hits UVM differently), but expect a **1 reboot cost** if it does |
| vLLM | — | ❌ Never |

Want me to set up **llama.cpp + a small GGUF model with an OpenAI-compatible API server** on `.137` right now (CPU mode — no risk to the box)? It would give you a working inference endpoint on the LAN today.
