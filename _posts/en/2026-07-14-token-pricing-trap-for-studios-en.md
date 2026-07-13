---
audio: false
generated: true
image: false
lang: en
layout: post
title: Token Pricing Trap for Studios
translated: false
type: note
---

Question: Model the token-economics of a 2–3 person AI-native dev studio (charging clients ~100 CNY/1M tokens for "prompt/architecture effort" on mini-programs, websites, apps), then project what happens to this business model as long-horizon agents mature.

Answer:

**1. First, the number that kills the "price by token" idea outright.**

Sonnet 5 is currently $2/$10 per M tokens (intro, through Aug 2026); real agentic coding sessions run ~70-80% cache hit rate, so blended cost lands around $4/M — **~29 CNY/M tokens raw compute cost**. Against a 100 CNY/M client price that's a 71% gross margin on the token line item alone. Looks great until you check volume:

```
Project                                Tokens(M)  Rev@100CNY/M   China market rate   Tokens needed to match market
mini-program (template-tier)              5.5         550 CNY        14,000 CNY            140M
mini-program (custom)                    14.0        1,400 CNY       50,000 CNY            500M
marketing site + CMS                     10.0        1,000 CNY       32,500 CNY            325M
cross-platform app (client+backend)      55.0        5,500 CNY      190,000 CNY          1,900M
```

A real small mini-program build via agent (spec → codegen → debug loop → docs) burns maybe 5-15M tokens. Chinese market rate for the same custom mini-program is typically 20,000 CNY at minimum, sometimes reaching over 100,000 CNY for complex projects. To make 100 CNY/M tokens hit that market price you'd need 140-500M tokens on a project that's actually a few million. **The only way to hit revenue targets is to burn more tokens than the task needs** — bloated context, redundant agent loops, over-verbose specs. That's just the billable-hour trap wearing a token costume: it rewards inefficiency and punishes the engineer who solves it in fewer calls.

**Conclusion: don't price the deliverable in tokens. Use tokens as your internal COGS metric, and price the deliverable at market rate (or a discount to it).** Compute is no longer your cost driver — it's rounding error.

**2. What that means for a 2-person studio:**

```
Monthly burn (2 people @ 25k CNY draw + 8k overhead):  58,000 CNY
4 concurrent projects @ 25,000 CNY avg (30-50% below
  traditional agency rates, still market-anchored):   100,000 CNY revenue
Token COGS across all 4 projects:                       1,600 CNY (1.6% of revenue)
Net profit:                                            40,400 CNY/mo  (~40% net margin)
```

The constraint isn't typing speed anymore — a traditional shop needed 5-10 devs to run 4 concurrent mini-program/website builds; you need 2 people whose job is architecture, spec quality, and review, because the agent does the typing. That's the actual arbitrage: **same throughput, 1/3 to 1/5 the headcount, near-zero COGS.** You can underprice a 50-person outsourcing shop by 30-40% and still clear 40% net margin, because their cost floor is payroll and yours is API calls.

**3. The "client deeply joins" partner case:**

Since your marginal cost per project is ~1-2% of the fee, the profitable move isn't maximizing token markup — it's maximizing deal flow and reducing your own review burden. Two structures work:
- **Reduced cash + rev-share/equity**: client puts up domain knowledge + real user feedback loop, you put up engineering + agent orchestration, split ongoing revenue (GMV cut, subscription %) instead of a flat fee. Makes sense when the client is doing something you believe will actually get traction — you're underwriting some of the build cost with upside.
- **Retainer, not one-off fee**: since agents make revisions nearly free, bill monthly for "keep shipping and maintaining this" rather than a fixed-scope contract. Aligns incentives — you're not penalized for shipping fast, and you capture ongoing value instead of a single payout.

**4. Long-horizon agent maturity — where the business model actually breaks:**

Right now you're still the bottleneck reviewing every diff. Once agents run multi-day autonomous cycles (spec → build → test → deploy → iterate against real metrics) with only milestone-level human checkpoints:

- **Headcount leverage keeps compounding** — a 2-3 person team stops managing "4 projects" and starts managing a *portfolio* of running agent fleets across many clients, checking in weekly instead of reviewing PRs daily. This is closer to "agent-ops" than "software dev."
- **Project-fee pricing collapses further** — if a client can point Claude Code / Cowork at their own repo and get 80% of the way there themselves, the fee for pure implementation trends toward the token cost (near zero). The traditional 20k-500k CNY mini-program market gets hollowed out from the low end first — anyone doing "template + light customization" work is directly exposed.
- **Value shifts to judgment, not code** — what a client actually pays for becomes: knowing what to build, what NOT to build, catching the agent's wrong assumptions before they compound over a week of autonomous work, and being accountable when it breaks in production. This is exactly the Karpathy/Wenfeng-style bet: small teams with high judgment density beat large teams with high headcount, because judgment doesn't parallelize the way typing does.
- **Practical move**: position now as the "trusted operator" layer — infra decisions, data/privacy calls, taste on UX and business logic, and the relationship — not as a code shop. Price on outcomes (retainer + rev-share) rather than tokens or even project fees, because by the time long-horizon agents are mature, tokens will be too cheap to itemize and project fees will be under constant deflationary pressure from clients who can partially self-serve.

References:
- [Anthropic Claude Platform Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [AI Coding Costs 2026 — token math, Claude vs Codex vs Gemini](https://www.morphllm.com/ai-coding-costs)
- [微信小程序开发报价指南 2026 - 知乎](https://zhuanlan.zhihu.com/p/2017906562824447318)
- [2026 小程序开发多少钱 - 鲸弘科技](https://www.vi23.com/list_4/331.html)
