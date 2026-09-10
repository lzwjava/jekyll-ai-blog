---
audio: false
generated: true
image: false
lang: en
layout: post
title: Scope Ground to Motherboard GND
translated: false
type: note
---

Question: The ATX connector is already plugged into the PSU, so where do you connect the oscilloscope ground?

Answer: **That's exactly fine.** The oscilloscope ground does **not** need a separate power supply connection.

The motherboard's ATX **black wires are GND**, and all of those grounds are electrically connected together.

So:

```text
PSU
 │
 │ ATX 24-pin
 ▼
Motherboard GND ──────────────┐
                             │
                             │
                       Scope GND clip
                             │
                       DSO153 probe
                             │
                             ▼
                       signal / voltage
```

For example, measuring +5VSB:

```text
ATX connector

purple wire (+5VSB) ─────── probe tip
black wire (GND) ────────── scope GND clip
```

The PSU is already powering the motherboard. **You simply attach the scope probe to the existing circuit.**

### Very important

Your DSO153's ground clip should go to **motherboard GND**, such as:

* a black ATX wire
* an exposed motherboard GND point
* the metal shield/ground plane

Do **not** connect the scope ground to a random signal pin.

And because the DSO153 is battery-powered/portable, this is particularly convenient—you can probe the powered motherboard directly.

If you want, send me a photo of your **ATX 24-pin connector and DSO153 probe**, and I can point out exactly which wire is GND and where to put the probe.