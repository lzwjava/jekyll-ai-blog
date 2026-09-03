---
audio: false
generated: true
image: false
lang: en
layout: post
title: Connecting Front Panel Headers
translated: false
type: note
---

Question: How do I connect `POWER SW`, `RESET SW`, `HDD LED`, and `POWER LED +/-` to the motherboard's `F_PANEL` header?

Answer:

The usual front-panel layout looks like this:

```text
F_PANEL
┌─────────────────────────────┐
│ 1  2  3  4  5  6  7  8  9 10 │
│ ●  ●  ●  ●  ●  ●  ●  ●  ●  ○ │
│ ●  ●  ●  ●  ●  ●  ●  ●  ●  ● │
│ 11 12 13 14 15 16 17 18 19 20 │
└─────────────────────────────┘
```

But **the exact pinout is motherboard-specific**. The safest common Intel/ATX arrangement is:

```text
        F_PANEL

HDD LED +   HDD LED -
    |           |
    ●           ●

POWER LED +  POWER LED -
    |            |
    ●            ●


POWER SW
   ● ●

RESET SW
   ● ●
```

### Important point

For the **switches**:

```text
POWER SW  →  either direction
RESET SW  →  either direction
```

They are just momentary switches. Polarity does **not** matter.

For the **LEDs**:

```text
HDD LED
  + → LED+
  - → LED-

POWER LED
  + → LED+
  - → LED-
```

Polarity **does** matter. If an LED doesn't light, power off and reverse its connector.

If you're working on your **Lenovo L-IG41M3**, send me a clear photo of the motherboard around the `F_PANEL` pins. The Lenovo pinout may differ from the generic ATX layout, and I can mark **exactly which two pins are POWER SW, RESET SW, HDD LED, and POWER LED**.

I can also walk you through using the motherboard's `F_PANEL` pins to **start the PC with a screwdriver**, which is useful when testing a motherboard outside the case.
