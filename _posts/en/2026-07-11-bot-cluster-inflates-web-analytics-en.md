---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bot Cluster Inflates Web Analytics
translated: false
type: note
---

**Question:** Here's my actual Cloudflare Web Analytics dashboard (Core Web Vitals, page views by country/referrer/browser/OS/device) showing 61.37k total page views for the same 30-day window where GoatCounter shows ~3.8k–4k. What's really going on?

**Answer:**

This changes my earlier diagnosis, and I should say so directly: the presence of Core Web Vitals (LCP/INP/CLS) confirms this **is** the JS-beacon Web Analytics product, not the raw server-side edge-log product I flagged last time. So "wrong Cloudflare panel" isn't the explanation here — this beacon really is firing 61k times. The explanation is more specific and more interesting: **you have a JS-executing bot cluster concentrated almost entirely in one geography/OS/browser/device combo.**

## Overlay the majorities — they're the same traffic

Look at how these percentages stack on top of each other instead of reading them as five independent facts:

| Dimension | Dominant bucket | Share of 60.95k |
|---|---|---|
| Country | Singapore | 46.28k → **76%** |
| OS | Windows | 48.48k → **79.5%** |
| Browser | Chrome | 48.89k → **80.2%** |
| Device | Desktop | 54.24k → **89%** |
| Referrer | None (direct) | 54.87k → **90%** |

A personal Guangzhou-based engineer's blog does not organically get 76% of its readership from Singapore. Singapore is one of the densest **datacenter/cloud regions in Asia** (AWS ap-southeast-1, GCP asia-southeast1, Alibaba Cloud, Tencent Cloud, DigitalOcean SGP1, plus it's a common VPN/residential-proxy exit node). Combine that with "Windows + Chrome + Desktop + no referrer" — that's the single most common signature produced by **headless Chrome automation** (Playwright/Puppeteer default launch args spoof a plain Windows Chrome desktop UA unless explicitly randomized) running at scale from cloud VMs.

Critically: this is a bot that **executes JavaScript** — that's why it fires the Cloudflare beacon and even reports real Core Web Vitals (LCP/INP/CLS numbers), which a simple `curl`/`requests`-based scraper never could. This is exactly the category Cloudflare's own bot docs call out: When enabled, Bot Fight Mode identifies traffic matching patterns of known bots and issues computationally expensive challenges — and separately, the option to enable JavaScript Detections to identify headless browsers and other actors on the Internet exists specifically because JS-executing headless browsers are a distinct, harder-to-catch category from classic non-JS scrapers.

## Two more supporting anomalies

- **`/error-en` got 1,040 hits** — real humans don't hit your error page 1,040 times. That's consistent with an automated crawler probing many URL guesses/hallucinated paths and repeatedly landing on your 404/error route.
- **The genuinely human-looking signal is small and separate**: `weixin110.qq.com` (600), `yandex.ru`+`yandex.com` (470) — together ~1,070, under 2% of the total. That's the same organic WeChat-share / Yandex-search pattern I flagged from your GoatCounter data, just scaled proportionally. It's buried under the automated layer, not contradicted by it.

## Back-solving the real number

Strip the ~55k Singapore/Windows/Chrome/Desktop/direct cluster from 61k, and you're left with roughly **5-6k** — which lines up closely with GoatCounter's ~3.8-4k (the residual gap being GoatCounter's own blind spots I mentioned before: adblock-list filtering of its script domain, or a slightly stricter bot UA filter). **GoatCounter's number was the trustworthy one the whole time.** The 60k was never your real readership.

## Fix it, don't just measure around it

1. **Turn on Bot Fight Mode** (free plan, Security > Settings > filter "Bot traffic") — Bot Fight Mode is included with Free plans and forces JavaScript Detections on automatically for headless-browser identification, which is exactly the traffic type inflating your numbers.
2. **Check Security > Analytics > Bot Analysis** (if visible on your plan) before/after enabling it — Cloudflare assigns a bot score to every incoming request, grouped into Automated, Likely automated, and Likely human buckets, and you can filter by country, browser, and OS to confirm the Singapore/Windows/Chrome cluster scores as automated.
3. Give it a few days, then re-check the country/OS breakdown in Web Analytics — if this diagnosis is right, Singapore's share should collapse toward something proportionate to your real Asia readership (Hong Kong, China, Japan are already showing plausible, much smaller numbers).
4. For your brand-metrics purposes (AI · Live), **use GoatCounter as ground truth going forward**, not raw Cloudflare Web Analytics totals — it's a JS beacon too, but apparently isn't a specific target of whatever traffic-generation network is hitting the ubiquitous Cloudflare auto-injected beacon at scale across many Cloudflare-fronted sites.

**References:**

- [Get started with Bot Fight Mode · Cloudflare bot solutions docs](https://developers.cloudflare.com/bots/get-started/bot-fight-mode/)
- [Stop malicious bots while allowing legitimate traffic · Cloudflare use cases](https://developers.cloudflare.com/use-cases/solutions/stop-malicious-bots/)
- [How to protect your site from unwanted bot traffic with Cloudflare — Kinsta](https://kinsta.com/blog/block-bots-wordpress-cloudflare/)
