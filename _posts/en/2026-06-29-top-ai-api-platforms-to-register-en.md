---
audio: false
generated: true
image: false
lang: en
layout: post
title: Top AI API Platforms to Register
translated: false
type: note
---

Question: Which other AI/LLM API platforms (similar to Together.ai, OpenRouter, Jina AI) are worth registering for?

Answer:

Here's a curated list beyond the three you have, grouped by what they're actually good for. Skip the ones that overlap with what you already run.

**Inference aggregators / multi-model gateways (OpenRouter-class)**
- **Fireworks.ai** — fast serverless inference, strong on open models + function calling, FireAttention kernels. Good Together alternative.
- **DeepInfra** — cheap per-token open-model hosting, often undercuts Together/Fireworks.
- **Novita.ai** — cheap inference + GPU rental, decent for batch.
- **Hyperbolic** — cheap open-weight inference + on-demand GPUs (H100/MI300X spot), aligns with your training work.
- **Groq** — LPU inference, absurd tokens/sec for Llama/Qwen/Kimi. Worth it just for latency experiments.
- **Cerebras** — wafer-scale inference, even faster than Groq on some models. Free tier exists.

**Frontier labs (direct, for eval/agent work)**
- **DeepSeek** (platform.deepseek.com) — you're already DeepSeek-heavy; the direct API is cheaper than reselling and gets v4 first.
- **Moonshot / Kimi** (platform.moonshot.cn) — Kimi K2 is a strong agentic/coding model, cheap.
- **Z.ai / Zhipu GLM** — GLM-4.6 is a serious coding model, OpenRouter-priced but direct is cheaper.
- **Mistral** (la Plateforme) — for Codestral, embeddings, and EU-hosted needs.
- **xAI** (Grok API) — if you want Grok in your agent rotation.

**GPU rental (training, MI300X/4070 overflow)**
- **RunPod** — serverless + pods, community cloud is cheap. Best Together-tier GPU rental.
- **Vast.ai** — spot-market GPUs, cheapest H100/4090 if you tolerate variance.
- **Lambda** — clean H100/B200 on-demand, good for multi-GPU training runs.
- **Modal** — serverless Python, great for your CLI-agent/training-script style (decorate a function, run on H100).
- **Prime Intellect** — aggregated GPU marketplace, decentralized training focus, fits your nanoGPT/MoE interests.

**Embeddings / retrieval / reranking (Jina-class)**
- **Voyage AI** (now Anthropic-owned) — best-in-class retrieval embeddings + rerankers.
- **Cohere** — Embed v3 + Rerank, strong for RAG eval.
- **Nomic** — open embeddings + Atlas for dataset viz, fits your dataset-engineering work.

**Tooling-adjacent (worth an account)**
- **Replicate** — run/fine-tune any open model via API, good for one-off experiments.
- **Baseten** — Truss-based model deployment, if you want to serve your own GPT-2/finetune.
- **Fal.ai** — fast media/diffusion inference if you ever touch image/audio.

If I had to pick the highest-leverage five for your trajectory: **Groq** (latency), **DeepInfra** or **Hyperbolic** (cheap tokens), **RunPod** + **Modal** (training/serving), **Voyage** (embeddings). The rest are situational.

Want me to write a small Python script that benchmarks the same prompt across OpenRouter + Together + Groq + DeepInfra (tokens/sec, TTFT, cost/1M) so you can rank them empirically rather than from a list?
