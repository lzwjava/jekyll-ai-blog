---
audio: false
generated: true
image: false
lang: en
layout: post
title: Steelmanning Future Tech Expertise
translated: false
type: note
---

**Question:** What tech/knowledge stack should you invest in now (2026) so that by 2030 you're the one people learn *from* — using the historical analogy that 2010s mobile devs are now learning LLM, but new devs skip mobile entirely?

**Answer:**

This is a sharp mental model. Let me steelman it and extend it.

---

## The Analogy Is Structurally Sound

| Era | "New platform" | Who got wealthy | Who got left behind |
|-----|---------------|-----------------|---------------------|
| 2008–2012 | iOS/Android | Early mobile devs, app founders | Web-only devs who waited |
| 2012–2016 | Cloud/AWS | Early DevOps, SRE, distributed systems | On-prem-only engineers |
| 2016–2020 | Deep Learning | Early ML engineers, PyTorch users | CV/NLP rule-based people |
| 2020–2024 | LLMs/Transformers | Prompt engineers, fine-tuners, agent builders | Everyone else catching up |
| **2024–2028** | **???** | **You want to be here** | — |

The key insight: **the people who are wealthy in knowledge by 2030 are the ones who go one layer deeper than "use the LLM API" right now.**

---

## What's the 2026 Equivalent of "Learn iOS in 2010"?

In 2010, learning iOS meant:
- Learning a platform *most people dismissed* ("who needs an app?")
- Going below the abstraction (Objective-C, UIKit internals, memory management)
- Building when tooling was immature and documentation was sparse

The direct analogy today is **not** "learn to call GPT-4". That's the equivalent of "learn to download an app." The equivalent of building iOS apps in 2010 is:

### 1. **Model Internals — Below the API**
Not "how to prompt" but:
- Attention mechanism implementation (you already do this — go further)
- KV cache management, speculative decoding, continuous batching
- Quantization: GPTQ, AWQ, GGUF — *why* they work, not just how to run them
- Custom CUDA kernels for attention (FlashAttention math, not just usage)

By 2030, the people who understand *why* a 70B model runs fast on 2 GPUs will be rare and expensive. Most people will just call APIs.

### 2. **Post-Training Stack (RLHF → DPO → GRPO)**
This is where value is manufactured from base models. You're already touching this. Double down:
- Reward modeling from first principles
- GRPO (what DeepSeek used) — Group Relative Policy Optimization
- Synthetic data generation pipelines (the real moat)
- Evaluation design — this is criminally underrated

The 2030 equivalent of "I shipped the first 5-star app in the App Store" is "I trained a domain-specific model that actually outperforms GPT on X."

### 3. **Agent Infrastructure (not LangChain — the layer below it)**
LangChain is the Cordova/PhoneGap of this era — it'll largely be irrelevant by 2028. What won't be:
- Tool use protocols (MCP is interesting here — you're already using it)
- Memory architectures (episodic, semantic, working memory for agents)
- Multi-agent orchestration at production scale
- Reliability engineering for non-deterministic systems

### 4. **Domain × Model Intersection**
The most defensible position by 2030 is **domain expertise + model training capability**. Pure ML engineers are becoming commoditized. But:
- A finance engineer who can fine-tune + evaluate models on proprietary financial data? Rare.
- You already have this: banking systems + AI engineering. That's a moat.

### 5. **Inference Optimization & Deployment**
As models commoditize at the API level, the value shifts to running them efficiently:
- vLLM internals, PagedAttention
- Mixture of Experts routing (what Mixtral/DeepSeek-MoE do)
- Edge inference (models on device — Apple Silicon NPU, Qualcomm)
- Disaggregated prefill/decode (the hot research area right now)

---

## What to *Avoid* Learning Deeply (2026)

These are the "BlackBerry development skills" of this era:

| Skip | Why |
|------|-----|
| Prompt engineering as a discipline | Gets automated by meta-prompting systems |
| RAG pipeline plumbing | Becomes a commodity feature in every vector DB |
| LangChain/LlamaIndex internals | Framework churn — abstractions will shift |
| "AI product management" | Too high-level, zero technical moat |
| Fine-tuning LoRA on commodity models | Table stakes by 2027 |

---

## Your Specific Position (Zhiwei)

You have a rare combination that maps cleanly onto the 2030 valuable stack:

```
Banking domain knowledge        →  finance model fine-tuning + evals
iOS/Android/full-stack history  →  on-device inference, multimodal UX
12 years systems engineering    →  agent reliability, infra for LLM systems  
GPT-2 training from scratch     →  go deeper: MoE, speculative decoding
1.5B tokens/year consumption    →  systematic evaluation, prompt-to-training pipeline
```

The bet I'd make for you specifically: **train a small (1–7B) finance/banking domain model end-to-end — pretraining data curation, post-training with DPO/GRPO, evaluation harness, deployment on vLLM.** That entire pipeline, done once with real data, makes you genuinely rare by 2028.

---

## The Meta-Point

The people who learned iOS in 2010 didn't know it would be worth $300k/year salaries by 2015. They just followed the platform that felt *alive* — where the energy was. 

Right now, the energy is clearly in:
1. Model internals and post-training
2. Agent systems that actually work in production
3. Inference efficiency at scale
4. Multimodal (vision + audio + text together)

You're already in the current. Go deeper, not broader. The 2030 version of "I built apps when no one else did" is "I trained models when everyone else just called APIs."