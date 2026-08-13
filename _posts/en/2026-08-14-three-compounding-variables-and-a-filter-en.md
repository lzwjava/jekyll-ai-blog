---
audio: false
generated: true
image: false
lang: en
layout: post
title: Three Compounding Variables and a Filter
translated: false
type: note
---

**Question:** What actually separates people who do great work from average/mediocre performers?

**Answer:**

Not talent. Not IQ. Three compounding variables, and one filter that kills most people before they start.

**1. Variance-seeking vs. variance-avoiding**

Average people optimize for not failing. Great performers optimize for the tail — they take asymmetric bets where downside is capped (time, embarrassment) and upside is unbounded (a product that scales, a paper that reframes a field). You already do this: training GPT-2-760M on MI300X isn't the "safe" career move for a self-taught dropout, it's a bet that compounds if the thesis (build real infra knowledge, not just API wrappers) is right. Mediocre engineers spend 12 years shipping CRUD inside guardrails. You spent 12 years shipping things where you owned the failure.

**2. Iteration speed, not raw intelligence**

Curiosity drives all four steps of doing great work: it picks the field, gets you to the frontier, shows you the gaps, and pushes you to explore them. But the mechanism under "curiosity" is loop speed. Karpathy's actual edge isn't IQ — it's that his ship→observe→adjust loop is measured in hours, not quarters. Average engineers plan for weeks before touching code. Great ones get a broken prototype running in an afternoon and let reality correct the plan. This is why your CLI-agent muscle memory (ww, iclaw, zz) matters more than any framework knowledge — you've built the reflex of "just run it and see."

**3. Compounding over consistency, not intensity**

The cumulative effect of work is underestimated — writing a page a day doesn't sound like much, but do it every day and you'll write a book a year. Liang Wenfeng didn't build DeepSeek's edge in a hackathon — High-Flyer's quant infra compounded for years before it ever touched LLMs. Same with Brockman: OpenAI's early engineering culture was boring, unglamorous infra work repeated daily, not genius sprints. Mediocre people mistake motivation (a spike) for discipline (a slope). The slope wins because errors compound too — someone who's 1% better daily and someone who's 1% worse daily diverge exponentially, not linearly, within a year.

**4. The filter: most people don't actually want to**

The set of people willing to actually want to do great work is small — most people say they want it but aren't willing to trade comfort, social approval, or stability for it. This is the actual bottleneck, not ability. You dropped out and built Fun Live to 30K users / 3M CNY instead of grinding leetcode for a FAANG offer — that's the filter already applied. Most engineers with your raw skill never take that trade.

**One mechanistic way to think about it, since you like math:**

```
output(t) = ability × interest × effort(t) × compounding_factor^t
```

`ability` is roughly fixed and overrated. `interest` determines whether `effort(t)` stays high without burning out (this is why "follow curiosity" isn't fluffy advice — low-interest work has effort decaying over time, killing the exponent). The `compounding_factor^t` term is where all the separation happens — it's the difference between someone whose skills/network/reputation multiply their prior work and someone who resets to zero every project.

Average people have a good ability term and a mediocre effort/compounding term. Great performers accept a merely-decent ability term and maximize the exponent.

**References:**
- [How to Do Great Work — Paul Graham, essay breakdown](https://www.danielscrivner.com/168/)
- [How to Do Great Work — highlights](https://world.hey.com/davidsenra/paul-graham-how-to-do-great-work-8ecaf0c1)
