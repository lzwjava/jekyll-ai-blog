---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M DDR4 Variant Required
translated: false
type: note
---

Question: Can an MSI B760M motherboard use DDR4 memory?

Answer: **Only if it is the DDR4 variant.** B760M is the chipset/platform name; MSI makes both DDR4 and DDR5 boards.

For example:

* **MSI PRO B760M-E DDR4** → ✅ DDR4
* **MSI PRO B760M-E D5** → ❌ DDR4, **DDR5 only**
* **MSI MAG B760M MORTAR WIFI DDR4** → ✅ DDR4
* **MSI MAG B760M MORTAR WIFI** (DDR5 version) → ❌ DDR4

DDR4 and DDR5 **cannot be physically interchanged**: the notch is in a different position, and the electrical signaling/PMIC architecture differs.

So for the **MSI PRO B760M-E D5 you were looking at for 120 CNY**, your Samsung **8 GB PC3L DDR4** sticks will **not** work. You need DDR5 DIMMs.

If you send me a photo of the exact motherboard, I can identify the RAM type from the board markings.
