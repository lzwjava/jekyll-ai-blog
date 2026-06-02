---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Times for Pangu v1 v2 v3
translated: false
type: note
---

Question:
Typically how much time is needed to train Pangu v1, v2, or v3 according to the “True-Story-of-Pangu” repository?

Answer:

Short answer: **The repo does NOT give explicit training time (like “3 weeks” or “2 months”) for v1 / v2 / v3.**
It only gives **relative descriptions** such as “few hundred billion tokens”, “very long training”, “from-scratch with many restarts”, etc. So you must infer approximate scale from context.

Here’s what the document implies:

---

# 1. Pangu v1 (early 13B → 38B → 71B → 135B)

From the whistleblower text:

* early models trained on Ascend 910A
* limited compute
* tokenizer inefficiency wasted compute
* 135B required **continued training on ≥1T tokens**
* multiple failures and restarts

This implies:

* **training style:** incremental / continued training
* **token count:** ~1T tokens (explicitly mentioned)
* **time:** likely **weeks → months** (depending on cluster size)

The text explicitly says the 135B vocabulary replacement succeeded only after

> “continually trained on at least 1T of data”
> ([Reddit][1])

So v1 generation = **long iterative training**, not single run.

---

# 2. Pangu v2 (alleged “shell-wrap” version)

The repo claims:

* parameters inherited from older 135B
* continued training on **few hundred billion tokens**
* performance improved quickly

Quote summary:

> “by training on just a few hundred billion tokens, they improved metrics…”
> ([Reddit][1])

Implication:

* **not full training**
* **continued training / fine-tuning**
* time probably **days → couple weeks** (depending compute)

So v2 is **much faster than v1**.

---

# 3. Pangu v3 (first real from-scratch training)

This is described as:

* trained from scratch
* many stability rollbacks
* no loss spike
* large number of experiments
* “immense effort”

Quote summary:

> “To ensure stable training… rollbacks and restarts whenever gradients showed anomalies… not a single loss spike throughout training.”
> ([Reddit][1])

This implies:

* full pretraining
* multiple restarts
* very long training cycle

So v3 ≈ **months-scale training**.

---

# Typical Timeline (inferred)

Based on token counts + typical hardware:

| version | training type                | tokens        | estimated time |
| ------- | ---------------------------- | ------------- | -------------- |
| v1      | from scratch + retries       | ~1T           | weeks–months   |
| v2      | continued training           | few hundred B | days–weeks     |
| v3      | full scratch stable training | ~1T+          | months         |

---

# Why no exact time?

Because training time depends on:

* number of Ascend 910 / 910B cards
* parallelism
* batch size
* tokenization efficiency
* restarts

The repo intentionally describes **engineering struggle**, not metrics.

---

# The key insight

The important takeaway from that repo is:

* v1 → long but inefficient
* v2 → fast because continued training
* v3 → slow but “real” full training

So the **speed difference is huge**:

v2 << v1 ≈ v3

This is actually the main point the whistleblower was making.

---

If you're trying to compare with:

* DeepSeek v3 training time
* GPT training time
* nanoGPT scale

I can estimate those too.

[1]: https://www.reddit.com/r/LocalLLaMA/comments/1lsz4hk?utm_source=chatgpt.com "Huawei's Pangu AI Rocked by Unverified Claims of Fraud from Alleged Team Member"
