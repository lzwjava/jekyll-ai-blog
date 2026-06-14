---
audio: false
generated: true
image: false
lang: en
layout: post
title: Smaller High-Trust Teams with AI
translated: false
type: note
---

**Question:** Will future teams be smaller and higher-trust, with more Individual Contributors, as AI agents replace slow human communication overhead?

**Answer:**

Yes, and this is already happening — but the dynamics are more nuanced than just "fewer people."

## The Core Shift

The fundamental unit of leverage is changing. Previously:

- **Leverage came from coordination** — more engineers → more parallelism → more output
- **Communication overhead scaled quadratically** (Brook's Law: n² channels for n people)
- **Management layers existed to compress that coordination cost**

Now:

- **Leverage comes from AI amplification** — one engineer with good agents > five without
- **AI agents are synchronous, context-rich, don't need standups**
- **The bottleneck shifts from headcount to taste, judgment, and system design**

## What "Smaller + High Trust" Actually Means

**Small** isn't just headcount — it's **decision surface area**. High-trust teams eliminate:

- Status update meetings (AI maintains state)
- Code review bottlenecks (AI does first-pass, humans approve architectural decisions)
- Onboarding ramps (AI knows the codebase, new IC is productive day 1)
- Spec-to-impl translation (IC talks directly to the system)

**High trust** becomes tractable because AI makes output verifiable cheaply. You don't need to trust someone's word on "it's done" — you run evals, you see the diff, agents generate test coverage automatically. Trust is anchored to **output + verifiability**, not tenure or politics.

## IC Resurgence

Big corps went management-heavy because coordination was expensive and individual output was hard to measure. Both of those are now reversing:

- **Individual output is increasingly measurable** — AI-assisted throughput is trackable, evals are automatable
- **Coordination cost drops** — agents maintain shared context, async is the default
- **The "10x engineer" becomes real and legible** — previously dismissible as myth, now demonstrably true when one person with good agent infrastructure ships what a team used to

You're already living this. Your `ww`, `iclaw`, `zz` CLI agents, your 1B token/month workflow — that's not unusual productivity, that's what the high-leverage IC looks like. Companies will hire fewer people who work like that instead of many people who don't.

## What Big Corps Actually Do

They won't restructure cleanly — they'll do it messily:

- **Layer AI on top of existing bloat** first (Microsoft/GitHub Copilot, internal GPTs)
- **Hiring freezes + attrition** replace headcount reduction announcements
- **New orgs spun out lean** while legacy orgs stay fat until they're deprecated
- **IC titles inflate** — "Staff AI Engineer" becomes the new "Senior Manager" in terms of actual leverage

The honest version: the next Stripe, Linear, Vercel, or Cursor will be built by 10-20 people doing what 200 used to do. That's the competitive threat that forces big corps to eventually follow.

## Human Communication Isn't Gone — It's Curated

The part that's slow and unnecessary: status sync, approval chains, ambiguity resolution on well-specified problems.

The part that stays irreplaceable:
- **Taste and vision** — what to build, what matters
- **Conflict on values** — what the product *shouldn't* do
- **Novel problem framing** — when the spec itself is wrong
- **Trust-building for high-stakes decisions** — M&A, pivots, firing

The ratio of "humans talking to humans" vs "humans directing agents" flips. Human conversation becomes a **premium, high-signal activity** rather than the default coordination mechanism.

## For You Specifically

You're positioning correctly. The IC who can:
1. Design agent systems, not just use them
2. Run evals and measure output quality
3. Train/fine-tune models for specific workflows
4. Compress what used to need a team into a tight pipeline

...is the most valuable hire or founding team member in 2025-2030. The "AI Engineer" role you're building toward is exactly the IC profile that survives and thrives in this transition.

The engineers who get squeezed are the ones whose primary value was **coordination and communication** — PMs who translated between business and eng, engineers who existed to review other engineers' work, managers who existed to maintain alignment. Those roles hollow out first.
