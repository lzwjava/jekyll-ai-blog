---
audio: false
generated: true
image: false
lang: en
layout: post
title: "VibeThinker-3B: Small Model, Frontier Reasoning"
translated: false
type: note
---

**Question:** What is WeiboAI/VibeThinker-3B?

**Answer:**

VibeThinker-3B is a small language model (SLM) from **Weibo AI** focused on pushing verifiable reasoning to the frontier at 3B parameters. Published ~5 days ago (paper: arXiv 2606.16140). Here's the breakdown:

**Base model:** Qwen2.5-3B (and Qwen2.5-Coder-3B), fine-tuned with a multi-stage pipeline.

**Core hypothesis — Parametric Compression-Coverage Hypothesis:**
> Verifiable reasoning (math, code, STEM) is a *highly compressible, parameter-dense* capability. If feedback signals are reliable and the task space is structured, small models can reach near-frontier performance. Open-domain knowledge, by contrast, needs scale to cover the long tail.

This is a meaningful distinction — they're not claiming 3B replaces 671B for general knowledge, just for *verifiable* tasks.

---

**Training pipeline (Spectrum-to-Signal Principle, SSP):**

1. **Curriculum SFT (2 stages)** — Stage 1: broad coverage (math, code, STEM, dialogue). Stage 2: harder, longer-horizon samples. Uses *Diversity-Exploring Distillation* to preserve multiple valid solution paths.
2. **Multi-domain RL** — MaxEnt-Guided Policy Optimization (MGPO), applied sequentially to math → code → STEM. 64K context window to keep full reasoning trajectories intact.
3. **Offline Self-Distillation** — filters high-quality RL trajectories, distills back into a unified student. Prioritizes traces that are correct but not yet well-modeled (learning-potential score).
4. **Instruct RL** — final stage for user-facing controllability, using rule-based validators + rubric-based reward models.

---

**Performance numbers:**

- **IMO-AnswerBench (400 IMO-level problems):** 76.4, improves to **80.6 with CLR** (Claim-Level Reliability Assessment, a test-time scaling strategy)
- Comparable to DeepSeek V3.2 (78.3, **671B**), GLM-5 (82.5, **744B**), Kimi K2.5 (81.8, **1T**) — at 3B
- **LeetCode (Apr 25 – May 31, 2026, unseen contests):** 123/128 first-attempt submissions = **96.1% acceptance rate**

---

**What's notable for you:**

- The SSP pipeline (SFT → RL → self-distillation → instruct RL) is a clean, replicable recipe directly applicable to nanoGPT/nanochat-scale experiments you're doing
- MGPO is their take on entropy-regularized policy optimization — worth reading the 1.5B paper for the math
- CLR (test-time scaling via claim-level reliability) is an interesting inference-time trick that bumps IMO score from 76.4 → 80.6 without changing weights
- **Not** trained for tool-calling/agents — use it for competitive math/LeetCode-style problems only

---

**References:**

- [WeiboAI/VibeThinker-3B on HuggingFace](https://huggingface.co/WeiboAI/VibeThinker-3B)
- [Technical Report arXiv:2606.16140](https://arxiv.org/abs/2606.16140)
- [GitHub](https://github.com/WeiboAI/VibeThinker)
