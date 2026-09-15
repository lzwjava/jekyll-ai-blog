---
audio: false
generated: true
image: false
lang: en
layout: post
title: PCIe x16 Slots Explained
translated: false
type: note
---

Question: Does the Gigabyte **GA-AB350-Gaming 3** have two PCIe x16 slots?

Answer: **Yes.** It has:

* **1× PCIe 3.0 x16** — CPU-connected, full x16
* **1× physical PCIe x16 running at x4** — chipset-connected, PCIe 2.0
* **1× physical x16 running at x1**
* **2× PCIe x1**

So if you mean **two full-length x16 slots for GPUs/cards**, yes: **two**. But only the first is actually x16 electrically; the second is **x4**. ([GIGABYTE][1])

One important detail: the second x4 slot shares bandwidth with two x1 slots. If those x1 slots are populated, the x4 slot drops to **x2**. ([GIGABYTE][1])

If you're considering this for **two GPUs / two AI cards**, I can check whether the PCIe lane layout is actually usable for your specific cards.

[1]: https://www.gigabyte.com/us/Motherboard/GA-AB350-Gaming-3-rev-1x/sp?utm_source=chatgpt.com "GA-AB350-Gaming 3 (Rev. 1.x) Motherboard Specifications - GIGABYTE U.S.A."
