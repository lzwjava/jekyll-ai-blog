---
audio: false
generated: true
image: false
lang: en
layout: post
title: MemTest86+ No Errors Yet
translated: false
type: note
---

Question: What can I tell from this photo?

Answer: This is **MemTest86+ v8.00** running on a system with:

* **CPU:** Intel Xeon E31260L @ 2.40 GHz — 4 cores / 8 threads
* **RAM:** 7.88 GiB total

  * Slot 0: Kingston 4 GB DDR3-1333
  * Slot 2: Kingston 4 GB DDR3-1333
* **Current RAM speed:** 665 MHz × DDR ≈ **1330 MT/s**
* **Timings:** CL 9-9-9-24
* **CPU temperature:** ~55–56 °C
* **Test:** Moving inversions, 64-bit pattern
* **Progress:** ~80% through the current test
* **Errors:** **0**

So, **at the moment shown, the memory test has found no errors**. However, it isn't finished yet (`Status: Testing`), so 0 errors at this point does **not** yet prove the RAM is completely stable. For a serious stability check, let MemTest86+ complete multiple passes; ideally, several full passes with **0 errors**.
