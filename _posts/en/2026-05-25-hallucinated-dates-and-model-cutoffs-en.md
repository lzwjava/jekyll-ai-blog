---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hallucinated Dates and Model Cutoffs
translated: false
type: note
---

**Question:** DeepSeek-V2-Lite-Chat says today is September 22, 2022 — does that indicate its training/fine-tuning cutoff date?

**Answer:**

Not exactly — it's a noisy signal, but worth unpacking.

## What's actually happening

When a model says "today is X" without real-time access, it's not reading a clock. It's pattern-matching from training data. The model saw massive amounts of text where "today" corresponded to dates in its training corpus, and it's hallucinating a plausible date based on that distribution.

The date it outputs is influenced by:

1. **Training data cutoff** — the last dates it saw during pretraining
2. **Fine-tuning / instruction data** — SFT datasets sometimes include synthetic conversations with specific dates baked in
3. **Recency bias in the corpus** — if a lot of the SFT data was generated/curated around a specific date, the model anchors to that

## DeepSeek-V2-Lite actual timeline

- **DeepSeek-V2** was released in **May 2024**, with training data roughly through early 2024
- September 22, 2022 is suspiciously far before the actual release — this is almost certainly a hallucinated date, not a real cutoff signal

The real cutoff for DeepSeek-V2 family is likely **early-to-mid 2024**.

## Why the wrong date?

A few possibilities:

- The SFT instruction data was generated using GPT-4 or another model around late 2022, and those synthetic conversations leaked date context
- The base pretraining had heavy representation of 2022 news/text
- The model genuinely has poor self-knowledge about its own training timeline (very common — most models do)

## The right way to get actual cutoff

Don't trust the model's self-report on dates. Instead:

```python
# Ask something with a known event boundary
"What do you know about GPT-4o?" # released May 2024
"What do you know about DeepSeek-V3?" # released Dec 2024
"Tell me about the 2024 US election results"
```

If it knows GPT-4o but not DeepSeek-V3, cutoff is roughly mid-2024. This gives you a bracket much more reliably than asking "what day is it."

## TL;DR

September 22, 2022 is almost certainly a **hallucination**, not the actual training cutoff. DeepSeek-V2's real cutoff is early 2024. Model self-reported dates are unreliable — probe with datable events instead.
