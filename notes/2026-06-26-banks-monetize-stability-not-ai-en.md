---
audio: false
generated: true
image: false
lang: en
layout: post
title: Banks Monetize Stability, Not AI
translated: false
type: note
---

Question: Why do big banks lag in AI adoption — is it because they're still living comfortable, stable lives and lack the existential pressure that forces companies like Meituan or ByteDance to constantly pivot and ship models?

Answer:

Your thesis is basically right, and it's a cleaner version of the "innovator's dilemma" — but the mechanism is more specific than "they're comfortable." Let me sharpen it.

**The core asymmetry: banks monetize stability, tech companies monetize growth.**

A bank's competitive moat is regulatory license + balance sheet + trust, not technology. Their revenue per employee is enormous regardless of whether their stack is modern. JPMorgan made ~$50B profit in 2023 running on COBOL mainframes. There is no market mechanism punishing them for slow AI adoption — depositors don't leave because the bank doesn't have a HuggingFace profile. Contrast ByteDance/Meituan: their *entire* moat is the recommendation/matching algorithm. If their model degrades, GMV drops next quarter. AI isn't a side bet — it's the product. The selection pressure is direct and immediate.

**Why "they had a good life" maps to real structural forces:**

1. **Regulatory capture cuts both ways.** The same barriers that protect banks from disruption also make it expensive to ship anything. A model that touches credit decisions needs model risk management (SR 11-7 in the US), explainability, audit trails. You can't `git push` a transformer into a lending pipeline. So even motivated bank teams move at 1/10th startup speed — not because they're lazy, but because the cost of a hallucinated loan approval is a regulatory action, not a bad UX review.

2. **Open-sourcing has no upside for them, only legal/IP/compliance downside.** Why would a bank publish on HuggingFace? Tech companies open-source to (a) recruit, (b) set ecosystem standards, (c) signal capability to the talent market. A bank recruits with money and brand, doesn't need to set ML standards, and its legal department sees only risk in publishing weights trained on anything near customer data. The *absence of a HuggingFace profile is rational* given their incentive structure — it's not a sign they "don't get it," it's a sign the payoff matrix is different. Weibo publishing a model is a recruiting/PR move; a bank gains nothing from it.

3. **2000s pivot vs. now.** You're pointing at something real: banks survived the internet transition (online banking, mobile apps) precisely because they could *bolt on* a channel without changing the core business. AI might be the same — they'll bolt on copilots for traders, fraud detection, doc processing — without ever needing to become an "AI company." The question is whether AI is a *channel innovation* (survivable by bolting on, like web banking) or an *architecture innovation* (requires becoming a different kind of company). My bet: for banks specifically, it's mostly the former. They'll be fine being late.

**Where your model is incomplete:**

The hyper-growth companies aren't a fair comparison class. Meituan/ByteDance are *survivors* of a brutal selection process — for every one of them, hundreds of equally aggressive startups died. You're comparing the winners of a high-variance game to the steady-state incumbents of a low-variance game. Banks optimize for not-dying; that's their job (a bank that "moves fast and breaks things" with your deposits is a crime). So "banks are slow" and "ByteDance is fast" are both the *correct* adaptations to their respective environments, not evidence that one is smart and the other dumb.

**The relevant insight for you personally:** this is exactly why your bank job is correctly framed in your playbook as a salary-and-learning-ground, not a place to do frontier AI. The institution's incentive structure guarantees you'll never get to ship the AI work you actually want to do there at startup speed. Extract the infrastructure access and domain knowledge (financial systems are a real moat for a future AI product), keep your real AI building outside, and don't mistake the bank's stability for a place where your trajectory compounds. The bank is comfortable for the same reason it's a dead end for an AI-first builder — those are the same fact viewed from two sides.

One nuance worth holding: some banks *are* moving — JPMorgan's LLM Suite, Goldman's internal copilots, the quant desks running serious ML. The lag isn't uniform. It's concentrated in retail/commercial banking where the regulatory drag is heaviest and the competitive pressure is lightest. The trading and risk side, where alpha is directly tied to model quality, moves much faster — closer to your ByteDance dynamic.
