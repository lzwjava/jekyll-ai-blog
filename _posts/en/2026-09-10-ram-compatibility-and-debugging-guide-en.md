---
audio: false
generated: true
image: false
lang: en
layout: post
title: RAM Compatibility and Debugging Guide
translated: false
type: note
---

Question: **You're using a Galaxy GAMER II DDR4-2666 8GB C19 DIMM with the i5-6500 + MSI B150M PRO.**

Answer: **That RAM should be compatible.** DDR4-2666 is not inherently a problem.

The i5-6500 officially supports **DDR4-2133**, so on a normal B150 setup, your DDR4-2666 stick should simply run at a lower speed (typically **2133 MT/s**) rather than prevent POST.

So if the debug LED keeps cycling:

```text
CPU → DRAM → CPU → DRAM ...
```

I'd test in this order:

```text
1. One GAMER II 8GB stick
2. Try each DIMM slot
3. Clear CMOS
4. Reseat CPU
5. Inspect LGA1151 socket pins
6. Try another known-good DDR4 stick
```

**Don't worry about the C19 rating yet.** That's not likely to be the cause of a complete failure to POST.

If you upload a photo of the **RAM installed + the motherboard Debug LEDs**, I can inspect the physical setup and tell you what I'd check next.