---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma 4 on RTX 4070 in OpenClaw
translated: false
type: note
---

**Question:** How good is `gemma-4-26B-A4B-it-UD-IQ3_S.gguf` when used with llama.cpp on an RTX 4070 in OpenClaw (an AI agent framework)? What are the pros and cons?

---

**Answer:**

## Overview: What Is This Model?

`gemma-4-26B-A4B-it-UD-IQ3_S.gguf` refers to:

- **Gemma 4** — Google DeepMind's latest open model family, released April 2, 2026
- **26B-A4B** — A Mixture-of-Experts (MoE) model with 26 billion total parameters, but activating only 3.8 billion of its total parameters during inference to deliver fast tokens-per-second
- **UD** — "Unsloth Dynamic" quantization from Unsloth, which applies smarter per-layer quant strategies
- **IQ3_S** — An "importance matrix" quantization at ~3-bit. IQ-quants offer better performance for their size and work well on CUDA (Nvidia) — but they can be slower than K-quants on CPU, so speed vs. quality is a tradeoff

---

## RTX 4070 + IQ3_S: Will It Fit?

The RTX 4070 has **12 GB of VRAM**. Here's the situation:

- For the 26B A4B model, memory needs are roughly 10–14 GB depending on quantization. All expert weights must be loaded into VRAM; the efficiency gain of MoE is in compute, not storage.
- IQ3_S is one of the most aggressively compressed quantizations (~3.35 bits per weight). For a 26B total-parameter MoE, this should land roughly around **10–11 GB**, making it one of the few quantizations that can actually *fit fully in VRAM* on a 12 GB card.
- The 26B A4B model fits into 12–14 GB VRAM while delivering reasoning quality close to a 26B dense model, because only ~4B parameters are active during inference. It's the most efficient Gemma 4 option for users who want more than E4B but can't run 31B.

So IQ3_S on 12 GB is a tight but workable fit — and in fact the specific reason people choose this quant level.

---

## Gemma 4 in OpenClaw: Official Support

This combination is explicitly endorsed by NVIDIA. The Gemma 4 26B and 31B models are designed for high-performance reasoning and developer-centric workflows, making them well-suited for agentic AI. The latest Gemma 4 models are compatible with OpenClaw, allowing users to build capable local agents that draw context from personal files, applications, and workflows to automate tasks. NVIDIA has collaborated with Ollama and llama.cpp to provide the best local deployment experience.

On the agentic side, Gemma 4 includes native function calling, structured JSON output, multi-step planning, and configurable extended thinking/reasoning mode. It can also output bounding boxes for UI element detection — useful for browser automation and screen-parsing agents.

---

## Pros

**1. Fits a 12 GB GPU with IQ3_S quantization**
IQ3_S is aggressively compressed yet smarter than naive 3-bit. You get the 26B MoE onto an RTX 4070 where Q4 variants often won't fit cleanly.

**2. MoE architecture is fast despite large parameter count**
Only 3.8B parameters fire per forward pass, so it achieves roughly 97% of the dense 31B model's quality at a fraction of the compute. This matters greatly for agent workflows that generate many tokens.

**3. Excellent benchmark performance for the size**
Arena reports Gemma-4-26B-A4B at #6 among open models in the open leaderboard. This is exceptional for something running locally on consumer hardware.

**4. Native agentic features**
Gemma 4 natively supports structured tool use (function calling), reasoning on complex problem-solving tasks, code generation, and agents — making it well-suited for agentic AI like OpenClaw.

**5. Long context window**
Gemma 4's max context is 256K for the 26B A4B model. Even if you can't use the full window on 12 GB with IQ3_S, you still get a large and useful context compared to older models.

**6. Apache 2.0 license**
Fully free for commercial use, modification, and redistribution — no usage caps or licensing friction.

**7. Confirmed working on 12 GB cards with similar quants**
A real-world test on a 12 GB card using UD-Q5_K_XL showed: prompt processing at ~1466 tok/s and text generation at ~47 tok/s — fast enough for daily interactive use, viable 128K text serving, and working vision inference. IQ3_S will be even lighter, likely maintaining or improving these speeds.

---

## Cons

**1. IQ3_S quality loss is real**
3-bit quantization is a significant compression. Compared to Q4_K_M or Q5_K_M, you will notice degraded coherence on complex reasoning, math, and nuanced instructions. The UD (dynamic) quant strategy mitigates this somewhat, but it is not a free lunch.

**2. Tight VRAM leaves little room for long contexts**
With only ~1–2 GB headroom after loading the model, your KV cache budget is constrained. Longer contexts consume additional VRAM for the KV cache — if you plan to use long context windows for RAG pipelines or document analysis, you need 20–30% headroom above base model requirements. On 12 GB with IQ3_S, long contexts will push you into CPU offload territory, slowing things down significantly.

**3. Slower than Qwen 3.5 35B-A3B for equivalent hardware**
Multiple community users report that Gemma 4's MoE runs significantly slower than Qwen 3.5's equivalent on the same hardware, with one user reporting 11 tokens/sec on Gemma 4 26B-A4B vs 60+ tokens/sec on Qwen 3.5 35B-A3B on the same GPU. If raw speed is your top priority, Qwen 3.5 35B-A3B may be worth comparing.

**4. VRAM-hungry KV cache for Gemma 4 compared to competitors**
Community notes indicate Gemma 4 uses more VRAM for context at the same quantization level compared to Qwen 3.5, with one user noting they could only fit Gemma 3 27B Q4 with 20K context on a 5090, while Qwen 3.5 27B Q4 fit with 190K context on the same card.

**5. New model, still maturing in ecosystem**
Early community reports include Mac hard crashes when loading in LM Studio, some jailbreak issues with basic system prompts, and occasional infinite loops in vision tasks — though these may be resolved with updates. As of early April 2026, the tooling is still catching up.

---

## Verdict

Yes, it's quite good for what it is. The `IQ3_S` quant is the **right choice specifically for RTX 4070 (12 GB)** because it's the only way to run this quality of model fully in VRAM. The MoE architecture means compute is efficient even though all weights are in memory. For OpenClaw agentic use — function calling, tool use, code generation — Gemma 4 26B-A4B is natively designed for it and officially supported.

However, manage expectations: IQ3_S has real quality degradation compared to Q4+, context length is constrained by tight VRAM, and Qwen 3.5 35B-A3B may outperform it in speed benchmarks on the same hardware. If you have a 16 GB card (RTX 4070 Ti Super / 4080), consider upgrading to Q4_K_M or Q5_K_M for a noticeably better experience.

---

**References:**

- [NVIDIA RTX AI Garage — Gemma 4](https://blogs.nvidia.com/blog/rtx-ai-garage-open-models-google-gemma-4/)
- [Gemma 4 Hardware Requirements Guide (Avenchat)](https://avenchat.com/blog/gemma-4-hardware-requirements)
- [Running Gemma 4 26B-A4B Locally on 12GB VRAM](https://carteakey.dev/blog/running-gemma-4-26b-a4b-locally/)
- [Unsloth Gemma 4 Local Inference Guide](https://unsloth.ai/docs/models/gemma-4)
- [Gemma 4 After 24 Hours — Community Findings](https://dev.to/dentity007/-gemma-4-after-24-hours-what-the-community-found-vs-what-google-promised-3a2f)
- [WaveSpeed — What Is Gemma 4?](https://wavespeed.ai/blog/posts/what-is-google-gemma-4/)
- [GGUF Quantization Overview (GitHub)](https://gist.github.com/Artefact2/b5f810600771265fc1e39442288e8ec9)