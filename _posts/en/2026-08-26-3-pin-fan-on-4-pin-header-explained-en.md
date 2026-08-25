---
audio: false
generated: true
image: false
lang: en
layout: post
title: 3-Pin Fan on 4-Pin Header Explained
translated: false
type: note
---

**Question:** Why does the CPU fan on the Gigabyte H81M-DS2 motherboard use a 3-pin connector, and what does that mean?

**Answer:**

First, a clarification: according to the official Gigabyte GA-H81M-DS2 user manual, **all fan headers on this motherboard are actually 4-pin**. So if your fan plug only has 3 pins, that's a property of the **fan itself**, not the motherboard header.

Here's why this happens and what it means:

**Why your fan may have only 3 pins:**

Older or budget CPU coolers often ship with 3-pin connectors. A standard 3-pin fan connector carries three signals: power (+12V), ground, and a tachometer/speed feedback wire. The motherboard controls a 3-pin fan by varying the voltage on the power pin — typically somewhere between about 5V and 12V — to change fan speed.

**How it differs from 4-pin (PWM):**

On 4-pin headers, speed is controlled via PWM (Pulse Width Modulation) — a separate signal tells the fan exactly how fast to spin, while it always receives full 12V. On 3-pin headers, speed control happens by varying the voltage instead.

Both fan types are physically compatible with both header types, so a 3-pin fan will plug into the 4-pin header just fine — the fourth pin simply goes unused.

**What happens when you plug a 3-pin fan into the 4-pin header:**

The PWM pin on the header will be unused, and the fan will likely run at 100% speed all the time unless you configure your BIOS to control it in DC mode (voltage variation). The H81M-DS2 BIOS does offer fan speed control settings, so you can switch the header to DC mode for basic speed adjustment.

**Summary table:**

| | 3-Pin Fan | 4-Pin Fan |
|---|---|---|
| Speed Control | Voltage (DC) | PWM signal |
| Precision | Lower | Higher |
| Compatible with 4-pin header? | ✅ Yes (pin 4 unused) | ✅ Yes |

---

**References:**
- [Gigabyte GA-H81M-DS2 User Manual (ManualsLib)](https://www.manualslib.com/manual/577266/Gigabyte-Ga-H81m-Ds2.html?page=12)
- [CPU Fan Header Guide — SunbeamTech](https://sunbeamtech.com/hardware-guides/cpu-fan-header-where-it-is-and-how-to-use-it/)
- [3-pin vs 4-pin Fan Differences — ElectronicsHub](https://www.electronicshub.org/3-vs-4-pin-fans/)
- [3-pin vs 4-pin Compatibility — PositionIsEverything](https://www.positioniseverything.net/can-i-use-4-pin-fans-on-3-pin-headers-or-vice-versa/)
