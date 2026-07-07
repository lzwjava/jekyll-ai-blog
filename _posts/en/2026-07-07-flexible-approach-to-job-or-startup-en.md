---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flexible Approach to Job or Startup
translated: false
type: note
---

**Question:** I'm interviewing for a Java backend role at Standard Chartered (~400K CNY) while also transitioning out of my current job, researching company registration, and studying GPT-3 pretraining. Should I take the job or commit to the AI startup? What do you think of my flexible approach?

**Answer:**

The flexibility is the right instinct, not a contradiction. You've already stated your own decision rule clearly: at 500-600K/year you wouldn't quit to found a company. That's a real threshold, so use it. 400K is below it but within negotiating distance — which means the SC interview isn't a distraction from the startup, it's price discovery on your own time.

A few direct reactions:

**The math favors taking a good offer right now.** Your stated survival number is ~25K CNY/month. 400K pre-tax covers that roughly 2.4x, with zero client-acquisition risk. Your consulting pipeline is currently unproven — no signed high-end client yet, family opposed, 900K mortgage. A salary that funds mortgage + GPU time + 20% side experiments is not the death of the startup; it's runway you don't have to raise. Wenfeng Liang ran High-Flyer for years before DeepSeek. The employed-researcher path is a legitimate route to founding, not a detour from it.

**But the "join then quit in a month" idea is the one genuinely bad move here.** The banking/finance contractor circle in Guangzhou–Shenzhen–HK is small, and vendors track this. You've already worked one global bank contract; burning SC after 30 days can follow you into exactly the Phase-1 client market (GBA + HK financial institutions) you're targeting. If you take it, plan for 12+ months or don't take it. Interviewing while undecided is fine; joining while planning to bolt is reputation debt at high interest.

**Java backend is a money role, not a growth role — price that in.** It won't advance the transformer/MoE/training trajectory at all. So the real trade is: 40 hours/week of technically stagnant work in exchange for financial safety and evening/weekend research. That trade is acceptable at 2023-skill-level; it becomes a bad trade once you're at the frontier, because frontier skills decay fast if unused. Ask in the interview whether there's any AI-adjacent work internally — banks are all building LLM tooling now, and an internal transfer beats an external Java box.

**On the "40% Karpathy, ~2023 level" self-assessment — that calibration is actually your most valuable asset right now.** Most people can't self-assess honestly. But be precise about what the gap is: 2023-level means you understand attention, KV cache, fine-tuning, nanoGPT-scale pretraining. What the market pays frontier rates for in 2026 is different: RL infrastructure (GRPO at scale, reward modeling), MoE training stability (router load balancing, expert parallelism), inference systems (speculative decoding, paged attention, disaggregated prefill/decode), and agent evaluation. GPT-3 pretraining study is good foundation work, but note it's a 2020 artifact — the faster path to billable expertise is probably finishing nanochat end-to-end and then reproducing one modern component (e.g., a small MoE with aux-loss-free load balancing, DeepSeek-style) and writing it up publicly. That's a portfolio piece a bank job can't give you and consulting clients will actually pay against.

**Concrete decision rule I'd propose:** Take the SC process seriously and negotiate hard toward 450-500K. If the final offer plus your honest read of workload lets you keep 15+ hours/week of deep research, take it and run the startup as a nights-and-weekends entity (register the company anyway — it costs little and lets you invoice side projects). Flip to full-time founder only when trailing 3-month consulting revenue exceeds the monthly salary equivalent. That converts "world is changing, I stay flexible" from a vibe into a mechanism.

And yes — 交接、注册调研、训模型、下厨房 is a perfectly good week. The cooking might be the highest-ROI item for the family-persuasion problem, honestly. Numbers convince eventually; dinner convinces tonight.
