---
audio: false
generated: true
image: false
lang: en
layout: post
title: Copilot's Premium Request Multipliers Explained
translated: false
type: note
---

**Question:** Why does Claude Opus 4.7 show 15x and Gemini 3.5 Flash show 14x premium request multipliers in GitHub Copilot?

**Answer:**

This is GitHub Copilot's **premium request multiplier** system — a token-cost normalization mechanism baked into the Copilot subscription model.

## How Copilot's Premium Request System Works

Copilot Pro+ gives you a fixed monthly budget of **1,500 premium requests**. Each model costs a different number of those credits per invocation, expressed as a multiplier. So at 15x, one Opus 4.7 turn costs 15 credits, leaving you ~100 turns/month from your base allotment.

The multipliers roughly track the underlying API token cost of each model. GitHub is essentially passing through model pricing as a normalized rate, then adding margin.

## Specific Models

Claude Opus 4.7 launched with a 7.5x promotional multiplier, which ended April 30th — after which the multiplier jumped to **15x**.

Gemini 3.5 Flash launched at **14x**, though GitHub notes the pricing is tentative and subject to change.

## Why These Numbers Are Surprising

The counterintuitive part: "Flash" in Gemini's branding implies fast/cheap, but in Copilot, the model launches with a 14x premium multiplier — a "Flash" badge in Copilot doesn't mean cheap.

Similarly, Opus 4.7 at 15x is brutal: at 15x, the 1,500-credit Pro+ allowance drops to ~100 Opus 4.7 turns; at 30x (a rumored future rate), to ~50 — fewer than two agentic sessions involving context gathering, generation, and retry loops.

## Community Reaction

Users are pointing out that at 15x post-promo, it's cheaper to just use Claude Code with the Pro plan and work around the rate limiter, or switch to Codex.

## Practical Takeaway for You

Given your usage pattern (top 6% in AI assistant usage at the bank), Copilot's premium system is likely a bad deal at these multipliers for heavy users. The math:

| Option | ~Cost for heavy Opus use |
| --- | --- |
| Copilot Pro+ ($39/mo) + 15x multiplier | ~100 Opus turns/mo |
| Claude Pro ($20/mo) or API direct | Much higher limits |
| Claude Code ($100/mo Max plan) | Highest limits, no per-turn tax |

For agentic workflows especially, the Copilot multiplier system penalizes you heavily since each tool call in a multi-step agent counts separately.

**References:**

- [Claude Opus 4.7 is generally available - GitHub Changelog](https://github.blog/changelog/2026-04-16-claude-opus-4-7-is-generally-available/)
- [Gemini 3.5 Flash is generally available for GitHub Copilot - GitHub Changelog](https://github.blog/changelog/2026-05-19-gemini-3-5-flash-is-generally-available-for-github-copilot/)
- [Opus 4.7 now 15x? - GitHub Community Discussion](https://github.com/orgs/community/discussions/194470)
