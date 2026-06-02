---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Engineering Context for AI Agents
translated: false
type: note
---

Question: What is the content of the blog post at https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus?

Answer:

# Context Engineering for AI Agents: Lessons from Building Manus

**Author:** Yichao "Peak" Ji
**Date:** July 18, 2025

The blog post shares practical lessons on "context engineering" — the art of carefully shaping the input context for large language models (LLMs) — drawn from the author's experience building **Manus**, a general-purpose autonomous AI agent that executes complex computer-based tasks.

## Introduction
The team behind Manus decided to build their agent using in-context learning with frontier LLMs (rather than fine-tuning open-source models) to enable rapid iteration and benefit from ongoing model improvements. This approach required mastering context engineering, leading to four full rewrites of the agent framework through trial-and-error (humorously called "Stochastic Graduate Descent"). The post outlines key principles discovered along the way.

## Key Lessons

### 1. Design Around the KV-Cache
The KV-cache hit rate is the most critical metric for production AI agents because agents have very high input-to-output token ratios (e.g., 100:1 in Manus). Reusing cached prefixes dramatically reduces latency and cost.

Best practices:
- Keep the prompt prefix completely stable (avoid dynamic elements like timestamps).
- Make context strictly append-only and use deterministic serialization.
- Explicitly mark cache breakpoints when changes are unavoidable.

### 2. Mask, Don't Remove
Dynamically adding/removing tools from the context causes KV-cache invalidation and can confuse the model. Instead, keep all tools defined but use logit masking (via prefill modes in function calling) to enforce or prevent specific actions. Grouping tools with consistent name prefixes helps manage availability efficiently.

### 3. Use the File System as Context
Large context windows are insufficient for real agent tasks due to huge observations, performance degradation, and cost. Treat the local file system as unlimited external memory: agents read/write files, store URLs/paths instead of full content, enabling lossless "compression" of context.

### 4. Manipulate Attention Through Recitation
For long-running tasks, the agent maintains a `todo.md` file reciting current objectives. This keeps the high-level plan in recent context, countering "lost-in-the-middle" issues.

### 5. Keep the Wrong Stuff In
Do not hide or clean up errors and failed actions. Leaving failures (with stack traces) in context allows the model to learn from them and avoid repeating mistakes — a sign of true agentic behavior.

### 6. Don't Get Few-Shoted
Uniform few-shot examples can cause the agent to over-imitate patterns, leading to drift or hallucinations in repetitive tasks. Introduce structured variation (different phrasings, serialization, minor noise) to maintain diversity.

## Conclusion
Context engineering is an emerging but essential discipline for AI agents. It determines speed, robustness, recovery, and scalability. The lessons from Manus emphasize thoughtful context shaping over relying solely on bigger models. The future of agents will be built "one context at a time."

References:

- [Original blog post](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
