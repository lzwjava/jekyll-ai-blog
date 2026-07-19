---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Goofish: China's eBay for Hardware"
translated: false
type: note
---

Question: What's [https://www.goofish.com/?locale=en](https://www.goofish.com/?locale=en) ?

Answer:

[Goofish (Xianyu)](https://www.goofish.com/?locale=en&utm_source=chatgpt.com) is the international web domain of **Xianyu (闲鱼 / Idle Fish)**, Alibaba's second-hand marketplace. It is basically the Chinese equivalent of **eBay + Facebook Marketplace**, but deeply integrated into Alibaba's ecosystem. ([Wikidata][1])

It is especially famous in China for:

* **Used electronics**

  * GPUs: RTX 3090, RTX 4090, A6000, Tesla cards
  * CPUs, servers, MacBooks
  * phones, cameras
* **Computer hardware**

  * mining GPUs
  * workstation parts
  * engineering samples
  * retired enterprise hardware
* **Collectibles**
* **Second-hand goods**
* **Factory surplus / clearance items** ([Savvyoo][2])

For your AI hardware hunting, this is exactly the place where many Chinese users buy/sell:

```
RTX 3090 24GB
A6000 48GB
Tesla P100
Tesla V100
MI50
MI100
EPYC servers
DDR4 ECC RAM
NVMe SSD
```

The reason prices can be much lower than JD/Tmall is that many sellers are:

* individuals selling old equipment
* small GPU miners liquidating cards
* IT shops selling used enterprise hardware
* companies clearing inventory

Example:

```
JD:
RTX 3090 new/official channel: very expensive or unavailable

Goofish:
RTX 3090 used:
¥4000-8000 CNY depending on condition
```

(Prices fluctuate heavily.)

The business model:

```
Buyer
  |
  |  Alipay escrow
  |
Xianyu platform
  |
  |
Seller
```

Money is held by Alibaba's payment system until the transaction completes. ([Alibaba Group][3])

However, unlike JD/Tmall:

|               | Goofish            | JD        |
| ------------- | ------------------ | --------- |
| Seller        | Mostly individuals | Retailers |
| Price         | Lower              | Higher    |
| Warranty      | Often none         | Better    |
| Risk          | Higher             | Lower     |
| Negotiation   | Common             | Rare      |
| Rare hardware | Excellent          | Poor      |

For GPU purchases, common checks:

```bash
# before buying RTX 3090
1. Ask for GPU-Z screenshot
2. Ask for FurMark / 3DMark test
3. Check memory errors
4. Check mining history
5. Test temperature
6. Prefer local pickup
```

Since you are already looking at Chinese second-hand GPU markets, Goofish is basically the main battlefield. It is where many Chinese AI enthusiasts find cheap VRAM. ([Trip.com][4])

The English UI exists, but most listings and seller communication are still Chinese-focused. International buyers often need Chinese language ability, a China address, or a forwarding/buying service. ([Savvyoo][2])

References:

* [Alibaba Xianyu overview](https://www.alibabagroup.com/en-US/about-alibaba-businesses-1747081802473799680?utm_source=chatgpt.com)
* [Xianyu (Wikidata)](https://www.wikidata.org/wiki/Q32187808?utm_source=chatgpt.com)

[1]: https://www.wikidata.org/wiki/Q32187808?utm_source=chatgpt.com "Xianyu - Wikidata"
[2]: https://savvyoo.com/sites-apps/xianyu/?utm_source=chatgpt.com "Xianyu (Idle Fish) Guide: Second-Hand Shopping, Agents & Safety – Savvyoo"
[3]: https://www.alibabagroup.com/en-US/about-alibaba-businesses-1747081802473799680?utm_source=chatgpt.com "XIANYU-Alibaba Group"
[4]: https://www.trip.com/guide/info/xianyu.html?utm_source=chatgpt.com "Xianyu Guide for Foreigners: How to Buy/Sell in English | Trip.com"
