---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Laya: Multilingual Non-Autoregressive Decision Model"
translated: false
type: note
---

Question: What is the "laya" model on Hugging Face (convaiinnovations/laya)?

Answer: Laya is a multilingual, non-autoregressive "System 1" decision model that takes a state (text, email, ticket, or JSON) plus typed questions and returns typed answers with calibrated probabilities in a single forward pass (about 33 ms) across 100+ languages. It never generates free text, so there's nothing to hallucinate — it's built for classification/routing/scoring/guardrail-type tasks rather than open-ended generation.

Key details:

- **Architecture**: The English checkpoint (this repo's root) is a ModernBERT-large backbone (395M params) fully fine-tuned plus a decision head trained from scratch, 421M total parameters, with a 512-token context. A multilingual variant uses an mmBERT-base backbone (322M params, up to 8k context), and a third checkpoint is fine-tuned specifically for "typed-decisions" workflows.
- **Training method**: It uses what the authors call RLCD (Reinforcement Learning for Calibrated Decisions) — the model is trained against strictly proper scoring rules so that reporting honest probabilities is the reward-maximizing strategy.
- **License**: Apache 2.0 (open weights, commercial use allowed).
- **Positioning**: The model card explicitly compares it to a closed system called "TypeSafe Jev," claiming much lower latency (32.8 ms vs. 236–276 ms p50) and better accuracy on several benchmarks, while noting Jev still leads on very high-cardinality classification (>20 label options).
- **Honest limitations** (stated by the authors): the base checkpoints perform close to chance zero-shot on their own "typed-decisions" benchmark — the strong 0.766 accuracy figure belongs to a checkpoint fine-tuned on that benchmark's training split, not the raw model; scores also ship overconfident before temperature calibration.
- Install via `pip install laya`; there's a GitHub repo, PyPI package, and a live HF Space demo.

In short: it's a small, fast, open-source encoder-based classifier/decision model (not a text generator), aimed at structured decision-making tasks like routing, moderation, and scoring — positioned as a faster, cheaper, open alternative to a closed "Jev" system.

References:

- [convaiinnovations/laya on Hugging Face](https://huggingface.co/convaiinnovations/laya)
- [Laya GitHub repository](https://github.com/NandhaKishorM/laya)
- [Laya on PyPI](https://pypi.org/project/laya/)
