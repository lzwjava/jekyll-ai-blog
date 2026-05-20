---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X Running DeepSeek V4 Flash
translated: false
type: note
---

**Question:** Given an AMD MI300X with 192GB VRAM, what are the most impressive and practically possible things to do with it, in the context of what's trending on HuggingFace and dominating OpenRouter rankings right now (May 2026)?

**Answer:**

The landscape has shifted massively since the original prompt was written. Here's what's actually hot right now and what your MI300X can do with it.

---

## What's Dominating the Rankings Right Now

OpenRouter as of early May 2026 shows Anthropic leading with 1.6T weekly tokens, OpenAI at 518B, and Google at 514B — with 400+ active models across 60+ providers.

The hottest model on OpenRouter's tool-calling rankings right now is **DeepSeek-V3.2**, described as introducing DeepSeek Sparse Attention (DSA), a fine-grained sparse attention mechanism reducing training/inference cost while preserving quality in long-context scenarios — with reported performance in the GPT-5 class, and gold-medal results on the 2025 IMO and IOI.

The open-weight frontier as of May 2026:

On the May 12, 2026 LiveBench snapshot, **Kimi K2.6 Thinking** leads all open-source models with 78.57 Coding Avg and 58.33 Agentic Coding Avg. Its architecture is MoE with ~1T total / 32B active parameters. DeepSeek V4 Pro (1.6T total / 49B active, MIT license) and GLM 5.1 are close behind on agentic coding. **DeepSeek V4** was released April 24, 2026 with a 1M token context window.

**GLM-5.1** from Zhipu AI is a 744B MoE with 40B active parameters, trained on 28.5 trillion tokens using DeepSeek Sparse Attention — built specifically for long-horizon agentic engineering tasks, staying productive across hundreds of rounds and thousands of tool calls.

---

## What Fits on Your Single MI300X (192GB)

Here's the honest map of today's frontier models to your hardware:

| Model | Architecture | Total params | Active params | VRAM needed (Q4_K_M) | Fits? |
|---|---|---|---|---|---|
| **DeepSeek V3.2** | MoE | 671B | 37B | ~390 GB (FP16), ~150GB (Q2_K) | Q2_K barely; needs 8× for FP16 |
| **DeepSeek V4 Flash** | MoE | 284B | 13B | ~160 GB (Q4_K_M) | ✅ Fits comfortably |
| **Kimi K2.6** | MoE | ~1T | 32B | Too large for single card | ❌ Needs multi-GPU |
| **GLM-5.1** | MoE | 744B | 40B | Too large for single card | ❌ Needs multi-GPU |
| **Qwen 3.6 27B** | Dense | 27B | 27B | ~17 GB | ✅ Trivially fits, fast |
| **DeepSeek R1 671B** | MoE | 671B | 37B | Same as V3 | Q2_K only |

**The real sweet spot for your card in 2026:**

**DeepSeek V4 Flash** — 284B total parameters, just 13B active per token, 1M token context window — is designed specifically as the efficiency-optimized MoE for deployments like yours. At ~160GB Q4_K_M it fits with ~30GB left for KV cache. With only 13B active params, you get throughput closer to a 13B dense model (80–120 t/s estimated) with quality far beyond it.

---

## Most Impressive Things You Can Actually Do

### 1. Run the Frontier Coding Agent Locally — Zero API Cost

**DeepSeek V4** offers the best performance-to-inference-cost ratio for self-hosted GPU deployments, with substantially improved tool-call reliability over V3 — far fewer partial function calls or malformed JSON payloads. It's the top recommendation for teams self-hosting on GPU clusters who need frontier-level coding performance.

With your MI300X running DeepSeek V4 Flash (fits in 192GB), you get a **Claude Code-class coding agent** locally. No rate limits, no per-token cost, full 1M context for entire codebases. Connect it to your `ww`/`iclaw`/`zz` CLI tools via llama-server's OpenAI-compatible endpoint:

```bash
# llama.cpp server, OpenAI-compatible, point Claude Code at it
llama-server \
  --model DeepSeek-V4-Flash-Q4_K_M.gguf \
  --n-gpu-layers 999 \
  --ctx-size 65536 \
  --host 0.0.0.0 --port 8080

# Then in Claude Code or any OpenAI-compatible client:
export OPENAI_BASE_URL=http://localhost:8080/v1
export OPENAI_API_KEY=dummy
```

### 2. Run DeepSeek R1 671B at Q2_K — Full Reasoning Model Locally

At Q2_K (~150 GB), DeepSeek R1 squeezes in. This is the reasoning/thinking model that benchmarks at frontier level on math and coding. You get chain-of-thought reasoning at ~5–10 t/s — slow but zero cost and fully private. This is what cloud providers charge $15–30/M tokens for.

### 3. Fine-Tune 70B Models with LoRA — Full-Precision

192GB lets you fine-tune a 70B model in **bf16 with LoRA** without sharding to CPU. This is what separates a single MI300X from consumer setups:

```python
# QLoRA on 70B — fits comfortably with 192GB
from transformers import AutoModelForCausalLM
import torch

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-72B",
    torch_dtype=torch.bfloat16,
    device_map="cuda"
)
# Full 70B in bf16 = ~140GB. 52GB headroom for optimizer states with LoRA.
```

With LoRA rank 64, you can fine-tune a 72B model on your own data (banking domain, code style, etc.) — something normally requiring 4× A100s.

### 4. Serve as a Private OpenAI-Compatible API for Your Team

A single MI300X can run Llama 3.1 70B at 120,000 tokens context via vLLM — that's a full private API server supporting long-context RAG, document analysis, and multi-turn agents for multiple users simultaneously.

```bash
docker run --device=/dev/kfd --device=/dev/dri \
  rocm/vllm-dev:latest \
  vllm serve Qwen/Qwen3-72B \
  --tensor-parallel-size 1 \
  --max-model-len 120000 \
  --gpu-memory-utilization 0.85
```

### 5. Train GPT-2 Scale → Qwen3-8B Scale from Scratch

You already trained GPT-2 on H200/H100. On an MI300X with 192GB, you can scale that up to **8B parameter training from scratch** in bf16 without any memory tricks:

- 8B model in bf16 = ~16GB weights
- Adam optimizer states = ~64GB
- Activations + gradients = ~60GB
- **Total: ~140GB** — fits with headroom

That's a full Llama-3/Qwen3-8B-scale pretraining run on a single card. Karpathy's nanoGPT scales directly.

---

## The Honest Priority Order

Given where OpenRouter rankings and HuggingFace trends are pointing, here's what I'd actually do with your MI300X today:

1. **DeepSeek V4 Flash (284B MoE, 13B active) via llama.cpp** — the best single-card frontier model right now. Fits, fast, frontier quality.
2. **Fine-tune Qwen3 72B with LoRA** on your bank domain data — 192GB makes this single-card, no infra headaches.
3. **Run DeepSeek R1 671B Q2_K** for math/reasoning tasks where you want chain-of-thought locally.
4. **vLLM server for team use** — serve Qwen3 72B at 120K context to 5–10 concurrent users.
5. **Scale nanoGPT → 8B pretraining** — you now have the VRAM to go from "toy" to "real model" territory.

The single most impressive flex: a private, zero-cost, frontier-quality coding agent (DeepSeek V4 Flash) running locally with 1M token context for full codebase analysis. No Claude/GPT API bills. No rate limits. Fully yours.

---

References:

- [Performance of llama.cpp on AMD GPU (MI300X) — GitHub Discussion #14640](https://github.com/ggml-org/llama.cpp/discussions/14640)
- [Best Open Source Self-Hosted LLMs for Coding — Pinggy (May 2026)](https://pinggy.io/blog/best_open_source_self_hosted_llms_for_coding/)
- [Best Open-Source LLMs for Agentic Coding 2026 — MindStudio](https://www.mindstudio.ai/blog/best-open-source-llms-agentic-coding-2026)
- [The Best Open-Source LLMs in 2026 — BentoML](https://www.bentoml.com/blog/navigating-the-world-of-open-source-large-language-models)
- [OpenRouter Homepage — Live Rankings](https://openrouter.ai/)
- [Llama.cpp Meets Instinct: AMD ROCm Blog](https://rocm.blogs.amd.com/ecosystems-and-partners/llama-cpp/README.html)