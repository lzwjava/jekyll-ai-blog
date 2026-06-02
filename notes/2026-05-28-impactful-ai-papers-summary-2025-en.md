---
audio: false
generated: true
image: false
lang: en
layout: post
title: Impactful AI Papers Summary 2025
translated: false
type: note
---

**Question:** What are the new and impactful AI/LLM papers from the past year?

**Answer:**

Here's a curated, opinionated breakdown organized by theme — papers that shifted thinking, not just benchmarks. I'm covering roughly May 2024–May 2026.

---

## 1. Reasoning & RL Post-Training

### DeepSeek-R1 (Jan 2025) — *the* paper of the year
**arXiv: 2501.12948**

Uses GRPO (Group Relative Policy Optimization) as the RL framework, with reward signal solely based on correctness of final predictions against ground-truth answers, without imposing constraints on the reasoning process itself — bypassing the conventional SFT phase before RL training entirely.

Several emergent behaviors appeared as reasoning steps increased: "aha moments," self-reflection, and tracing back to revise strategies. The reward design uses verifiable correctness checks — does the code compile, does the math expression give the right result — now called RLVR (Reinforcement Learning from Verifiable Rewards).

AIME 2024 pass@1 went from 15.6% → 71.0%, and with majority voting → 86.7%, matching OpenAI-o1-0912.

The key insight: **reasoning can emerge as a behavior, not just imitation of human traces.** This unlocked a wave of "RL for reasoning" work (STILL, DAPO, Dr. GRPO, etc.) and the RLVR paradigm.

**Dr. GRPO (2025):** Identifies a bias in GRPO's optimization that leads to progressively longer incorrect responses, and proposes a simple fix (GRPO Done Right). Achieves state-of-the-art reasoning performance with only 27 hours of compute on 8× A100 GPUs on Qwen2.5-Math-7B.

---

### s1: Simple Test-Time Scaling (Jan 2025)
**arXiv: 2501.19393**

Demonstrates that distilling Gemini 2.0 Flash Thinking traces into Qwen-32B with "budget forcing" (forcing the model to keep thinking up to a token budget) yields strong reasoning at low cost. Uses only ~1K examples for finetuning.

Shows you can get o1-class reasoning for $50 of finetuning if you have the right distillation data. Directly relevant to your model-training work.

---

## 2. Architecture & Efficiency

### Titans: Learning to Memorize at Test Time (Dec 2024)
**Google Research**

Introduces a neural long-term memory module that learns to memorize historical context *at test time*, combining the strengths of recurrent models and attention mechanisms. Enables efficient processing of sequences beyond 2 million tokens.

This is the most interesting architecture paper of the cycle — it's an attack on the "attention is all you need" assumption for long context. Attention = short-term memory, the new module = long-term memory. Worth reading alongside Mamba/SSM literature.

---

### Scaling LLM Test-Time Compute (Aug 2024)
**arXiv: 2408.03314** — Berkeley/Google

The main premise: if increased test-time computation can improve LLM outputs, then scaling inference compute can be more effective than scaling model parameters on hard tasks.

This is what theoretically grounded o1, R1, and the whole reasoning model wave. **Pre-training scaling is hitting diminishing returns; inference-time scaling is the new axis.**

---

### DeepSeek-V3 / MoE Architecture (Dec 2024)
**arXiv: 2412.19437**

The engineering paper behind R1. Key contributions:
- Multi-head Latent Attention (MLA) — compresses KV cache via low-rank projection
- Auxiliary-loss-free load balancing for MoE
- FP8 mixed-precision training at scale

If you want to understand how a 671B MoE runs efficiently, this is your paper.

---

## 3. Inference Optimization

### Trellis: Learnable KV Cache Compression (Dec 2025)

Introduces a learnable, bounded-memory alternative to traditional KV caches. On benchmarks like RULER, it outperforms baselines by retaining more context in under 1% of the memory footprint. Sequence length scales to 128K tokens without quadratic memory growth.

The O(n²) KV cache problem is now being attacked from multiple angles — SnapKV, RazorAttention, Trellis, and MLA (above). If you're building inference systems on your 4070, this literature is directly relevant.

---

## 4. Agents & Memory

### Memory in the Age of AI Agents: A Survey (Dec 2025)

Distinguishes Agent Memory from RAG and Context Engineering, providing a comprehensive taxonomy across three lenses: Forms (what carries memory), Functions (what memory does), and Dynamics (how memory evolves). Covers everything from KV cache eviction to episodic memory modules.

Good map of the agent memory space if you're building CLI agents like your `ww`/`zz` tools.

---

## 5. Open & Reproducible Models

### OLMo 2 (2025)

One of the most important fully open AI model papers of 2025 — emphasizes complete transparency across training data, architecture, and methodology. Strengthened the push toward reproducible open AI research.

If you're training GPT-2-scale models and want to understand real training decisions at scale, OLMo 2's full transparency (data, checkpoints, training code) is invaluable.

---

### Qwen3 (2025)

Integrates flexible thinking and non-thinking modes, optimizing resource usage for diverse tasks. The flagship Qwen3-235B-A22B model achieved 85.7 on major benchmarks.

GSPO (Group Sequence Policy Optimization) was used in Qwen3 and contributed "remarkable improvements" by using sequence-level importance ratios instead of token-level, providing more stable RL training.

---

## 6. Benchmarks Worth Knowing

- **SWE-Lancer** — Benchmarks LLMs on 1,400+ freelance coding tasks from Upwork. Even Claude 3.5 Sonnet succeeded only 26.2% of the time, highlighting AI's current limits in applied software engineering.
- **CURIE** — evaluates LLMs on long scientific document reasoning (quantum computing, materials science)
- **WideSearch** — tests broad information-gathering agents vs narrow deep reasoning

---

## TL;DR Priority Reading Order for You

| Priority | Paper | Why |
|---|---|---|
| 🔥 Must | DeepSeek-R1 (2501.12948) | RLVR, GRPO, emergent reasoning |
| 🔥 Must | Test-Time Compute Scaling (2408.03314) | New scaling axis, pre-training plateau |
| High | Titans (Dec 2024) | Architecture alternative to attention for long-ctx |
| High | DeepSeek-V3 (2412.19437) | MLA, MoE engineering at scale |
| High | s1 (2501.19393) | Budget forcing, cheap reasoning distillation |
| Medium | Dr. GRPO (2503.20783) | Fix GRPO bias, replicate R1 cheaply |
| Medium | OLMo 2 | Open training transparency |
| Skim | Trellis / SnapKV / RazorAttention | KV cache compression, inference opt |

Given you're training GPT-2-scale models now, the R1 + Dr. GRPO + s1 cluster is the most immediately actionable — you could replicate R1-Zero training on math datasets on your 4070 within the Dr. GRPO budget.

---

**References:**

- [DeepSeek-R1](https://arxiv.org/abs/2501.12948)
- [s1: Simple Test-Time Scaling](https://arxiv.org/abs/2501.19393)
- [Scaling LLM Test-Time Compute](https://arxiv.org/abs/2408.03314)
- [DeepSeek-V3](https://arxiv.org/abs/2412.19437)
- [Dr. GRPO](https://arxiv.org/abs/2503.20783)
- [Titans](https://arxiv.org/abs/2501.00663)
- [Sebastian Raschka's 2025 LLM Paper List](https://magazine.sebastianraschka.com/p/llm-research-papers-2025-list-one)
- [Latent.Space 2025 AI Engineering Reading List](https://www.latent.space/p/2025-papers)
