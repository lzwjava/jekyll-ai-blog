---
audio: false
generated: true
image: false
lang: en
layout: post
title: Scaling LLM Usage to Billions of Tokens
translated: false
type: note
---

Question: How can someone consume around 10 billion tokens in a year using LLMs, and who are known examples of people doing this (like Huang Dongxu from TiDB)?

Answer:

If you actually want to reach **billions of tokens per year**, casual chatting won’t get you there. You need to treat LLM usage as a **systematic, high-throughput workflow**, not just occasional prompting.

Let’s break it down realistically.

---

# 1. What “10 billion tokens/year” actually means

10B tokens/year ≈

* ~27 million tokens/day
* ~1.1 million tokens/hour (24h continuous)

That’s not human-scale interaction anymore. That’s **pipeline + automation scale**.

So if you're imagining “just prompting more,” that won’t work. You need **machines prompting machines**.

---

# 2. The only 3 ways people reach that scale

## (A) Programmatic usage (most important)

Instead of:

* You → prompt → read → prompt

You do:

* Code → generates prompts → sends to LLM → processes outputs → loops

Typical patterns:

* Batch processing datasets
* Auto-evaluation loops
* Synthetic data generation
* Multi-agent simulations

Example:

```python
for item in dataset:
    response = llm(prompt_template(item))
    store(response)
```

This alone can generate **millions of tokens per hour**.

---

## (B) Iterative pipelines (LLM calling LLM)

Heavy users don’t just call once—they chain:

* Draft → critique → improve → summarize → evaluate
* Or:

  * Generator model
  * Critic model
  * Refiner model

This multiplies token usage by **5–20x per task**.

---

## (C) Long-context workflows

Using:

* 32k / 128k / 1M context windows

Activities:

* Feed entire books/codebases
* Repeated re-analysis
* Memory-based agents

One run can consume:

* **hundreds of thousands to millions of tokens**

---

# 3. Practical ways YOU can reach high token usage

If your goal is intentional (learning / building), here are concrete strategies:

## 1. Build a “thinking loop system”

Instead of asking once:

* Ask → get answer
* Ask model to critique
* Ask model to improve
* Ask model to compress
* Repeat

This turns:

* 1 prompt → 10–50 prompts

---

## 2. Use LLM for everything you read

You mentioned:

> prompting + reading + iterating

Upgrade it:

* Paste articles/books/code
* Ask:

  * summarize
  * extract structure
  * generate questions
  * debate both sides

You multiply token usage by:

* input tokens (large)
* output tokens (large)

---

## 3. Synthetic data generation

This is what serious builders do:

* Generate:

  * Q&A pairs
  * training data
  * edge cases
* Then:

  * filter
  * score
  * regenerate

This is **exactly how people burn billions of tokens**.

---

## 4. Continuous background jobs

Run scripts like:

* “Generate 10k problems per day”
* “Simulate 1k conversations”
* “Rewrite dataset 5 times”

This is how you cross from:

* **millions → billions**

---

## 5. Multi-agent systems

Create agents that:

* Debate
* Plan
* Execute
* Reflect

Each step = multiple LLM calls.

This explodes token usage naturally.

---

# 4. People known for extreme LLM usage

## Huang Dongxu

* Known in engineering circles for:

  * Deep technical exploration
  * Heavy experimentation mindset
* Represents the **“builder who learns by doing at scale”** archetype

---

## Andrej Karpathy

* Talks about:

  * “tokens as the new compute”
  * treating LLMs as programmable systems
* Encourages high-volume experimentation

---

## Sam Altman

* Has mentioned:

  * some users consume **massive token volumes**
* Internally, power users are:

  * researchers
  * startups building pipelines

---

## Emad Mostaque

* Advocates for:

  * large-scale generation
  * synthetic data loops

---

# 5. Reality check (important)

If you’re doing:

> manual prompting + reading

You might reach:

* 1M–10M tokens/year (already heavy)

To hit:

* **1B+ tokens → requires automation**
* **10B+ tokens → requires infrastructure**

So the real shift is:

> from “user” → “system builder”

---

# 6. A better mental model

Think like this:

* Tokens = fuel
* Prompts = programs
* LLM = CPU

If you want to burn fuel:
→ you need **programs running continuously**

---

# 7. A practical path for you (based on your background)

Given you already:

* do ML
* build systems

You should try:

1. Build a **dataset generator**
2. Add:

   * evaluator loop
   * improvement loop
3. Run it daily

That alone can push you into:

* **100M–1B tokens/year range**

---

If you want, I can design a **personal “10B token system architecture”** tailored to your skills (full-stack + ML).