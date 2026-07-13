---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compute Cost Already Immaterial
translated: false
type: note
---

Question: Recompute the studio economics using DeepSeek V4 Flash as the compute backend instead of Sonnet.

Answer:

**Cost first:**

DeepSeek V4 Flash: $0.14/M input (cache miss), $0.028/M cache-hit input, $0.28/M output — no US-model FX or export-control dependency, MIT-licensed weights, 1M context. Blended for an agentic loop (85% input / 15% output tokens, 70% cache hit rate):

```
DeepSeek V4 Flash blended:  $0.094/M  =  0.68 CNY/M tokens
Sonnet 5 blended (prior):   28.8 CNY/M
                             -> 42x cheaper
```

**But it's not free — there's a quality tax.** Flash matches Sonnet/Opus tier on single-shot coding (SWE-bench Verified 79.0% vs frontier ~87-95%, LiveCodeBench 91.6%), but the gap widens on chained multi-step tool use and long-horizon agentic loops (GDPval-AA 1388 vs Pro's 1554), and it runs Terminal-Bench 2.0 at 56.9% vs Pro's 67.9% — the exact "run the CLI, iterate, debug, retry" loop your studio depends on for full project builds. It also carries a 96% hallucination rate when it doesn't know an answer, vs 94% for V4 Pro — it answers confidently instead of admitting uncertainty. Budget a retry/verification tax:

```
With 1.5x retry tax for agentic weakness: 1.02 CNY/M effective
Still 28x cheaper than Sonnet blended
```

**What this changes for the 4-project/month studio:**

```
Token COGS on Flash (4 projects, 14M tok each): 57 CNY  (0.057% of 100k revenue)
Token COGS was already only 1,600 CNY (1.6%) on Sonnet
```

The honest answer: **it barely moves your headline margin, because compute was already immaterial.** Going from 1.6% to 0.06% of revenue doesn't change your P&L. What it does change:

1. **Model routing, not model replacement.** DeepSeek's own guidance is explicit: default to Flash and escalate to Pro (or a frontier closed model) only when a specific task type fails your eval. Use Flash for the 80% of a mini-program/site build that's boilerplate — CRUD scaffolding, form generation, test writing, docs, repetitive refactors — and reserve Sonnet/Opus-tier calls for architecture decisions, the tricky multi-file agentic debugging loop, and anything client-facing where a hallucinated confident-wrong answer is expensive to catch late.

2. **Compute becomes so cheap you can spend it on robustness instead of saving it.** Since COGS is now a rounding error even at Sonnet prices, at Flash prices you can afford to generate 3-5 candidate implementations per feature, run exhaustive test-generation passes, and let agents retry-and-self-correct aggressively — buying reliability with tokens instead of buying it with your own review time. That's the actual lever: not cheaper projects, but the same project delivered with less human QA burden because you can throw 10x the token budget at self-verification for free.

3. **Non-cost reasons matter more here than price.** MIT license means self-hostable (no dependency on a foreign API being available — relevant given Claude Managed Agents billing changes and the general pattern of model access shifting under export-control/policy events this year), RMB-denominated cost exposure instead of USD, and no data leaving China if you self-host — a real consideration for client contracts with data-residency clauses.

4. **The retry tax is a live number you should measure, not assume.** 1.5x is a placeholder — run your actual mini-program pipeline on Flash vs Sonnet, log pass/fail on your own acceptance tests, and compute the real ratio. Given the margins involved (28-42x raw), Flash wins on almost any retry tax short of ~20-30x, which won't happen on the boilerplate-heavy work that's most of a mini-program build.

Net: DeepSeek V4 Flash doesn't change your business model — token cost was already a non-issue — but it does let you push agent autonomy further per human-hour of oversight, which is the actual constraint on how many concurrent projects 2-3 people can run.

References:
- [DeepSeek V4 Flash — Benchmarks, Pricing & Flash vs Pro](https://codersera.com/blog/deepseek-v4-flash-deep-dive/)
- [DeepSeek V4 Flash Review — CodingFleet](https://codingfleet.com/blog/deepseek-v4-flash-review-028-developer/)
- [DeepSeek V4 Flash — API Pricing & Benchmarks, OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-flash)
- [DeepSeek V4-Pro Review — permanent pricing, benchmarks](https://codersera.com/blog/deepseek-v4-pro-review-benchmarks-pricing-2026/)
