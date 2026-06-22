---
audio: false
generated: true
image: false
lang: en
layout: post
title: Code Training Beats Natural Language
translated: false
type: note
---

**Question:** Is training small models on code better than natural language due to lower entropy? And is Anthropic's code-first bet vs OpenAI's scattered approach a key reason Anthropic is catching up in market cap?

**Answer:**

Your intuition is directionally correct, and the reasoning chain holds. Let me sharpen each link.

---

## Entropy Chain: Why Code Wins for Small Models

Natural language has high **conditional entropy** — given "The weather today is...", the next token distribution is nearly flat across hundreds of plausible continuations. Code is the opposite:

```python
for i in range(
```

The next token is almost certainly `10`, `n`, `len(`, or a variable name from scope. The **branching factor** is tiny.

Formally: if cross-entropy loss is `H = -Σ p(x) log p(x)`, a lower-entropy distribution means the model has less to "guess" per token. For a small model (say 760M params like your GPT-2), this matters enormously — the model's capacity isn't wasted learning that "the" can follow 10,000 different things.

**Result:** same model size, same compute, but code models converge faster and generalize better on their domain. This is why Codex (the original code model) was fine-tuned from GPT-3, not trained differently in architecture — the data distribution did the work.

---

## Why Code Data Quality Is Also Higher

- **Ground truth is verifiable** — code either runs or it doesn't. Natural language has no such oracle.
- **Less noise** — GitHub code has consistent formatting, naming conventions, syntax. Crawled web text is chaotic.
- **Implicit structure** — `user`, `users`, `all_users` teaches the model morphology, plurality, scope, naming conventions *implicitly* — things natural language needs explicit annotation to teach.
- **Compression ratio** — code is dense with semantics per token. A 10-line function encodes logic, control flow, types, naming — equivalent prose would be a paragraph.

---

## Anthropic's Bet: Correct Strategic Prioritization

Your framing is right. The implicit Anthropic thesis:

```
Code > Natural Language > Image/Video
(in terms of: trainability, data quality, verifiability, ROI per compute dollar)
```

Anthropic leaned into code + long context + safety-on-reasoning. OpenAI went:
- Sora (video gen — hardest modality, highest compute cost, lowest verifiability)
- GPT-4o multimodal (voice, image, video all at once)
- Operator, various consumer products
- o1/o3 reasoning (good bet, but late relative to internal capability)

Scattered surface area = diluted learning signal across teams, compute, and data pipelines.

Anthropic's counter: Claude Code is now a genuine moat. Code generation is the highest-ROI use case for LLMs in enterprise — measurable productivity gains, easy to evaluate, direct revenue attachment. The $18.4B valuation catch-up is partly this focus paying off.

---

## The Sora Timing Point

Completely valid. Sora is a **diffusion transformer on latent video** — the compute and data requirements are 100x text. OpenAI shipped it before the infrastructure economics made sense. A few years from now when H100-equivalent compute is $0.10/hr instead of $2+, video gen becomes viable at scale. OpenAI was technically impressive but economically early.

---

## Your Analogy

The upgrade from natural language → code training feels like the Android → iPhone switch because:

- **Feedback loops tighten** (loss descends faster = you see results sooner)
- **Signal quality improves** (code errors are unambiguous)
- **The environment is more predictable** (syntax constrains the space)

Training intuition compounds faster in a low-entropy domain. You build the mental model of "what makes a good model" faster when the ground truth is clear.

This is also why I'd suggest: if you're running nanochat experiments on your RTX 4070, **start with code corpus** (The Stack, StarCoder data, or even just filtered GitHub Python). You'll see cleaner loss curves, faster iteration, and the model behaviors will be more interpretable — which is exactly what you need to build intuition for the harder natural language and multimodal work later.
