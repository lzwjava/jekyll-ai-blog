---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX PRO 6000 Price Surge
translated: false
type: note
---

Question: Did the "RTX A6000 Pro" (i.e., RTX PRO 6000 Blackwell — there's no card actually named "A6000 Pro") jump from ~50K CNY to ~100K CNY over the past few months?

Answer: Roughly yes, confirmed by multiple sources. Two clarifications first:

**Naming**: The old RTX A6000 (Ampere, 2020, 48GB GDDR6) hasn't moved much in price. What's actually spiking is the **RTX PRO 6000 Blackwell** (96GB GDDR7, launched March 2025) — people colloquially call it "6000 Pro" in China, which likely got garbled to "A6000 Pro." Just confirm which card you're tracking before quoting numbers to a client.

**Price trajectory (RTX PRO 6000 Blackwell, official US marketplace)**:

| Date | USD | CNY (approx, official exchange) |
| --- | --- | --- |
| Mar 2025 (launch) | $8,000–8,565 | ~54,500 |
| May 2026 | $8,900–11,500 (retail spikes) | ~60,600–78,300 |
| Jun 13, 2026 | $13,250 (official Nvidia marketplace) | ~89,789 |

So: **~55-65% increase in ~15 months**, from ~54.5K CNY to ~90K CNY at official/street pricing.Nvidia has raised the official marketplace price of its RTX Pro 6000 Blackwell workstation GPU to $13,250, roughly 55% above its March 2025 launch MSRP.

The gap to your "100K CNY" figure closes when you account for **mainland China landed cost**. Because these cards face export-control friction, most units reach China via Singapore/Malaysia/HK triangulation with added tariffs, VAT (13%), and middleman markup. One breakdown estimated landed cost at ~75,000 CNY even when the US launch price was still ~$8,500 — before the June 2026 hike to $13,250. Scale that same markup chain to the current $13,250 official price and you land close to or above 100K CNY for actual delivered units in China, especially Server Edition variants (one Newegg listing at $14,999 ≈ 102,000 CNY).

Root cause per all sources: **GDDR7 memory shortage**, not manufacturing cost — only a small fraction of the increase reflects higher manufacturing costs; the rest is supply-and-demand pressure in the GDDR7 memory market.

If you're specing this for your GPU cluster budget, worth checking current grey-market quotes (Taobao/eBay Shenzhen sellers) directly rather than official MSRP, since that's where your real procurement number will land — the eBay Shenzhen listing I found was already at ~$10,300–10,345 (~88-89K CNY) before shipping/tariff pass-through.

References:

- [Nvidia Raises RTX Pro 6000 Blackwell MSRP to $13,250 - MLQ News](https://mlq.ai/news/nvidia-raises-rtx-pro-6000-blackwell-msrp-to-13250-a-55-hike-in-one-year/)
- [Tom's Hardware — 55% increase over MSRP](https://www.tomshardware.com/pc-components/gpus/nvidia-raises-rtx-pro-6000-blackwell-gpu-pricing-to-usd13-250-55-percent-increase-over-msrp-in-a-years-time)
- [RTX Pro 6000 Blackwell 大陆到手价 - 知乎](https://zhuanlan.zhihu.com/p/1916163513161868969)
- [AI巨量需求抽干库存 - 新浪科技 (May 2026)](https://finance.sina.cn/stock/jdts/2026-05-18/detail-inhyhpyq4093606.d.html)
