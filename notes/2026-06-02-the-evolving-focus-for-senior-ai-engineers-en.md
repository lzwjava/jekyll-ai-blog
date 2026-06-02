---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Evolving Focus for Senior AI Engineers
translated: false
type: note
---

Question: Is the current hot focus for senior engineers in AI/agent/full-stack roles centered around AI harness, agents, LLM training, and inference?

Answer:

**Yes, but with nuance.** The frontier has shifted in the last 6-12 months. Here's what's actually hot:

**1. Agent systems & reasoning (the biggest move)**
The industry pivot from "chatbots with tool use" → "autonomous agents that actually plan and execute." This includes:
- Multi-step reasoning (OpenAI o1, DeepSeek-R1)
- Tool orchestration at scale (how do agents compose API calls?)
- Agentic workflows (CrewAI, LangGraph, Anthropic's Prompt Caching for stateful agents)

You're already positioned here. Your CLI agents (ww, iclaw, zz) are exactly what senior engineers are building now.

**2. Inference optimization (the efficiency war)**
- KV cache quantization (4-bit, 2-bit)
- Speculative decoding (draft model → verify)
- Batching strategies for agents (agents are bursty, not steady-state)
- Running smaller, fine-tuned models instead of calling GPT-4 (LoRA, DPO/GRPO on H100 is cheaper than API calls at scale)

For your bank workload (1.5B tokens/year), this is **direct ROI**: a 2x inference speedup + quantization = 50% cost reduction.

**3. Training (real but narrower)**
- Fine-tuning on domain data (finance, in your case—perfect)
- Continued pretraining on proprietary data (less common; expensive)
- RLHF/DPO/GRPO for preference alignment (why GPT-4 is smarter than Llama on your tasks)

Training from scratch (like your GPT-2 work) is now niche — most senior engineers tune existing models. **Except:** if you're at a bank with proprietary financial datasets and H100s, training a domain-specific 7B-13B model is legitimate frontier work. That's rare and high-value.

**4. What's NOT hot anymore**
- Plain LLM APIs (everyone uses them; no senior engineer career wins)
- Basic RAG (boring, saturated)
- Generic fine-tuning without inference optimization

**Where you should double down:**

Given your setup (H200/H100 access, 1.5B token consumption, agent-building experience):

1. **Agent architecture + reasoning** — build systems that use smaller, fine-tuned models for specific reasoning tasks instead of calling GPT-4
2. **Inference at scale** — quantize models, implement speculative decoding, optimize batching for your bank's workload
3. **Fine-tuning pipeline** — build internal tooling to train domain-specific financial models on your proprietary data, then deploy them
4. **Agent <> model co-optimization** — train agents that know which tool (big model, small model, API) to use for each task (this is where Andrej/Karpathy-level thinking lives)

**The real frontier for you right now:**

Build a system that:
- Takes your bank's proprietary financial queries
- Routes to a 7B fine-tuned model (trained on your data + DPO)
- Falls back to GPT-4 for complex reasoning
- Logs reasoning traces for continuous improvement
- Costs 80% less than pure GPT-4 while being faster

That's not a product pitch — that's a **senior AI engineer's job**. And it's exactly what global banks are hiring for (or trying to build internally and failing at).

You're not behind. You're at the center of it. Just make sure "agent + training + inference optimization" is your trinity, not "training from scratch" alone.