---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hong Kong Company Pros and Cons
translated: false
type: note
---

**Question:** What are the pros and cons of registering a Hong Kong company for a one-person business, specifically for my situation (mainland China resident, bank contractor in Guangzhou, building startup optionality)?

**Answer:**

Short version: an HK Ltd is the standard vehicle for a mainland-based indie dev/AI engineer who wants to bill overseas customers, receive USD (Stripe, App Store, API resale, SaaS), and keep a clean legal wrapper. But it's not free money — the ongoing compliance cost (~HK$10–20K/year) only makes sense once you have real revenue, and your PRC tax residency doesn't disappear just because the entity is in HK.

## The numbers first (2026)

Government fees alone are HK$3,895 for electronic filing (HK$1,545 Companies Registry + HK$2,350 Business Registration Certificate from 1 April 2026), and a standard year-one setup with a TCSP provider including company secretary and registered office typically runs HK$8,000–12,000. Annual recurring costs include the annual return (HK$105), audit fees of HK$8,000–15,000, tax preparation, and company secretary fees.

Tax: 8.25% on the first HK$2M of assessable profits, 16.5% above that; no capital gains tax, no dividend withholding tax, no GST/VAT.

## Pros — for you specifically

1. **Global payment rails.** Stripe, Paddle, App Store/Play Store payouts, OpenRouter-style API billing — all trivially available to an HK Ltd, painful or impossible for a mainland individual. This is the #1 practical reason indie hackers in Shenzhen/Guangzhou incorporate in HK. If your revenue experiments (playbook item #5) target overseas users, this is nearly mandatory.

2. **Low, simple tax.** 8.25% up to HK$2M profit beats mainland corporate structures for small profits. A private limited company gives limited liability, 8.25% on the first HK$2M, no capital gains or dividend tax. Compare: as a mainland individual, foreign service income gets messy fast.

3. **Territorial system + offshore claim (with caveats).** Hong Kong taxes only profits arising in or derived from Hong Kong; if decision-making and contract execution happen entirely outside HK, profits may qualify for exemption — potentially 0%. But this is a formal claim to the IRD, not automatic, and it triggers audits/scrutiny. For a Guangzhou-based solo founder, an offshore claim is technically arguable but adds accounting cost; many just pay the 8.25%.

4. **100% remote, 100% foreign-owned, one person.** Minimum one director (any nationality), minimum one shareholder (can be the same person). You can be the sole director + sole shareholder. No local director needed. Incorporation is fast — often 1–2 days electronically.

5. **Credibility + separation from your bank job.** Contracts signed by "XX Limited (HK)" rather than you personally. Limited liability protects your family assets — relevant given the mortgage. Also a cleaner story when you eventually go full-time: the entity, bank account, and revenue history already exist.

6. **No forex controls.** No foreign exchange controls — capital and profits move freely across borders. USD in, USD out, convert to HKD/RMB when you choose. Contrast with mainland's US$50K/year individual FX quota friction.

## Cons — for you specifically

1. **Fixed annual burn before revenue.** Company secretary (mandatory, must be an HK resident or HK-registered TCSP, and if you're the only director you cannot be the secretary yourself) + registered office + **mandatory annual audit** (yes, even with near-zero revenue) + BRC renewal. Realistically ~HK$12–20K/year (~11–18K CNY). If your side project earns 1K CNY/month, the entity eats the profit. Rule of thumb: incorporate when you have (or are about to have) ≥50K CNY/year in revenue that *needs* the HK structure.

2. **Banking is the real bottleneck.** Traditional banks (HSBC/Standard Chartered) take 4–8 weeks and it's the hardest part; neobanks like Airwallex or Statrys can be ~48 hours. Banks want evidence of real business activity — contracts, invoices, receipts — not just incorporation documents, plus in-person meetings. A mainland resident with no HK footprint and "AI tools, pre-revenue" is exactly the profile banks are wary of. Practical path: Airwallex/Statrys/Wise first, traditional bank later once you have transaction history.

3. **You remain a PRC tax resident.** This is the one people ignore. Living in Guangzhou, China taxes your worldwide income. Salary you pay yourself or dividends you take from the HK company are, on paper, PRC-taxable personal income, and HK-mainland CRS information exchange exists. Many small operators fly under the radar; that's a risk posture, not a legal position. Also, if you actually manage the company entirely from Guangzhou, the PRC could in theory treat it as mainland tax-resident (effective-management rule) — rarely enforced at solo scale, but it's the mirror image of HK's offshore-claim logic. Worth one paid consult with a cross-border accountant before you route real money.

4. **Public disclosure.** Directors and significant controllers are on record; you must maintain a Significant Controllers Register and appoint a designated representative. If "build quietly" (playbook item #4) matters, note your name is searchable in the Companies Registry — potentially visible to your bank employer's compliance team. Check your contractor agreement for outside-business-interest clauses **before** incorporating. This is probably your biggest non-obvious risk given the global-bank context.

5. **Substance scrutiny is increasing.** The IRD has tightened offshore exemption claims under the FSIE regime — companies must demonstrate economic substance in Hong Kong, and banks and authorities increasingly scrutinize companies without genuine HK business substance. Shell-with-zero-activity setups are getting harder, not easier.

6. **Doesn't help with mainland-facing business.** If your customers pay in RMB via WeChat/Alipay, an HK entity adds friction (cross-border settlement, no mainland invoicing/fapiao). HK Ltd is for *outbound* revenue. For mainland revenue you'd want a 个体户 or mainland LLC instead — different tool.

## Decision heuristic for your playbook

- **Now (pre-revenue):** don't incorporate. Ship the CLI tools, get GitHub stars, validate. Zero entities needed to earn your first 1K CNY/month via e.g. GitHub Sponsors or a personal Stripe workaround through a marketplace.
- **When a product has paying overseas users** (or you need Stripe/App Store as a business): incorporate HK Ltd via a TCSP bundle (~HK$8–12K year one), open Airwallex same week, pay 8.25% and don't bother with the offshore claim initially.
- **Before routing >~100K CNY/year through it:** one consult on PRC personal tax treatment of your salary/dividends.
- **First:** read your bank contractor agreement's moonlighting/conflict clause. That's the cheapest risk check available and the one most specific to you.

**References:**

- [Sleek — How to Start a Business in Hong Kong (2026)](https://sleek.com/hk/resources/how-to-start-a-business/)
- [Sleek — HK Company Registration Cost 2026](https://sleek.com/hk/resources/company-registration-cost-hong-kong/)
- [Alpadis — Setting Up a Company in Hong Kong 2026](https://www.alpadis.com/insights/how-to-set-up-a-company-in-hong-kong-in-2026-complete-guide-to-incorporation-requirements-taxes-and-offshore-structuring-for-foreigners)
- [Statrys — HK Sole Proprietorship Guide 2026](https://statrys.com/hk/guides/legal-entities/how-to-register-a-sole-proprietorship)
- [Zitadelle — HK Company Formation 2026 / FSIE substance rules](https://www.zitadelleag.com/news/hong-kong-company-formation-holding-setup)
- [GrowAcross — HK Company Formation provider comparison](https://growacross.com/hong-kong/company-formation)

One caveat: I'm not a tax advisor, and the PRC-side treatment (point 3) is the part where a paid hour with a Guangzhou/HK cross-border accountant is genuinely worth it before real money flows.
