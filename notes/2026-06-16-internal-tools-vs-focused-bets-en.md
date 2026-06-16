---
audio: false
generated: true
image: false
lang: en
layout: post
title: Internal Tools vs Focused Bets
translated: false
type: note
---

**Question:** Are large corporations inefficient by building internal tools that serve only thousands of employees, while startups like Revolut beat traditional banks by concentrating bets? Should software strategy favor one big focused shot over scattered internal tooling?

**Answer:**

You're touching something real but the picture is more nuanced than it looks.

---

## Where You're Right

**Internal tooling sprawl is genuinely wasteful.** A bank with 80k employees might have 400 internal apps, each with a team, infra, on-call rotation, and compliance overhead. Most of these serve 2k-10k users. The ROI per engineer is terrible compared to a product serving millions.

**Revolut's leverage is real.** They have ~10k engineers serving 45M+ customers. A legacy bank might have 50k IT staff serving 10M customers. The output-per-engineer ratio is 10-50x worse at the incumbent. That's the compounding advantage of building one coherent platform instead of 400 siloed systems.

**Concentration of bets compounds.** Every Stripe engineer improving the payments API improves the experience for millions of businesses simultaneously. Every internal-tooling engineer at a big corp improves the experience for maybe 500 colleagues. The leverage gap is enormous.

---

## Where It's More Complex

**Internal tools often can't be replaced by SaaS** — not because IT is incompetent, but because:

- Regulatory constraints (data residency, audit trails, FIPS compliance)
- Integration with decades-old core systems (mainframes, COBOL ledgers)
- Business logic so specific that no vendor will build it

Goldman's risk engine, JPMorgan's trade settlement system — these aren't internal tools that could be replaced by Notion or Jira. They're the actual product differentiation buried inside.

**"One big bet" has survivorship bias.** Revolut succeeded. Dozens of neobanks didn't. The strategy looks brilliant in hindsight. For every Revolut there are 20 Monzos-that-never-scaled, Finn-by-Chase shutdowns, Google Stadia equivalents.

**Org size changes the calculus.** At 100k employees, even a "small" internal tool serving 5k engineers on the critical path (say, the internal deployment system) has massive leverage — because those engineers ship the revenue-generating product. The inefficiency isn't the tool existing; it's having 12 teams build 12 overlapping versions of it.

---

## The Actual Inefficiency

The waste at big corps isn't "internal tools exist." It's:

1. **No consolidation incentive** — teams own budgets, not outcomes. Building a new tool is easier than adopting someone else's.
2. **NIH syndrome** — "Not Invented Here." Every team rebuilds auth, logging, dashboards from scratch.
3. **No usage accountability** — a tool serving 200 users with a 4-person team never gets killed because no one measures ROI.
4. **Conway's Law in action** — org structure produces system structure. Siloed orgs produce siloed tools.

Revolut avoids this because they're org-flat enough that platform teams are forced to serve the whole company, not their fiefdom.

---

## The Right Mental Model

Think in terms of **leverage per engineer** not "internal vs external":

| Type | Users per eng | Leverage |
|---|---|---|
| Stripe payments API | millions | very high |
| Internal deploy tool used by 5k devs | 5k | medium (multiplier on other eng) |
| Internal HR portal used by 500 | 500 | low |
| Internal report nobody reads | 10 | negative |

The Revolut insight isn't "don't build internal tools" — it's **build fewer things, serve more people per thing, kill what has no leverage.**

In AI terms: you want **one foundation model** fine-tuned for many tasks, not 400 bespoke models each trained on 10k examples. Same principle.

---

For your trajectory specifically — the tools you're building (ww, iclaw, zz) are high-leverage *because* they're multipliers on your own output. That's the right instinct. The question to ask about any tool is: **does this compound, or does it just serve?**
