---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Together AI: Tri Dao and Platform"
translated: false
type: note
---

**Question:** What is Together AI specifically about, and does Tri Dao work there?

**Answer:**

Yes — Tri Dao is a **Co-Founder & Chief Scientist** at Together AI, not just an employee. He's one of the five co-founders alongside Vipul Ved Prakash (CEO), Ce Zhang (CTO), Chris Ré, and Percy Liang — all heavy hitters from Stanford/CMU systems + ML research.

**What Together AI is:**

Together AI is a full-stack AI platform for production AI, powered by cutting-edge systems research — helping teams ship faster, scale reliably, and achieve superior unit economics. More concretely, it's three things:

1. **Inference API** — fast, cheap serving of open-source models (Llama, Qwen, Mistral, DeepSeek, etc.). Real-world benchmarks show 31% more TPS than TensorRT-LLM, 2× better TTFT at saturation, and 76% lower cost than Claude Opus 4.6.

2. **Fine-tuning platform** — managed fine-tuning on their GPU infra, recently upgraded with larger models and longer contexts.

3. **Systems research** — this is the differentiator. They published ATLAS (AdapTive-LeArning Speculator System), runtime-learning accelerators delivering up to 4x faster LLM inference, and do serious kernel-level work (Dan Fu is VP of Kernels).

**Tri Dao's specific role:**

He's also an Assistant Professor of Computer Science at Princeton, leading the Dao AI Lab, focused on hardware-aware algorithms and sequence models with long-range memory. His two defining works you should know:

- **FlashAttention / FlashAttention-2** — IO-aware exact attention, now standard in every serious training stack. FA-2 achieves 72% model FLOPs utilization on A100s and speeds up training by up to 4x vs the previous version.
- **Mamba** (with Albert Gu) — SSM-based alternative to Transformers, relevant to the "beyond Transformers" wave. Together has been publishing on StripedHyena and hybrid architectures building on this.

**Why it matters to you:**

Together AI is one of the best alternatives to OpenAI's API if you're building on open-source models — competitive pricing, FlashAttention-optimized serving, and real systems research behind it (not just reselling GPU time). Given you're already on OpenRouter + DeepSeek, Together is worth benchmarking for latency-sensitive workloads, especially for Llama/Qwen inference.

**References:**

- [Together AI - Tri Dao announcement + FA-2](https://www.together.ai/blog/tri-dao-flash-attention)
- [Tri Dao's homepage](https://tridao.me/tridao.github.io/)
- [Together AI About page](https://www.together.ai/about-us)
