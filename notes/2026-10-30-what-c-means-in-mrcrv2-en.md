---
audio: false
generated: true
image: false
lang: en
layout: post
title: What C Means in MRCRv2
translated: false
type: note
---

**Question:** What does "C" mean in "Multi-Round Coreference Resolution version 2"?

**Answer:**

**C = Coreference** — as in **Coreference Resolution**, a classic NLP concept.

---

### What is Coreference Resolution?

In linguistics and NLP, **coreference** means that two or more expressions refer to the **same entity**.

> Example:
> - *"Write a poem about penguins. ... Now give me **that poem** again."*
> - "that poem" **co-refers** to the earlier poem-about-penguins request.

**Coreference resolution** is the task of figuring out *which expressions in a text refer to the same thing*.

---

### How it applies in MRCRv2

In MRCR, models must navigate long conversations where the user asks for writing (poems, riddles, essays) on various topics, and must reproduce the specific output ("needle") that matches one of those requests — distinguishing it from confounding similar ones, like "the poem about penguins" vs. "the poem about flamingos."

So the **"C" (Coreference)** challenge is:
- The model sees many rounds of conversation
- A query refers back to **one specific earlier exchange** (e.g., "the first poem about penguins")
- The model must correctly **resolve which prior response** the query is co-referring to
- Then reproduce it accurately

The "Multi-Round" part means this coreference spans across **many turns** in a very long context (up to 1M tokens).

---

### Full name breakdown

| Part | Meaning |
|---|---|
| **Multi-Round** | Across many conversation turns |
| **Coreference** | Expressions referring back to the same earlier item |
| **Resolution** | Correctly identifying *which* item is being referred to |
| **v2** | Enhanced version with more needles and longer contexts |

**References:**
- [Michelangelo Paper (arXiv:2409.12640)](https://arxiv.org/abs/2409.12640)
- [MRCR Leaderboard - LLM Stats](https://llm-stats.com/benchmarks/mrcr)
