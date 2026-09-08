---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M-E DDR5 CPU Compatibility
translated: false
type: note
---

**Question:** What CPUs can be used with the MSI PRO B760M-E DDR5 motherboard?

**Answer:** The **MSI PRO B760M-E (DDR5)** uses **LGA1700** and officially supports Intel **12th, 13th, and 14th Gen Core CPUs**, plus Pentium Gold and Celeron. ([MSI][1])

### CPU compatibility

| Generation            | Examples                                           | Works? |
| --------------------- | -------------------------------------------------- | ------ |
| 12th Gen              | i3-12100, i5-12400, i5-12600K, i7-12700, i9-12900K | ✅      |
| 13th Gen              | i3-13100, i5-13400, i5-13600K, i7-13700, i9-13900K | ✅      |
| 14th Gen              | i3-14100, i5-14400, i5-14600K, i7-14700, i9-14900K | ✅      |
| Pentium Gold          | Various LGA1700 models                             | ✅      |
| Celeron               | Various LGA1700 models                             | ✅      |
| Core Ultra / 15th Gen | LGA1851                                            | ❌      |

The important part is **LGA1700**. It cannot take newer Intel Core Ultra desktop CPUs, which moved to LGA1851.

### But there's an important catch

The **B760M-E is a very entry-level board**. I would **not pair it with an i9-13900K/14900K** despite the socket compatibility. The CPU can technically be supported, but the board's power delivery and cooling are not really what I'd choose for sustained high-power workloads.

For this board, I'd target:

* **i3-12100 / 13100 / 14100** → cheap
* **i5-12400** → ⭐ excellent cheap choice
* **i5-13400 / 14400** → ⭐ good
* **i5-13500** → ⭐ very interesting used-market choice
* **i5-13600K / 14600K** → possible, but you're approaching the point where I'd buy a better motherboard
* **i7/i9** → technically compatible, but not my recommendation for this board

Also, because yours is the **DDR5 version**, it has **2 DDR5 DIMM slots and supports up to 128 GB** according to MSI's current specification. ([MSI][1])

If you're looking at a **cheap second-hand CPU + motherboard combination**, I'd probably hunt for a **used i5-12400/13400/13500** rather than an expensive 14th-gen chip.

[MSI PRO B760M-E official specifications](https://www.msi.com/Motherboard/PRO-B760M-E/Specification?utm_source=chatgpt.com)

If you give me the **CPU you're considering and its price**, I can tell you whether it's a good Xianyu deal for this board.

[1]: https://www.msi.com/Motherboard/PRO-B760M-E/Specification?utm_source=chatgpt.com "PRO B760M-E"
