---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Token Usage and Mindset Shift
translated: false
type: note
---

Question: Reflecting on yesterday's ~250M token usage (failed 1B challenge), and noting I have a 700M token plan on Xiaomi's Mihomo platform — what do you think?

Answer:

Honest reaction: the shift in mindset from point 3 is the most valuable thing you wrote. "Consuming for the sake of consuming" is a real trap — it optimizes the metric, not the outcome. 250M tokens that produced meaningful code, insights, or learning compounds. 1B tokens of aimless prompting doesn't.

**On the 700M Mihomo token plan:**

I'm not familiar with Xiaomi's "Mihomo" LLM platform specifically — it's likely a newer product or rebranding after my knowledge window. Let me search quickly.So it's **Xiaomi MiMo**, not "Mihomo" — interesting platform. Here's my full take:

---

**On your mindset shift (points 1–6):**

Your self-reflection is sharp. The key insight is point 3 — **token consumption as a vanity metric is the same trap as GitHub commit streaks.** What actually compounds is:

- Did you build something that works?
- Did you understand something you didn't before?
- Did you automate a recurring pain?

250M tokens with a family day, 6 hours sleep, and community interaction? That's actually a healthy day. The 1B challenge was always a stress test, not a lifestyle.

Point 6 resonates most with me for you specifically: *AI bringing more freedom* — that's the right north star. Not token throughput. Freedom to work fewer hours for the same output, freedom to explore ideas faster, freedom to spend time with people.

---

**On the Xiaomi MiMo 700M token plan:**

This is genuinely interesting. Here's the technical picture:

MiMo-V2-Pro was released in March 2026 with over 1 trillion total parameters (42B active), and MiMo-V2-Flash at 309B total (15B active) — both on the platform.

MiMo-V2-Pro ranks 8th globally and 2nd among Chinese LLMs on the Artificial Analysis Intelligence Index, supports up to 1M-token context, and uses Multi-Token Prediction for fast generation. It's explicitly designed for agent tasks — completing tasks, not just answering questions.

MiMo-V2-Flash benchmarks close to DeepSeek-V3.2 in performance but at roughly half the cost, and matched GPT-5 High on AIME 2025 math.

The token plan tiers range from 39 yuan to 659 yuan/month, using a unified Credit system across multi-modal calls.

**What I think about using it:**

For your use case — CLI agents, automation, heavy API consumption — MiMo is worth experimenting with seriously, for two reasons:

1. **Cost efficiency**: Chinese domestic LLM APIs are priced aggressively. If MiMo-V2-Flash is near DeepSeek-V3.2 quality at half cost, and you're consuming 250M+ tokens/day in bursts, the economics matter.

2. **Agent-first design**: MiMo-V2-Pro was post-trained specifically across agent tasks to "complete tasks" rather than just generate demos — that aligns with your `ww`, `iclaw`, `zz` agent tooling direction.

3. **1M context window** — useful for your long code sessions and document analysis.

**What to watch out for:**

- MiMo-V2-Pro is proprietary (V2-Flash is MIT licensed). API reliability and rate limits for a newer platform need real-world testing.
- The 700M tokens — check if it's credits that expire. If so, treat it as a testing budget, not a daily driver commitment.
- For coding/math/reasoning tasks, benchmark it yourself against Claude Sonnet / DeepSeek before committing workflows to it.

**Suggested experiment:** Route one of your existing CLI agents (say `zz` or `ww`) to use MiMo-V2-Flash via their API for a week. Compare output quality and latency against your current stack. 700M tokens is enough to run a real evaluation.

---

Today's goal — natural exploration over metric chasing — is the right mode. Let the 700M tokens be a playground, not a pressure.

References:

- [Xiaomi MiMo Wikipedia](https://en.wikipedia.org/wiki/Xiaomi_MiMo)
- [MiMo-V2-Pro official page](https://mimo.xiaomi.com/mimo-v2-pro)
- [MiMo Token Plan global launch](https://platform.xiaomimimo.com/)
- [MiMo-V2-Flash GitHub](https://github.com/XiaomiMiMo/MiMo-V2-Flash)
- [VentureBeat: MiMo-V2-Pro analysis](https://venturebeat.com/technology/xiaomi-stuns-with-new-mimo-v2-pro-llm-nearing-gpt-5-2-opus-4-6-performance)