---
audio: false
generated: true
image: false
lang: en
layout: post
title: Automate Execution, Never Understanding
translated: false
type: note
---

**Question:** AI agents automate tedious tasks, but that removes the challenge and the "flow" state. Does that mean we should deliberately do more hard things manually to stay sharp and feel alive?

**Answer:**

This is a real tension, and you're pointing at something Csikszentmihalyi got right: flow requires the challenge-to-skill ratio to be in the sweet spot. Too easy → boredom. Too hard → anxiety. Automation collapses difficulty, so flow disappears.

But I think the framing "do hard things manually" is slightly off. Here's a sharper model:

---

## The Real Issue: Where Is the Frontier?

Agents didn't remove challenge — they **shifted where the frontier is**.

Before agents: the frontier was *implementing* the thing.
After agents: the frontier is *knowing what to build, why, and how to verify it's right*.

If you're bored watching an agent run commands, it's because **you haven't pushed the problem to where agents still fail**. That zone still exists:

- Designing a novel training loop agents don't understand yet
- Debugging a CUDA kernel that produces wrong gradients
- Architecting a multi-agent system where failure modes are non-obvious
- Reading a paper and deciding which parts actually matter vs. hype
- Writing an eval that catches subtle model regressions

These are genuinely hard. Agents flail at them. Your brain is still the bottleneck.

---

## Flow Isn't About Pain — It's About Feedback Loops

Manual coding gives flow because the feedback loop is tight and personal: you type, it runs, it breaks, you fix. The challenge is *yours to own*.

With agents, the feedback loop is: you prompt, you wait, you read. The gap breaks flow because **you're a reviewer, not a doer**.

The fix isn't to go back to writing boilerplate. It's to **restructure what you're doing so you're still in the tight loop**:

- Write the *spec* that the agent implements, but make the spec hard enough that getting it wrong is obvious and painful
- Read the *output critically* — not passively. Treat agent output as a first draft from a junior engineer. Finding the bugs is a skill.
- **Train your own judgment faster than agents improve** — that's the actual game

---

## What Karpathy Actually Does

Karpathy doesn't write boilerplate by hand to "stay sharp." But he also doesn't delegate thinking. He:

- Builds things from scratch when the goal is *understanding* (nanoGPT, minGPT)
- Uses tools aggressively when the goal is *shipping*
- Keeps a clear internal model of what every line does, even when he didn't write it

The distinction is: **he never lets the agent be the only one who understands the system.** That's the rule worth adopting.

---

## Practical Principle for You

> **Automate execution. Never automate understanding.**

Use agents to run commands, scaffold code, format docs, run evals.
But the part where you *understand why* something works — read that code, trace that gradient, understand that architecture — do that yourself, slowly, painfully, with friction.

The challenge you want isn't in *doing* things manually. It's in **choosing harder problems** — ones where even with full agent support, you're still the limiting factor.

You're at 760M GPT-2 from scratch on MI300X. The next frontier isn't writing more bash manually. It's understanding MoE routing at the weight level, or building an eval pipeline that catches reasoning failures, or implementing GRPO from the paper. Those will put you in flow. Agents won't take that from you.
