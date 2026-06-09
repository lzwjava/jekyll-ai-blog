---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek's Next Two Years Strategy
translated: false
type: note
---

**Question:** What will DeepSeek do in the next years?

**Answer:**

DeepSeek has a ~1T parameter MoE model (V4) in circulation with 32–37B active parameters per token, 1M token context, native multimodal (text, images, video, audio), and is 10–50x cheaper API pricing than frontier closed-source models, with open-source weights expected under Apache 2.0 license and runnable locally on dual RTX 4090s or single RTX 5090.

Three strategic vectors define their next ~2 years:

### 1. **MoE Scaling with Efficiency Focus**

V4 refines the MoE foundation from V3 (671B, 37B active) with updated routing mechanisms that dispatch tokens across experts with less redundant computation. V4 reportedly activates approximately 37 billion parameters per token — roughly the same as V3 — which means inference costs stay manageable even though the total model is 50% larger. This is the core innovation: they're pushing parameter count horizontally while keeping activation ratio flat. The next frontier is **expert routing efficiency** — less redundant computation across the 256+ expert pool.

For your GPU training interests: DeepSeek-V3 uses 256 experts with 8 active per token, achieving only 37B of 671B parameters activated (5.5% activation ratio) and uses Multi-Token Prediction for speculative decoding during inference. Watch for refinements in load-balancing across experts and FP8-friendly training to reduce VRAM footprint on mi300x clusters.

### 2. **Reasoning (R1 → R2) and Agentic Systems**

R2 development faced delays because CEO Liang Wenfeng was not satisfied with its performance; engineers were refining R2 until Liang approved release, and as of May 7, 2026, R2 is not listed among current model IDs. The delay signals they're targeting **something beyond just better benchmarks** — likely multi-language reasoning improvements (R1 was strong in English but weak in Chinese math/code) and deeper long-horizon agentic planning.

DeepSeek plans to launch an AI Agent by the end of 2025, building on existing technology like R1 and V3/V3.1 for scalable AI advancements. This is critical for you: they're moving from model-centric to **agent-centric architecture**. Expect tool use, planning, multi-step reasoning, and internal reasoning traces similar to OpenAI's o1.

### 3. **Infrastructure & Cost Reduction**

DeepSeek will expand its cloud ecosystem in 2025 with DeepSeek Cloud—a scalable platform offering seamless model access. They're building vertical integration: train on AMD chips (avoiding Nvidia export restrictions), serve via their own cloud, open-source weights for local deployment. This triples their surface area — API users, self-hosted enterprises, and research community all get access.

**API pricing** is their primary moat. V4 API is 10–50x cheaper than GPT-5.4 and Claude Opus 4.8, which forces other labs to optimize or lose market share. Expect continued price compression and expansion into verticals (finance, legal) where cost-per-inference matters.

### 4. **Vision & Multimodal Consolidation**

DeepSeek hinted at future multimodal support when announcing V3 in December 2024, mentioning multimodal support and cutting-edge features in the DeepSeek ecosystem. VL2 and Janus models are deployed for vision, OCR, and multimodal generation; Janus-Pro-7B is tracked as live. Their multimodal story is parallel tracks (VL2 for vision-language, Janus for generation), not unified V4 yet — expect convergence by 2027.

### 5. **Open-Source Acceleration**

DeepSeek plans to expand open-source initiatives, providing researchers with transparent access to datasets, methodologies, and model architectures, fostering community trust and strengthening its position as a leader in responsible AI research. This is cultural shift: they're competing on **transparency and accessibility**, not moat gatekeeping. Expect open technical reports, leaked weights pre-official release, and community-driven evals.

---

### **For You Specifically:**

Given your MI300X setup and nanoGPT interests:

1. **Watch MoE routing code** — their expert dispatch mechanism is where the efficiency lives. Decouple activation prediction from forward pass.
2. **Local inference optimization** — V4 at 37B active tokens is runnable on your RTX 4070. Study vLLM/SGLang + speculative decoding for that codepath.
3. **Agent architecture** — R2 + their planned agents signal movement toward agentic systems; this is where next-gen engineering lives.
4. **Cost curves** — track their API pricing monthly. They're signaling a race to $0.001/token inference by 2027. Margins compress, value moves to agents/applications.

**The core thesis:** DeepSeek is executing on *efficiency at scale*. Not "bigger models faster" — but "same capability, 10x cheaper, open weights, run locally." That directly threatens Nvidia's margin structure and forces everyone else to rethink architecture. Their next years are defined by doubling down on that asymmetry.
