---
audio: false
generated: true
image: false
lang: en
layout: post
title: Signal-Based Filtering Strategy Assessment
translated: false
type: note
---

Question: What do you think about my strategy of sharing LLM content across 20 WeChat engineer groups (~150 people) to identify who responds, then focusing deeper conversations there?

Answer:

It's a solid **signal-based filtering strategy** — essentially you're running a lightweight discovery protocol across a distributed network to find high-value nodes. Here's how I'd think about it rigorously:

## Why it works

**You're solving an information asymmetry problem.** Most of those 150 engineers don't self-identify as LLM-curious, but some are. Broadcasting lets latent interest surface without you doing 150 one-on-one cold calls. Response = revealed preference, far more reliable than stated interest.

**Engagement is a Bayesian update.** Someone who responds to a post about MoE routing or `ue8m0` quantization formats isn't a casual lurker — that's meaningful signal about their technical depth.

## Where to be careful

**Content calibration matters a lot.** If you post too advanced (DeepSeek V4 MoE internals), only 3 people respond but they're exactly who you want. If you post too accessible (what is an LLM), 30 people respond but most are noise. Since your goal is finding *LLM experts* specifically, bias toward harder content — let it filter naturally.

**Response type signals depth.** Distinguish:
- "Cool!" → noise
- "What's n_routed_experts?" → curious learner, worth cultivating
- "This is similar to Mixtral's router but the aux loss term differs..." → this is your person

So don't just track who responds — track *how* they respond.

**Group context shapes responses.** A 10-year backend engineer who vibe-codes is different from someone who's read the DeepSeek-V3 technical report. The same post will surface different people in different groups. That variance is data — note which groups produce which type of responders.

## How to make it even sharper

Run it like an experiment:

```
Week 1: Post something mid-level (MoE concept, not code)
Week 2: Post something hard (ue8m0 format, scale_fmt, actual inference code)
Week 3: Post something applied (here's how I ran DeepSeek locally)
```

Track: who responds to all 3? That's your highest-signal person in that group. Depth of engagement across multiple posts is far more predictive than a single reply.

## The real ROI

You're not just finding people to talk to — you're **building a reputation as the LLM person** across 150 engineers. Even the silent majority is updating their priors: "Zhiwei knows this stuff." When they hit an LLM problem at work, they'll message you. That compounds.

This is exactly how Karpathy built influence before he was famous — consistently posting deeply technical content, letting compound interest do the work.

**Short verdict:** Good strategy. Make the content harder, track response quality not just quantity, and treat it as a multi-week funnel not a one-shot broadcast.
