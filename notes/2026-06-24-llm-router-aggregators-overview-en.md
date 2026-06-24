---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Router Aggregators Overview
translated: false
type: note
---

**Question:** What are the major LLM API routers/aggregators besides OpenRouter?

**Answer:**

Here are the main ones worth knowing:

## Tier 1 — Full Aggregators (multi-provider routing)

| Service | Models | Key Feature |
|---|---|---|
| [OpenRouter](https://openrouter.ai) | 300+ | Best coverage, fallback routing, usage analytics |
| [Together AI](https://together.ai) | 100+ | Good for open-source, fast inference, fine-tuning |
| [Fireworks AI](https://fireworks.ai) | 50+ | Fast inference, function calling, JSON mode |
| [Replicate](https://replicate.com) | 1000s | Any model via Docker, good for image/audio too |
| [Groq](https://groq.com) | ~20 | Extremely fast (LPU chip), Llama/Mixtral |
| [Cerebras](https://cerebras.ai) | ~5 | Fastest inference (~2000 tok/s), Llama 3.3 |

## Tier 2 — Focused Routers

| Service | Specialty |
|---|---|
| [Hugging Face Inference API](https://huggingface.co/inference-api) | Any HF model, serverless |
| [Novita AI](https://novita.ai) | Cheap open-source models |
| [DeepInfra](https://deepinfra.com) | Competitive pricing on open models |
| [Perplexity API](https://docs.perplexity.ai) | Search-augmented models |
| [Mistral API](https://mistral.ai) | Official Mistral, good EU option |

## Tier 3 — Enterprise / Self-hosted Routers

| Service | Use Case |
|---|---|
| [LiteLLM](https://github.com/BerriAI/litellm) | Self-hosted proxy, 100+ providers, OpenAI-compatible |
| [PortKey](https://portkey.ai) | Observability + routing + guardrails |
| [Helicone](https://helicone.ai) | Proxy with logging, rate limiting, caching |
| [Martian](https://withmartian.com) | Intelligent model routing by cost/quality |

## For Your Setup Specifically

Given you use OpenRouter heavily and build CLI agents:

**LiteLLM** is the most useful one to self-host — single OpenAI-compatible endpoint, routes to any provider:

```python
pip install litellm

# litellm --model openrouter/deepseek/deepseek-chat
# or in code:
from litellm import completion
response = completion(
    model="openrouter/deepseek/deepseek-r1",
    messages=[{"role": "user", "content": "hi"}],
    api_key="<API_KEY>"
)
```

**PortKey** if you want observability across your 2B token/month consumption — it logs, traces, and caches across providers.

## Pricing Comparison for DeepSeek V3 (your primary model)

| Router | Input ($/1M) | Notes |
|---|---|---|
| OpenRouter | ~$0.27 | With caching discounts |
| Together AI | ~$0.30 | |
| Fireworks | ~$0.27 | |
| DeepInfra | ~$0.28 | |
| Official API | ~$0.27 | api.deepseek.com direct |

For your use case (high volume, CLI agents, DeepSeek-heavy), I'd recommend:

- **Primary**: OpenRouter (coverage + fallback)
- **Fast inference**: Cerebras or Groq for latency-sensitive tasks
- **Self-hosted proxy**: LiteLLM to unify them all behind one endpoint
