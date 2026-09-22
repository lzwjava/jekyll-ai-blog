---
audio: false
generated: true
image: false
lang: en
layout: post
title: Testing 12V on PCIe 8-Pin
translated: false
type: note
---

Here's exactly how to test the **12V at the 8-pin PCIe input**:

## Setup

- **Multimeter setting:** DC voltage — dial to **20V DC** (the "V⎓" section, choose "20", not "200m")
- **Board state:** powered ON (plugged into a working PSU via the riser/test bench)
- **Safety:** don't let probes touch adjacent pins at once — shorting 12V to ground will spark

## 1. Find the 8-pin connector

It's the **8-pin power socket at the top edge** of the card (where the PCIe power cable plugs in). Looking at the back of the PCB, you'll see **8 solder joints** where it's soldered — 4 pins in a row, 2 rows.

## 2. Identify +12V vs GND pins

The 8-pin PCIe pinout is:

```
   [12V] [12V] [12V] [GND]     ← top row
   [GND] [GND] [GND] [GND]     ← bottom row
```

Actually, standard PCIe 8-pin (looking at the plug, clip up):

| Pin | Function |
| ----- | ---------- |
| 1 | +12V |
| 2 | +12V |
| 3 | +12V |
| 4 | GND (sense) |
| 5 | GND |
| 6 | GND |
| 7 | GND |
| 8 | GND |

So: **3 pins are +12V, 5 pins are GND.**

## 3. Probe it

1. **Black probe** → any **GND pin** on the connector (or the card's metal bracket / a mounting-hole ground pad)
2. **Red probe** → each of the **3 × +12V pins**, one at a time
3. Read the display

**Expected result: ~12.0 V (11.4–12.6 V is fine)**

## 4. How to interpret

| Reading | Meaning |
| --------- | --------- |
| **~12 V** | ✅ Input power OK — move on to 5V/3.3V test |
| **0 V** | ❌ No power reaching the card — PSU/cable/connector/fuse issue |
| **< 11 V** | ⚠️ Voltage sag — weak PSU or bad cable/connector |

## Quick tips

- If you're using a **riser cable / test bench**, verify the PSU cable itself first: measure directly at the PSU's 8-pin plug (same test) to rule out a bad cable.
- Some boards have the 8-pin on the **side** rather than top — follow where the power cable plugs in.
- If the card also has a **6-pin** connector, test all +12V pins there too.

Tell me what voltage you read, and we'll move to the next rail (5V / 3.3V).
