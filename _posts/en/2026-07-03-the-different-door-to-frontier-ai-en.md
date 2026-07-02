---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Different Door to Frontier AI
translated: false
type: note
---

**Question:** Can I realistically start a frontier LLM/AI lab as a startup?

**Answer:**

Direct answer: **found one today, no. Get to the frontier, yes — but through a different door than you're imagining.** Let me show you the actual numbers, then the realistic ladder.

## What "frontier lab" costs in 2026

The entry ticket is founder pedigree converted into capital, before any product exists:

- SSI raised $2 billion at a $32 billion valuation in its second round, with no models or safety research published as of early 2026
- Thinking Machines closed a $12 billion seed in July 2025 and a $5 billion Series B at a $50 billion valuation in March 2026
- Two ex-Anthropic researchers raised $200M at $1B for Mirendil weeks after quitting — launched with no shipped product, on the strength of the founders alone
- xAI runs ~200,000 GPUs in Memphis and is building toward 1 million

The pattern is brutal and consistent: these rounds are priced on "this person led research at OpenAI/Anthropic/DeepMind." VCs are buying a claim on future researchers who will follow that founder. A self-taught engineer at a bank in Guangzhou — no matter how sharp — cannot raise this round in 2026. Your GPT-2 760M run is genuinely good work, but frontier pretraining is ~10^25–10^26 FLOPs; you're operating 4–5 orders of magnitude below that, and no amount of cleverness closes a compute gap that size solo.

## The Wenfeng Liang counterexample — read it correctly

Your idol did found a frontier lab from China with no US-lab pedigree. But the mechanism matters: he built High-Flyer first, a quant fund generating billions in AUM, then used its capital to stockpile ~10K A100s *before* export controls, then started DeepSeek. He didn't raise a frontier lab — he **self-funded it from a cash engine he built over a decade**. The lesson isn't "you can start a lab"; it's "build the capital/credibility engine first, lab second."

## Your actual ladder (compatible with the 900K mortgage and your family)

**Rung 1 — get hired by a Chinese frontier lab.** DeepSeek, Moonshot, MiniMax, Qwen, Zhipu, StepFun. This is the move that dominates everything else, and notice: it satisfies your wife and parents ("stay at a company") while putting you *inside* the frontier instead of adjacent to it at a bank. DeepSeek famously hires on curiosity and raw ability over credentials — Wenfeng has said this explicitly in interviews. Bank contractor → frontier lab engineer is a bigger career delta than bank → solo startup, and it pays you to build the exact skills on your list (MoE, RL post-training, inference systems).

**Rung 2 — build the application portfolio that gets you Rung 1.** Concretely, over the next 3–6 months on your MI300X:

- Implement a small DeepSeek-style MoE from scratch — MLA attention, aux-loss-free load balancing, shared + routed experts — at nanochat scale (~500M–1B params). Not a fork; from-scratch, with a Karpathy-style writeup on your blog explaining every design decision with math.
- Reproduce one post-training result: GRPO on a small model with verifiable rewards (math/code), showing the reward curves.
- One inference systems artifact: e.g., a paged KV-cache implementation or speculative decoding on the RTX 4070, benchmarked.

Three artifacts like this + your 8,000 notes + 400 posts is a stronger lab application than most master's degrees. This is exactly how Karpathy-lineage people get noticed: legible public artifacts.

**Rung 3 — the startup, later, is frontier-adjacent, not frontier.** Thinking Machines' first product, Tinker, is a fine-tuning API that lets developers customize open-source frontier models without managing distributed training — note that even a $50B lab's first revenue is *tooling on top of open models*, not a frontier model. When your mortgage hits 500K, the viable one-person-plus-agents startup is in that layer: post-training services, agent infrastructure, evals, inference optimization for open models (DeepSeek/Qwen weights are your raw material, free). That needs your 4070 and rented MI300X hours, not a $2B seed.

## The one-line strategy

Don't try to found the lab. **Join one, using open research artifacts as your credential — then, with lab experience + reduced mortgage + saved runway, found the frontier-adjacent company.** That's literally the Wenfeng sequencing (capital/credibility engine → lab) and the Karpathy sequencing (public artifacts → frontier lab → independent), compressed to your constraints.

If you want, next step: I can sketch the small-MoE-from-scratch spec (architecture, tokens budget for one MI300X, training schedule) as the first portfolio piece.

**References:**

- [New Frontier Lab Tracker: Thinking Machines, SSI, xAI 2026](https://presenc.ai/research/frontier-lab-tracker-thinking-machines-ssi-xai-2026)
- [Mirendil raises $200M to build AI that improves AI](https://thenextweb.com/news/mirendil-200m-seed-ai-research)
- [Frontier AI Labs Overview — Longterm Wiki](https://www.longtermwiki.com/wiki/E820)
- [Inside Thinking Machines Lab](https://builtin.com/articles/what-is-thinking-machines-lab)
