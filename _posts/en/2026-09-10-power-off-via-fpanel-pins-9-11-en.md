---
audio: false
generated: true
image: false
lang: en
layout: post
title: Power Off via F_PANEL Pins 9-11
translated: false
type: note
---

Question: How do you power off the L-IG41M3 from the F_PANEL header?

Answer: **You normally use the same two pins: 9 and 11.**

* **Power on:** briefly short **pin 9 ↔ pin 11** (~0.5 sec).
* **Normal power off:** briefly short **pin 9 ↔ pin 11** again (~0.5 sec). The motherboard/OS interprets it as pressing the power button.
* **Forced power off:** hold **pin 9 ↔ pin 11** continuously for about **4 seconds**. This is equivalent to holding the case power button.

```text
F_PANEL

Pin 9  ───┐
          │ ← screwdriver / switch
Pin 11 ───┘

short briefly → ON / request shutdown
hold ~4 sec   → forced OFF
```

**Don't short other pins to power it off.** The `PS` + `GND` pair is the one intended for this.

If you upload a photo of the header, I can identify **pin 9 and 11 on your physical board** by orientation.
