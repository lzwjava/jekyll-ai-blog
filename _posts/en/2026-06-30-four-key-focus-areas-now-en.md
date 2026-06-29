---
audio: false
generated: true
image: false
lang: en
layout: post
title: Four Key Focus Areas Now
translated: false
type: note
---

Question: What should I focus on recently?

Answer:

You didn't give me a specific task, so this is a check-in. Based on your stated trajectory, here's where your marginal hour pays off most right now:

**1. Finish the GPT-2 760M run, then write the post-mortem.** You're training on MI300X. The training itself isn't the lesson — the debugging artifacts are. Loss spikes, HBM3 utilization, ROCm-vs-CUDA gotchas, throughput numbers. That post-mortem is a high-signal blog post almost nobody else can write (ROCm training content is scarce). It compounds: credibility + your own reference + startup marketing.

**2. Pin down DeepSeek v4 MoE before chasing the next thing.** You listed it as "exploring." Concretely: implement a toy MoE router + top-k gating in ~80 lines, measure expert load balancing, then read the v4 architecture against your toy. Going from "I read the paper" to "I built the routing mechanism" is the gap that separates you from people who only consume content.

**3. Audit token spend → ROI.** 2B tokens/month is real money and real signal. Which of those tokens produced shipped artifacts vs. were burned on exploration that didn't compound? That audit is the same discipline as your energy accounting — apply it to inference too.

**4. Ship one of ww/iclaw/zz to 100 GitHub stars.** Per your own playbook (revenue experiments before launch), one of your CLI agents should get a real README, a demo GIF, and a Show HN / Hacker News post. Validation data > ambition.

If you tell me which one of these you want to move on today — or drop a different concrete task — I'll go deep and give you code, not a plan.
