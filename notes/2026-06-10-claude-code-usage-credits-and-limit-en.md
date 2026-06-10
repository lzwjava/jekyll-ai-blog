---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code usage credits and limit
translated: false
type: note
---

**Question:** How does the `/usage-credits` command and the monthly limit work in Claude Code?

**Answer:**

`/usage-credits` controls the *overflow* spending layer, not your plan's included usage. The mental model is three tiers:

1. **Included plan usage** — your Pro/Max subscription gives you a quota governed by a 5-hour session window and a 7-day weekly cap, and claude.ai chat, the Desktop app, and the Claude Code CLI all draw from the same budget. This part is flat-rate; nothing you set with `/usage-credits` touches it.

2. **Usage credits (pay-as-you-go overflow)** — when you exhaust the included quota mid-session, instead of being blocked, requests start billing against a prepaid credit balance at standard API rates, charged separately from your subscription. You enable and fund this in Settings > Usage on claude.ai — enable usage credits, add a payment method, then prepay funds via "Add funds".

3. **The monthly limit you just set ($10)** — this is a spend cap on tier 2. On Pro and Max plans, `/usage-credits` sets a monthly spend limit on usage credits. If you hit that limit while you still have credit balance available, Claude Code prompts you to raise or remove the limit so you can continue without leaving the CLI. Changing the limit requires billing access on the account.

So concretely: your subscription quota burns down as normal → quota exhausted → overflow billing kicks in at API token rates → once $10 of overflow has accrued this calendar/billing month, Claude Code stops and asks you to bump the cap. It's a circuit breaker, not a budget you're committing to spend. The limit resets monthly; the prepaid balance itself persists until spent.

Two things worth knowing as a heavy user:

- **Bundles**: if you expect to overflow regularly, pre-purchased usage bundles are discounted up to 30% vs standard usage-credit rates, with bigger bundles giving bigger discounts, and the balance pools across Claude, Claude Code, Cowork, and third-party products.
- **Separate programmatic pool**: starting June 15, 2026, Agent SDK and `claude -p` usage stops counting against your plan limits and instead draws from a separate monthly Agent SDK credit — interactive Claude Code in the terminal stays on your normal plan quota. So if you're scripting headless `claude -p` pipelines (very your style), that's metered differently from your `/usage-credits` cap. When that SDK credit runs out, additional usage flows to usage credits at API rates only if you've enabled them; otherwise SDK requests stop until refresh.

Quick checks from the CLI: `/usage` shows your session/weekly bars and resets, `/cost` shows current-session token spend.

**References:**

- [Manage costs effectively — Claude Code Docs](https://code.claude.com/docs/en/costs)
- [Manage usage credits for paid Claude plans — Claude Help Center](https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans)
- [Buy usage bundles — Claude Help Center](https://support.claude.com/en/articles/14246112-buy-usage-bundles)
- [Use the Claude Agent SDK with your Claude plan — Claude Help Center](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)
