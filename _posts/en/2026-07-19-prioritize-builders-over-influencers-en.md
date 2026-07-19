---
audio: false
generated: true
image: false
lang: en
layout: post
title: Prioritize Builders Over Influencers
translated: false
type: note
---

**Question:**
For a one-person company (OPC) / solo AI company, is it better to build relationships with highly technical engineers rather than attention-seeking KOLs or conference personalities? Are technical friendships more likely to become long-term mutual-benefit relationships?

**Answer:**

Yes, for a technical OPC, your highest-leverage network is usually **other builders**: engineers, researchers, founders who still write code, train models, ship products, debug systems.

The reason is structural:

### 1. Builders share the same "scar tissue"

A person who has:

* trained a model at 3 AM because CUDA OOM happened
* debugged distributed training failures
* shipped an agent that broke in production
* optimized inference cost
* dealt with customers

has a different communication layer.

You don't need to explain why:

* latency matters
* GPU memory is the bottleneck
* evals are hard
* "just fine-tune it" is usually naive

The relationship compounds because both sides exchange **real information**.

Example:

```
You:
"I tried Qwen with vLLM + LoRA, but KV cache exploded at 64k context."

Another engineer:
"Try paged attention + quantized KV cache. Also your batch strategy is wrong."

```

That is a relationship with immediate value.

---

### 2. Attention economies create different incentives

Many KOL / conference personalities optimize for:

```
attention → followers → reputation → opportunities
```

Builders optimize for:

```
knowledge → products → revenue → capability
```

These overlap sometimes, but not always.

A person whose main asset is audience may naturally ask:

> "How can this help my visibility?"

A builder often asks:

> "Can we build something together?"

For an OPC, the second type is usually more valuable.

---

### 3. The strongest AI companies are built through technical networks

Look at many successful AI organizations:

* early OpenAI came from a research community
* DeepMind grew from ML researchers
* many open-source projects grow from maintainers collaborating

The important network is not:

```
"I know 10,000 people"
```

but:

```
"I know 10 people who can each build something difficult"
```

A small number of high-agency technical people can create enormous leverage.

---

### 4. But don't completely ignore public-facing people

There is a useful distinction:

Bad:

```
KOL = only distribution, no depth
```

Good:

```
Technical founder + communication ability
```

The best people combine:

* deep technical ability
* ability to explain
* ability to connect people

For example, someone who writes excellent technical blogs, maintains open-source projects, and shares knowledge publicly is often a very good connection.

The signal is:

**Do they produce artifacts?**

Artifacts:

* GitHub repositories
* papers
* benchmarks
* products
* datasets
* technical writing

are stronger signals than:

* follower count
* conference photos
* hype posts

---

### 5. For your situation (AI OPC), I would prioritize

```
Tier 1:
AI engineers
ML researchers
open-source maintainers
startup technical founders

Tier 2:
technical product people
domain experts who can bring problems

Tier 3:
investors, KOLs, media people
```

The first group helps you create capability.

The second helps you find markets.

The third helps after you have something valuable.

---

A good rule:

> Don't network around status. Network around shared missions.

A person building an AI agent framework, training models, or deploying systems may become a 10-year collaborator.

A person only chasing the next trend topic may disappear when the trend changes.

For a high-tech OPC, **a small circle of extremely capable engineers is often a stronger moat than a large social following.** Your own path (training GPT-2, building agents, running an AI community, writing technical notes) naturally attracts that kind of person.
