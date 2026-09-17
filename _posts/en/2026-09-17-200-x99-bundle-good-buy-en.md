---
audio: false
generated: true
image: false
lang: en
layout: post
title: "¥200 X99 Bundle: Good Buy?"
translated: false
type: note
---

Question: Is the ¥200 used Huananzhi X99-AD4 + Xeon E5-2680 v4 board/CPU bundle a good buy?

Answer: **Yes — at ¥200, I’d consider it a good deal, assuming you can verify it boots and the board is healthy.** The price is low enough that the main risk is the used motherboard, not the CPU.

The important specs:

* **E5-2680 v4:** 14 cores / 28 threads, 2.4 GHz base, up to 3.3 GHz turbo, 35 MB cache, 120 W TDP. ([Intel][1])
* **X99-AD4:** LGA2011-3, 4× DDR4 DIMMs, quad-channel memory, up to 128 GB; it has PCIe 3.0 x16 slots and M.2 support. ([Scribd][2])
* The listing's **¥230 board+CPU price** makes the seller's ¥200 offer particularly attractive if genuine.
* There are recent used listings for the same CPU + AD4 combination, but those are sold with testing/warranty, so don't directly compare their asking prices to this **"no returns"** unit. ([Ruten][3])

### The catch

The seller says:

> no I/O shield, used condition, no returns, pickup recommended.

That **"no returns" matters more than the missing shield**.

At ¥200, I would **not buy it blind and have it shipped**. If you're in Guangzhou and can pick it up, this becomes much more attractive because you can test it before handing over money.

I'd test:

```text
1. CPU-Z → CPU recognized as E5-2680 v4 / 14C28T
2. BIOS → CPU + all 4 DIMM slots recognized
3. MemTest86 / memory test → ideally quick pass
4. Linux:
   lscpu
   free -h
   lspci
5. Stress CPU for 5–10 min
6. Check all PCIe slots
7. Check M.2/SATA
8. Check USB + Ethernet
9. Reboot 2–3 times
```

**Especially test the RAM slots.** Cheap X99 boards can be much more annoying when a DIMM channel/slot becomes flaky than when the Xeon itself is bad.

### What is ¥200 actually buying you?

Think of it as:

```text
E5-2680 v4        ~cheap commodity Xeon
X99-AD4            ~the valuable part
6-pipe cooler      free
----------------------------
Total               ¥200
```

The **14C/28T CPU is still useful for CPU-parallel workloads**, especially compilation, VM workloads, batch processing, rendering, and lots of lightweight processes. But don't expect modern single-thread performance: 2.4 GHz base / 3.3 GHz turbo is very old-school Xeon territory. ([Intel][1])

For an **AI workstation**, I'd treat the CPU as a platform for the GPU rather than the compute engine. A modern GPU will massively outperform this CPU for actual model inference/training.

### My price threshold

For a tested local pickup unit:

```text
¥150       steal
¥200       good buy
¥230       still reasonable
¥250–300   only if very clean / tested / accessories
>¥300      I'd start looking at newer platforms
```

So **¥200 + local pickup + test before payment = I'd take it**.

One thing I'd clarify with the seller before going: **does ¥200 include the E5-2680 v4 + X99-AD4 + the six-heatpipe cooler, or is ¥200 just the board+CPU and the cooler is only included at ¥230?** The listing text is slightly ambiguous.

If you want, I can also compare this ¥200 X99 setup against **used AM4 / Xeon W / newer Intel platforms around ¥300–500** and calculate the CPU/RAM/GPU expansion value.

[1]: https://www.intel.com/content/www/us/en/ark/products/series/91287/intel-xeon-processor-e5-v4-family.html?utm_source=chatgpt.com "Intel® Xeon® Processor E5 v4 Family"
[2]: https://www.scribd.com/document/744700977/HUANANZHI-X99-AD4-User-Manual?utm_source=chatgpt.com "HUANANZHI X99-AD4 User Manual | PDF"
[3]: https://www.ruten.com.tw/item/22518360627327/?utm_source=chatgpt.com "E5-2680 V4 ( 14C28T) CPU+華南金牌 X99-AD4 主機板/ DDR4/M.2/外觀品項新 | 露天市集 | 全台最大的網路購物市集"
