---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lenovo L-IG41M3 Power Button Wiring
translated: false
type: note
---

Question: **Which pins on the Lenovo L-IG41M3 11-pin front-panel connector should I connect to the case power/on button and the small front-panel circuit board?**

Answer: I found the **L-IG41M3 V1.1 schematic**. The board is an ECS design used by Lenovo, and the schematic explicitly identifies the front-panel power-switch signal as **`PANSWH_L`**. ([Scribd][1])

However, I **would not blindly short two pins on your 11-pin connector yet**. Lenovo customized the front-panel connector, and the exact physical pin numbering/orientation matters.

The useful signal names are:

```text
PANSWH_L   = power switch
SYS_RESET_L = reset switch
FP_LED0    = HDD/activity LED
FP_LED1    = power/status LED
GND        = ground
```

The schematic shows `PANSWH_L` going into the Super I/O and being used as the power-button input. ([Scribd][2])

### For your actual board

If you send me **one clear photo of the L-IG41M3 motherboard showing the 11-pin connector**, especially with:

* the connector itself
* any text printed beside it
* the pin-1 marking / missing-key position
* the small Lenovo front-panel PCB and its 11-pin cable

I can map it like:

```text
11-pin connector

┌─────────────────────┐
│ 1  2  3  4  5  6   │
│ 7  8  9 10 11       │
└─────────────────────┘

        ↓

POWER SW → pin X + pin Y
RESET    → pin X + pin Y
PLED     → pin X + pin Y
HDD LED  → pin X + pin Y
GND      → ...
```

**Don't connect the 11-pin front-panel board by trial and error**, because unlike a standard ATX `F_PANEL`, this Lenovo connector is OEM-specific. The L-IG41M3 schematic itself notes that the front-panel connector definition was modified for Lenovo. ([Scribd][2])

References:

* [L-IG41M3 schematic / manual source](https://manualmachine.com/ecs/lig41m3/24375062-schematics--rev-1/?utm_source=chatgpt.com)
* [L-IG41M3 technical discussion](https://vinafix.com/threads/l-ig41m3.19344/?utm_source=chatgpt.com)

[1]: https://www.scribd.com/document/522563336/ECS-ig41m3-g41t-lm3v1-1?utm_source=chatgpt.com "L-IG41M3 V1.1 Motherboard Overview | PDF | Manufactured Goods | Computer Architecture"
[2]: https://www.scribd.com/document/984973046/Z490H6-LA-V1-1?utm_source=chatgpt.com "Z490H6-LA Block Diagram Guide | PDF | Computer Networking | Physical Layer Protocols"
