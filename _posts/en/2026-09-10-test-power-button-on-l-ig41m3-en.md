---
audio: false
generated: true
image: false
lang: en
layout: post
title: Test Power Button on L-IG41M3
translated: false
type: note
---

Question: You short **pin 9 ↔ pin 11** on your L-IG41M3, but the machine does not power off. Is the motherboard faulty?

Answer: **Not necessarily—but if it powers on normally and the same short reliably starts it, then the F_PANEL input is probably working.** The important distinction is between **a normal shutdown** and **a forced power-off**.

The L-IG41M3 schematic confirms:

```text
pin 9  = PS / PWRBTN
pin 11 = GND
```

and the power-button signal goes into the motherboard's `PWRBTN_L` logic. ([ManualMachine][1])

### Test it this way

If you're currently in Windows/Linux:

```text
short pin 9 ↔ pin 11
       ↓
OS receives power-button event
       ↓
OS decides what "power button" means
```

It **may not immediately cut power**. The OS can be configured to ignore the button, sleep, or perform a normal shutdown.

Instead, test the hardware's forced-off behavior:

```text
Power ON
   ↓
short 9 ↔ 11
   ↓
keep shorting for ~4–5 seconds
   ↓
fans should stop
```

There is actually a repair report specifically for the **L-IG41M3** describing the exact symptom:

> power-on works, but after shutdown the fan keeps running and a 4-second short cannot turn it off.

The repair traced the shutdown sequence through `SLP3_L` → `IT8755E` → `ATX_PSON_L`; ultimately a USB power-controller fault was holding the shutdown signal in the wrong state. ([China2Japan][2])

So if **4–5 seconds of 9↔11 does absolutely nothing**, that becomes interesting from a motherboard-repair perspective.

### First, isolate the possibilities

Run this simple experiment:

```text
1. Boot the board.
2. Short 9 ↔ 11 briefly.
   → Does Windows/Linux react?

3. Then short 9 ↔ 11 continuously for 5–10 sec.
   → Do the fans/power actually stop?
```

Interpretation:

| Result                                     | Likely situation                                  |
| ------------------------------------------ | ------------------------------------------------- |
| Brief press shuts OS down                  | F_PANEL + PWRBTN logic good                       |
| Brief press does nothing, long press works | OS/button behavior/configuration                  |
| Brief press works, long press does nothing | **Possible motherboard power-sequencing problem** |
| Even starting with 9↔11 is unreliable      | Investigate F_PANEL / PWRBTN input                |

**One more important point:** don't keep the pins shorted for long periods repeatedly. The normal test is a brief contact; the ~4-second test is only to reproduce the motherboard's emergency power-button behavior.

If you can upload a photo of your **actual L-IG41M3 F_PANEL area while the board is powered on**, I can check the physical orientation and make sure you're actually shorting **9 and 11**, rather than relying on the pin numbering.

References:

* [ECS L-IG41M3 Rev. 1.1 schematic](https://manualmachine.com/ecs/lig41m3/24375062-schematics--rev-1/?utm_source=chatgpt.com)
* [L-IG41M3 repair case: cannot power off after shutdown](https://www.china2japan.com/bbs_forum/weixiujingyan/2021/0828/1178171.html?utm_source=chatgpt.com)

[1]: https://manualmachine.com/ecs/lig41m3/24375062-schematics--rev-1/?utm_source=chatgpt.com "ECS L-IG41M3 Schematics REV 1.1 - ManualMachine.com"
[2]: https://www.china2japan.com/bbs_forum/weixiujingyan/2021/0828/1178171.html?utm_source=chatgpt.com "日本维修经验酷派_ 按时序修好联想L-IG41M3谁有影驰660黑将的BIOS 麻烦"
