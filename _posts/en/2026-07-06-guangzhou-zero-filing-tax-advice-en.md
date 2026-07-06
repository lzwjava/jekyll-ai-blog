---
audio: false
generated: true
image: false
lang: en
layout: post
title: Guangzhou Zero Filing Tax Advice
translated: false
type: note
---

**Question:** Does this advice — separate bookkeeping, ~1,000 CNY/year agency fee is cheap if there's real invoicing, but pure zero-filing (零申报) can be DIY'd or even scripted if the company only exists for mini-program verification / ICP filing — apply to a Guangzhou-registered company?

**Answer:**

Yes, it applies. All of this is national policy, not city-specific — a Guangzhou company just files through the **Guangdong Provincial Electronic Tax Bureau (广东省电子税务局)**. The advice is basically correct, with a few details worth knowing:

**What a zero-revenue small-scale taxpayer (小规模纳税人) actually files:**

1. **VAT + surcharges** — quarterly (Jan/Apr/Jul/Oct, by the 15th). For 2026-01-01 to 2027-12-31, the threshold is 100K CNY/month or 300K CNY/quarter — below that, VAT-exempt, and at zero revenue it's a two-minute confirmation-style declaration.
2. **Corporate income tax (企业所得税)** — quarterly prepayment + annual settlement (汇算清缴) by May 31. Zero profit → zero filing.
3. **Individual income tax withholding (个税代扣)** — monthly via 自然人电子税务局, even if you pay no salary (declare 0 employees or 0 wages).
4. **Annual report (工商年报)** — once a year by June 30 on 国家企业信用信息公示系统. Miss it and you land on the 经营异常名录, which breaks things like WeChat mini-program verification — exactly what you registered the company for.

**On the 1,000 CNY figure:** yes, that's cheap for full agency bookkeeping (代理记账) in Guangzhou if you have real invoices — typical market rate is 1,200–3,000/year for small-scale taxpayers. If it's pure zero-filing, agencies charge for something you can do yourself in ~20 minutes per quarter.

**On scripting it:** technically feasible but with one hard wall — the Guangdong e-tax bureau requires real-name login with periodic face verification (via 粤税通/个人所得税 app scan). So a fully headless cron job is out. The realistic version is Playwright automation that holds a logged-in session: you do the face scan once, the script fills and submits the 增值税及附加税费申报表 (all zeros / 未达起征点), CIT prepayment, and the zero IIT declaration. Since it's only 4× VAT + 4× CIT + 12× IIT filings a year and the portal now offers 确认式申报 (pre-filled, one-click confirm), honestly the manual path may cost less time than maintaining the script against portal UI changes. A calendar reminder + 20-minute quarterly ritual is the pragmatic answer.

**Two caveats:**

- Long-term continuous zero-filing (roughly 6+ months) while the company shows activity signals (invoices received, bank account flows, social insurance registrations) can flag you for tax bureau review under Golden Tax IV. A genuinely dormant shell used only for 备案/小程序认证 is normally fine.
- If you ever start invoicing, switch to real bookkeeping immediately — receiving payments through personal accounts without invoicing/declaring is a current audit focus.

One disclaimer: I'm not a tax advisor, and enforcement details vary — for anything beyond zero-filing, a quick consult with a local 代账 firm is worth it.

**References:**

- [国家税务总局公告2026年第10号 — VAT threshold 2026–2027](https://fgk.chinatax.gov.cn/zcfgk/c102416/c5247434/content.html)
- [PwC — VAT Law supporting circulars interpretation (Feb 2026)](https://www.pwccn.com/zh/china-tax-news/2026q1/chinatax-news-feb2026-2.pdf)
- [KPMG — VAT Law transition analysis](https://kpmg.com/cn/zh/insights/2026/02/china-tax-alert-03.html)
