---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimal Use of 1M CNY for AI Startup
translated: false
type: note
---

Question: If I had an extra ~1,000,000 CNY, how should I prioritize spending it across GPU compute/LLM tokens/Nvidia stock, paid AI courses, consulting with real AI founders, and Hong Kong visa/company/degree study — given my mortgage-first startup playbook? My situation is a bit better now, not desperate-mode, so I can go all-in rather than rationing every "digital employee."

Answer:

Good, this is a real capital allocation problem, not a fantasy list. Let me rank it by expected return on *your specific* trajectory (AI engineering mastery + startup optionality unlocked at 500K mortgage), not generic "what would a rich person buy."

**TL;DR ranking:**

| Priority | Item | Amount | Why |
|---|---|---|---|
| 1 | Mortgage paydown | 400K CNY | Guaranteed risk-free return = your mortgage rate. Directly shortens time-to-500K-threshold, i.e., time-to-startup-permission. |
| 2 | HK Ltd company + banking | ~15K HKD (~14K CNY) | Cheapest, highest-leverage unlock — see below |
| 3 | Compute (rented, not bought) | 150K CNY | Funds ~2-3 years of serious training runs at current burn |
| 4 | Real founder access (paid, selective) | 50-80K CNY | Only if it's operator-level, not guru-course-level |
| 5 | Paid courses | 0-5K CNY | Skip almost entirely — you're past this |
| 6 | HK degree/study visa | 0 CNY (deprioritize) | Low ROI for you specifically — explained below |
| — | Nvidia stock | 0 CNY | Wrong tool for this goal |

**1. Mortgage paydown — 400K CNY, non-negotiable top slot**

This isn't "boring," it's math. Every yuan here earns your mortgage interest rate, risk-free, tax-free, and — critically — it's the *only* line item that moves your "startup permission" date. Your own playbook already says startup viability triggers at 500K remaining. 900K → 500K in one move means the 1M windfall doesn't just buy you tools, it buys you the *green light itself*. Nothing else on this list does that.

**2. Hong Kong Ltd — ~9,500–15,000 HKD, second priority despite being cheap**

Skip the "study in HK" angle entirely and go straight to the structural unlock: a Hong Kong private limited company. As of 2026, mandatory government fees are HK$3,895 for a 1-year Business Registration Certificate, and a realistic full incorporation setup — including registered address and company secretary — averages around HKD 9,474, with average annual maintenance around HKD 10,110. That's ~9-15K HKD to set up, ~10K HKD/year to maintain.

Why this matters more than a degree: Hong Kong doesn't require local directors and allows the entity to be 100% foreign-owned, and it gives you USD/HKD multi-currency banking, no mainland capital controls on that entity's revenue, and international payment processor eligibility (Stripe, Airwallex) that a mainland WFOE can't easily get. If your eventual product sells to global (USD) developers — which your own strategy already points toward — this is the actual infrastructure move, not a credential. Set it up *now* as a shell (dormant is fine, no audit needed if truly inactive), so it's ready the moment you have revenue to route through it. Cost is trivial relative to the optionality it buys.

**3. Compute — rent, don't buy, ~150K CNY**

You already have the right instinct with AMD Dev Cloud at ~$2/hr. Do the math before buying hardware: 150K CNY ≈ $21K USD ≈ 10,500 GPU-hours on MI300X on-demand. An actual MI300X card retail-equivalent cost plus the power/cooling/rack you don't have at home makes ownership strictly worse than renting unless you're running >50% utilization year-round, which you're not (you have a day job). Put the 150K into a pre-loaded cloud compute account (AMD Dev Cloud credits, or spread across AMD + a second provider for redundancy) and just burn it down on real training runs — nanochat-scale reproductions, your own MoE experiments, whatever moves your DeepSeek-v4-MoE understanding forward. Token spend (inference API calls for agent-building, eval, data generation) comes out of the same bucket.

**4. Nvidia stock — 0 CNY, wrong tool**

This is the one item that doesn't fit your goal at all. Buying NVDA is a generic macro bet on AI capex continuing — it doesn't make you better at AI engineering, doesn't fund your startup, doesn't reduce your risk. If you want equity exposure to the AI buildout, that's a separate "personal investing" bucket, not part of an AI-career-acceleration budget. Skip it here; if you want general equity allocation advice that's a different conversation (and I'm not a financial advisor — that one's genuinely "get your own view together" territory).

**5. Paid AI courses — near-zero**

You're training GPT-2 760M from scratch on real hardware and reading nanoGPT/nanochat source. Courses are for people who need structure and haven't started building. You've been building for years. The marginal course that's worth money for you is a genuinely novel *paper implementation* or a narrow technical workshop taught by someone who's shipped the exact thing you're trying to ship (e.g., a DeepSeek-alumni-run MoE training workshop, if one exists) — not a generic "AI for beginners" Coursera-tier product. If you find one like that, spend a few thousand CNY on it; otherwise this bucket stays empty.

**6. Consulting real AI entrepreneurs — 50-80K CNY, but gate it hard**

This can be genuinely high-value *if* you're buying access to someone who has actually shipped and monetized an AI product at your target scale (solo/small-team, AI-native, global market) — not a "AI business coach" who's never built anything. The test: would this person's Twitter/GitHub/product pass your own bullshit filter if a stranger sent it to you? If yes, a few paid 1:1 sessions or advisor-equity conversations are worth real money because they compress your mistake-discovery timeline. If the "AI entrepreneur" roster you're considering is influencer-tier, this money is better added to bucket #1 or #3.

**7. HK undergrad/associate degree — deprioritize to zero**

Be honest with the philosophy you already hold (Yin Wang, self-taught, first-principles): a credential doesn't compound for you the way shipped tools and public notes already do. The only version of "HK study" worth money is if it's explicitly a *visa/residency* play — e.g., using a study visa as a stepping stone toward HK residency for the banking/tax benefits above — but you get 90%+ of that structural benefit from the HK Ltd company alone, without tuition, without time cost, without living there. If residency itself becomes strategically necessary later (e.g., for a specific banking relationship or personal reasons), revisit it then as a standalone decision — don't bundle it into this budget now.

**Net effect of this allocation:** mortgage drops to 500K (startup-permission threshold hit), you have a dormant HK entity ready to receive global revenue the day you have a paying customer, ~2-3 years of compute runway funded, and you've spent almost nothing on credentials or passive equity bets that don't move your specific trajectory. That's "全力出击" without needing every digital employee on the payroll — the windfall itself does most of the work.

References:

- [Hong Kong Company Registration Cost Breakdown (2026)](https://sleek.com/hk/resources/company-registration-cost-hong-kong/)
- [How Much Does It Cost to Incorporate a Hong Kong Company? — Statrys](https://statrys.com/hk/guides/company-formation/costs-to-incorporate-a-company)
- [Hong Kong Company Formation 2026: Compare 8 Top Providers](https://growacross.com/hong-kong/company-formation)
