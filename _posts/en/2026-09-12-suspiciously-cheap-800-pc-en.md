---
audio: false
generated: true
image: false
lang: en
layout: post
title: Suspiciously Cheap ¥800 PC
translated: false
type: note
---

Question: **Is ¥800 for this whole PC unusually cheap?**

Answer: **Yes — if the listing is genuine and the specs are exactly as stated, ¥800 is absurdly cheap.** I would assume there's a catch until you test it.

The listed machine:

* RTX 4060 Ti
* i5-14600KF
* B760
* 32 GB RAM
* 1 TB SSD + 3 TB HDD
* presumably complete desktop

For perspective, recent Chinese used-market references put the **14600KF alone around ¥1,300+** in recovery value, while a recent used-market listing reference puts an RTX 4060 Ti around ¥3,600–4,900 equivalent depending on market/source. ([什么值得买][1]) A June 2026 Shenzhen recycler's reference had a **B760 + 32 GB + 1 TB + RTX 4060 Ti** machine at ¥4,500, albeit with a 12600KF rather than 14600KF. ([Sohu][2])

So I'd roughly think:

| Component       | Conservative used value |
| --------------- | ----------------------: |
| 14600KF         |            ¥1,000–1,300 |
| 4060 Ti 8GB     |           ¥1,500–2,000+ |
| B760            |                ¥300–500 |
| 32GB            |                   ¥300+ |
| 1TB SSD         |                ¥300-ish |
| 3TB HDD         |                ¥100–200 |
| PSU/case/cooler |                ¥200–400 |
| **Total**       |       **~¥3,700–5,000** |

**¥800 is not "cheap." It's suspiciously cheap.**

The seller's wording **「自己用，不是贩子，出价来」** is basically "personal use, not a reseller, make an offer." That itself isn't suspicious, but at ¥800 I'd check for:

1. **GPU actually being 4060 Ti** — run GPU-Z.
2. **CPU actually being 14600KF** — CPU-Z.
3. **No dead GPU / artifacting** — 10–20 min GPU stress test.
4. **SSD/HDD SMART health** — CrystalDiskInfo.
5. **CPU stability** — Cinebench/OCCT.
6. **BIOS detects everything.**
7. **PSU brand/model** — this is a big one.
8. **Why it's ¥800.** Ask directly: *“为什么这么便宜？有没有故障/暗病？”*
9. Ideally **local pickup + test before payment**.

One more thing: **14600KF has no iGPU**, so if the 4060 Ti is dead, you won't get a display from the motherboard.

If it's a complete working machine and you can physically test it, **I'd seriously consider buying it at ¥800**. Even if something is wrong, the component value can make the downside relatively small.

**At ¥800, the question isn't "is it a good deal?" — it's "what's broken?"**

[1]: https://post.smzdm.com/talk/p/anvq35d0/?utm_source=chatgpt.com "英特尔全代CPU回收行情一览！二手出手对照不被压价_什么值得买"
[2]: https://www.sohu.com/a/1036062896_122895879?utm_source=chatgpt.com "2026.6深圳二手台式DIY电脑回收价格表 报价公开给您参考_金士顿_Inteli_Corei"
