---
audio: false
generated: true
image: false
lang: en
layout: post
title: JFP1 Header Pinout Guide
translated: false
type: note
---

That maps perfectly onto the standard JFP1 layout — no ambiguity left. Here's exactly where each wire goes:

```
JFP1 (2x5 header, pin 9 = key/no pin)

 1  3  5  7  9(key)
 2  4  6  8  10
```

| Your cable | JFP1 Pin | Signal |
|---|---|---|
| Power LED+ | **Pin 2** | FP PWR/SLP+ |
| Power LED- | **Pin 4** | FP PWR/SLP- |
| PWR SW (either wire) | **Pins 6 + 8** | PWR_SW+ / PWR_SW- |
| RESET SW (either wire) | **Pins 5 + 7** | RST_SW+ / RST_SW- |

Notes:
- **Power LED is polarity-sensitive** — make sure `+` lands on pin 2 and `−` lands on pin 4. If you get it backwards, the LED just won't light (no damage), so if it doesn't turn on after boot, swap it.
- **PWR SW and RESET SW are not polarity-sensitive** — they're just momentary switches completing a circuit. Either wire can go on either of the two pins in their pair (6/8 for power, 5/7 for reset).
- **Pins 1, 3, 10** are unused in your case (that's the HDD LED slot you don't have a cable for) — leave them empty.
- **Pin 9 is physically missing** on the header itself — that's your orientation key, so your 2×5 connector block should naturally only seat one way.

Once wired, pressing the physical power switch should trigger boot, and the case's power LED should light up once POST completes.
