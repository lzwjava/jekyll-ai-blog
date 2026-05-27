---
audio: false
generated: true
image: false
lang: en
layout: post
title: Xiaomi MiMo Price Cut Technical Optimizations
translated: false
type: note
---

**Question:** What is this Xiaomi MiMo announcement saying, and what are the key technical optimizations behind the price reduction?

**Answer:**

## Summary

Xiaomi just sent a developer newsletter announcing **massive price cuts** for their MiMo-V2.5 reasoning model API, effective today (2026-05-27 Beijing time). The headline: **up to 99% price reduction**.

---

## Pricing Breakdown

| Model | Cache Hit Input | Cache Miss Input | Output |
|-------|----------------|-----------------|--------|
| MiMo-V2.5-Pro | ¥0.025/M tokens | ¥3/M tokens | ¥6/M tokens |
| MiMo-V2.5 | ¥0.02/M tokens | ¥1/M tokens | ¥2/M tokens |
| MiMo-V2.5-TTS | Free (limited time) | — | — |

Compare: MiMo-V2.5 output at ¥2/M ≈ **$0.28/M tokens** — cheaper than GPT-4o-mini output ($0.60/M), aggressive pricing in the Chinese LLM API market.

The huge spread between cache-hit (¥0.02) vs cache-miss (¥1) input pricing incentivizes you to structure prompts with long stable system prompts to maximize cache hits — same pattern as Anthropic's prompt caching.

---

## The Technical Story (Most Interesting Part)

The price cut is backed by real engineering. Let me break down what they actually did:

### 1. SGLang + HiCache with Sliding Window Attention (SWA)

**SWA** (used in Mistral-style architectures) means each token only attends to a fixed window of recent tokens, not the full context. This limits KV cache size per layer:

```
Standard attention: KV cache grows as O(seq_len × d_model) per layer
SWA: KV cache capped at O(window_size × d_model) per layer
```

**HiCache** is SGLang's hierarchical KV cache system — it tiered storage across:
- GPU HBM (fast, expensive, small)
- CPU RAM (slower, cheap, large)
- SSD (slowest, very cheap, very large)

Their claim: **data movement reduced to 1/7 of before**, **cacheable tokens increased 5x**. This is the core reason cache-hit pricing is 50x cheaper than cache-miss — serving a cached token is nearly free.

### 2. Expert Parallelism Optimization

MiMo is a **MoE (Mixture of Experts)** model (based on their architecture). Expert parallelism means different GPUs handle different experts. The optimization likely involves:
- Better load balancing across experts
- Reducing expert routing communication overhead
- Possibly fused dispatch/combine kernels

### 3. Input Length Bucketing

Instead of padding every sequence to max length, they bucket inputs by length range:

```python
# Conceptually:
buckets = [512, 1024, 2048, 4096, 8192]
# Batch requests within same bucket → less padding waste → higher GPU utilization
```

This improves **throughput per GPU**, directly reducing cost per token.

---

## Token Plan Reset (Business Side)

Existing paid users get their consumed credits **reset to zero** — effectively a free refill. Since V2.5 tokens go 5-8x further than V2 at these new prices, existing plans are now worth much more. Smart retention move.

---

## What This Means for You

If you're building anything with Chinese LLM APIs (for bank work, agents, CLI tools), MiMo-V2.5 is now worth benchmarking against:
- DeepSeek-V3 (¥2/M output, similar tier)
- Qwen-Plus
- Your current Claude/GPT-4o usage for non-English tasks

The SWA + HiCache architecture insight is also directly applicable to your own inference work — if you're running SGLang on your RTX 4070 or AMD MI300X, these are the knobs to understand.