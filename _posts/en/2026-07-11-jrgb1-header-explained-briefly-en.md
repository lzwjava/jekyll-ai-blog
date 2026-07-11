---
audio: false
generated: true
image: false
lang: en
layout: post
title: JRGB1 Header Explained Briefly
translated: false
type: note
---

Question: What does the JRGB1 header mean on the MSI MAG B760M Mortar WiFi motherboard?

Answer:

`JRGB1` is a **4-pin 12V RGB LED header** on the board — the standard (non-addressable) Mystic Light connector, distinct from the `JARGB_V2` headers.

**Key specs:**

- Connects standard 5050 RGB LED strips running at 12V
- Supports up to 2 meters of continuous 5050 RGB LED strip, max power rating 3A at 12V
- Controlled through MSI's **Mystic Light** software (part of MSI Center)

**Don't confuse it with `JARGB_V2`:** the board also has 1-2 `JARGB_V2` headers for addressable RGB (individually controllable LEDs, 5V, 3-pin, up to 240 LEDs). The JRGB connector and the JARGB_V2 connector provide different voltages, and connecting the ARGB 5V LED strip to the JRGB connector will result in damage to the LED strip — so pin/voltage mismatch here is a real "let the smoke out" hazard, not just a compatibility footnote.

**Quick reference table:**

| Header | Voltage | Pins | Use case |
| --- | --- | --- | --- |
| `JRGB1` | 12V | 4-pin | Standard non-addressable RGB strips |
| `JARGB_V2_1/2` | 5V | 3-pin | Addressable (individually controllable) ARGB Gen1/Gen2 strips |

If you're wiring this up on a build, the practical failure mode to watch for: some cheap "RGB" strips sold on Taobao/AliExpress are mislabeled — always check the strip's own spec sheet for 12V/4-pin vs 5V/3-pin before plugging in, since the connector shells can sometimes be forced into the wrong header if you're not careful.

References:

- [MSI MAG B760M MORTAR MAX WIFI Manual - ManualsLib](https://www.manualslib.com/manual/3270648/Msi-Mag-B760m-Mortar-Max-Wifi.html)
- [MSI MAG B760M MORTAR WIFI - Official Product Page](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI)
