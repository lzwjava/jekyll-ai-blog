---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI MAG B760M Mortar JFP1 Pinout
translated: false
type: note
---

Question: What are the pin definitions for the JFP1 (front panel) header on the MSI MAG B760M Mortar motherboard?

Answer:

JFP1 on the MAG B760M Mortar (all three SKUs: Mortar, Mortar WIFI, Mortar MAX WIFI) is the standard front-panel switch/LED header — it controls power on, power reset, and the LEDs on your PC case/chassis, with Power Switch/Reset Switch headers for the power/reset buttons, a Power LED header, and an HDD LED header that indicates hard disk activity. It's a 2×5 pin block with pin 9 physically absent as a keying/orientation guide, giving you 9 usable pins.

This is MSI's implementation of the Intel Front Panel I/O Connectivity Design Guide header, and the pin definition table is identical across essentially all modern MSI boards (B650, B760, Z790, etc.) — I pulled the canonical table below, sourced from MSI's own manuals for boards using this same connector:

```
JFP1 Pin Definition (2x5 header, pin 9 = no pin / key)

 1  3  5  7  9(key)
 2  4  6  8  10

Pin | Signal        | Description
----+---------------+---------------------------------------------
 1  | HD_LED+       | Hard disk LED, pull-up
 2  | FP PWR/SLP+   | Power LED pull-up
 3  | HD_LED-       | Hard disk activity LED cathode
 4  | FP PWR/SLP-   | Power LED pull-up (2nd LED lead)
 5  | RST_SW-       | Reset switch, low reference, pull-down to GND
 6  | PWR_SW+       | Power switch, high reference, pull-up
 7  | RST_SW+       | Reset switch, high reference, pull-up
 8  | PWR_SW-       | Power switch, low reference, pull-down to GND
 9  | (no pin)      | Key — orientation guide
10  | RSVD_DNU      | Reserved, do not connect
```

Practical wiring for your case cables:
- **Power Switch (2-pin, no polarity)** → pins 6 + 8
- **Reset Switch (2-pin, no polarity)** → pins 5 + 7
- **Power LED (2-pin, has polarity)** → pins 2 + 4 (or 4-pin if your case uses dual-color PWR/SLP, straddling those same signal pairs)
- **HDD LED (2-pin, has polarity)** → pins 1 + 3

Notes for your build:
- Power and reset switches are momentary contacts — polarity doesn't matter, they'll work either way.
- LEDs are polarity-sensitive: reversed wiring just means the LED won't light, no hardware damage.
- On the physical board layout, JFP1 sits near JTPM1, SATA7/8, and JUSB1/JUSB2, in the lower-right area of the board (this matches typical MSI mATX layouts, JFP1 bottom-right corner near the SATA ports).
- JFP2 (separate 8-pin header) is only for Buzzer/Speaker — not required for boot, useful for old-school POST beep codes.

References:

- [MSI MAG B760M MORTAR MAX WIFI / WIFI / MORTAR Motherboard Manual](https://www.manualslib.com/manual/3270648/Msi-Mag-B760m-Mortar-Max-Wifi.html)
- [MSI PRO B760M-A WIFI DDR4 — JFP1 description](https://www.manualslib.com/manual/3085563/Msi-Pro-B760m-A-Wifi-Ddr4.html?page=35)
- [MSI JFP1 pin definition table (MS-7346 manual, canonical across MSI line)](https://www.manualslib.com/manual/360307/Msi-Ms-7346.html?page=31)
- [MSI HOW-TO install front panel connectors (JFP1) — video](https://youtu.be/DPELIdVNZUI)
