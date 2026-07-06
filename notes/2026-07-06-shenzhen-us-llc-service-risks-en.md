---
audio: false
generated: true
image: false
lang: en
layout: post
title: Shenzhen US LLC Service Risks
translated: false
type: note
---

**Question:** Is the ~1,800 CNY "register a US company" service advertised by Shenzhen agencies on 58同城 legit, and is it a good deal for a Chinese citizen?

**Answer:**

Short version: 1,800 CNY (~$250) is a plausible, roughly-at-cost price for **year one of a Wyoming/Colorado LLC**. It's not a scam per se — but the price is a loss-leader. The money is made on renewals, "annual review" upsells, and the fact that you'll be locked into them as your registered agent. The real risk isn't the 1,800 CNY, it's what they *don't* file for you later.

**Why 1,800 CNY is possible (cost breakdown, cheapest path = Wyoming LLC):**

| Item | Actual cost |
|---|---|
| Wyoming state filing fee | $100 (one-time) |
| Registered agent (required, in-state) | $25–50/yr wholesale |
| EIN (federal tax ID) | **$0** — IRS Form SS-4 by fax, free |
| US mailing address (virtual) | ~$10–30/yr wholesale |
| Total | ~$150–200 |

So the agency clears maybe 300–800 CNY margin. Legit registration services covering state fees + registered agent + EIN + address exist around $260–360 all-in, so 1,800 CNY is market rate, not suspiciously cheap.

**What they usually don't tell you — the actual traps:**

1. **Form 5472 + pro forma 1120, every year, or $25,000 penalty.** A US single-member LLC 100% owned by a non-US person must file Form 5472 annually even with zero income, and the penalty for not filing is $25,000 per year. Even just contributing capital or paying your registered agent fee counts as a "reportable transaction," so there's effectively no "inactive, don't need to file" state. The IRS now cross-matches US bank account data, so an LLC with bank activity but no 5472 on file can get flagged automatically. The 1,800 CNY package almost never includes this; the agency will quote you another 1,500–3,000 CNY/yr for it, or worse, never mention it.

2. **Ongoing costs.** Registered agent renewal (they'll charge 500–1,000 CNY/yr for the $25 wholesale service), Wyoming annual report ($60 min), address renewal. Real total cost of ownership: roughly 2,000–4,000 CNY/year forever, until you formally dissolve it (dissolution also costs money — abandoning it just accrues state fees and potential IRS penalties).

3. **Banking is the actual hard part**, and the LLC certificate alone doesn't solve it. Mercury/Relay/Wise policies toward mainland-China-resident founders shift frequently and have generally tightened. Some Shenzhen agencies bundle "包开户" (guaranteed bank account) — ask exactly *which* bank/fintech, because a Wyoming LLC without a working USD account is a paperweight. This is where cheap agencies fail most often.

4. **China-side compliance.** Individual outbound investment technically touches SAFE Circular 37 (37号文) registration territory if the entity holds assets or raises money. For a small SaaS/e-commerce shell almost nobody registers, but know that it exists — especially if the entity ever becomes your startup holding vehicle with real revenue flowing back.

**My honest take for your situation:**

If your goal is Stripe access / selling AI tools or SaaS to US customers (which fits your startup-optionality playbook), the LLC route works, but I'd skip 58同城 agencies entirely. The two sane paths:

- **DIY** (~$160 first year): file Wyoming Articles of Organization online yourself (30 min), use Northwest Registered Agent ($39/yr) as agent + address, fax Form SS-4 to the IRS for a free EIN (takes ~1–2 weeks for foreign applicants without SSN), then apply to Mercury. Total control, no lock-in, and you understand every moving part — which matters when you're the one liable for the 5472.
- **doola / Firstbase / Stripe Atlas** ($300–500): English-language, standardized, and doola/Firstbase offer the annual 5472 filing as a documented add-on. Stripe Atlas is Delaware C-corp only ($500 + $175/yr franchise tax minimum) — overkill unless you're raising US VC money.

The 58同城 agency's only real advantage is Chinese-language hand-holding. The disadvantage is you're trusting a company with 1,800-CNY-deal economics to remind you about a $25,000 federal penalty every April. For someone who reads IRS instructions as easily as CUDA docs, DIY is the better trade.

One more thing: **don't register until you have a concrete use case** (e.g., Stripe for a specific product about to launch). An idle LLC is pure carrying cost + compliance liability. Given your playbook of validating revenue experiments first, form the entity the week you need to accept a payment, not before — Wyoming turnaround is days, not months.

**References:**

- [Form 5472 for foreign-owned LLCs: 2026 guide — Entity Inc.](https://www.entity.inc/blog/form-5472-foreign-owned-llc/)
- [IRS Instructions for Form 5472](https://www.irs.gov/instructions/i5472)
- [Form 5472 — LLC University walkthrough](https://www.llcuniversity.com/irs/form-5472-foreign-owned-llc/)
- [美国公司注册费用详解 — 知乎](https://zhuanlan.zhihu.com/p/10238483409)
