---
audio: false
generated: true
image: false
lang: en
layout: post
title: Interface Check and Motherboard Price
translated: false
type: note
---

**Question:** What does "checking interfaces one by one" mean (in the context of DIY PC troubleshooting), and is 1299 CNY a fair price for the MSI MAG B760M Mortar WiFi motherboard?

**Answer:**

**"挨个查接口" (checking interfaces one by one)**

This is standard hardware-debugging methodology — binary-search-style fault isolation applied to physical connectors instead of code:

- No display? Check each output port (HDMI/DP) individually, and test with a different cable/monitor per port to isolate whether the fault is GPU, cable, or monitor.
- No boot? Check each power connector (24-pin ATX, 8-pin CPU, PCIe power) one at a time — reseat, verify click-lock, check for bent pins.
- No storage detected? Check each M.2 slot / SATA port individually — some B760 boards share PCIe lanes between M.2 slots and SATA ports, so populating one can disable another (check the motherboard manual's lane-sharing table, this is a common "ghost fault").
- No USB/audio/RGB header working? Check each front-panel header pin-by-pin against the motherboard manual's silkscreen, since a single reversed pin (common with F_PANEL, USB 2.0/3.0 headers) causes silent failure, not a crash.

It's essentially manual differential diagnosis — the same "isolate one variable at a time" principle you already apply to debugging distributed systems, just physical instead of logical. You're right that it's the DIY tradeoff: full customization + skill-building vs. paying ~200 CNY/visit for a technician to do the same 10-minute reseat you can learn once and never pay for again.

**Price check: MSI MAG B760M Mortar WiFi — 1299 CNY**

This checks out. The MAG B760M Mortar WiFi II launched at 1299 yuan, with the non-WiFi variant priced 50 yuan cheaper, and this represented a 150 yuan price cut compared to the previous DDR5 generation's initial launch price. Separately, the DDR4 variant (MAG B760M Mortar WiFi DDR4) carries a reference price of 1299 yuan as well.

So 1299 CNY is accurate as a launch/reference price for either the WiFi II (DDR5) or the DDR4 variant — just confirm which SKU you're actually buying, since MSI has several near-identical "Mortar WiFi" naming variants (DDR4 vs DDR5, original vs "II" vs "MAX") at similar price points but different memory support and M.2 slot counts. For an AI/GPU workstation build, DDR5 + PCIe 5.0 (the WiFi II) is the better long-term pick if you ever want to drop in a discrete GPU or NVMe for local model work.

**References:**

- [微星MAG B760M 迫击炮 WIFI II主板评测 - 腾讯新闻](https://news.qq.com/rain/a/20231017A09OAM00)
- [微星MAG B760M MORTAR WIFI DDR4报价 - 天极产品库](https://product.yesky.com/product/1156/1156046/)
