---
audio: false
generated: true
image: false
lang: en
layout: post
title: APW8720 Pin Resistance to Ground Guide
translated: false
type: note
---

Question: With the **black probe on GND**, what should I expect on the 8 pins of **APW8720**, and which pins should show resistance to ground?

Answer: We can be much more precise for **APW8720** now. The datasheet confirms that it is an 8-pin single-buck PWM controller. ([Scribd][1])

### APW8720 — exact 8-pin pinout

For the **SOP-8 package**, viewed from the top with pin 1 at the marked corner:

```text
              APW8720
          ┌─────────────┐
 Pin 1    │             │   Pin 8
 BOOT     │             │   PHASE
 Pin 2    │             │   Pin 7
 UGATE    │             │   COMP
 Pin 3    │             │   Pin 6
 GND      │             │   FB
 Pin 4    │             │   Pin 5
 LGATE    │             │   VCC
          └─────────────┘
```

This is the manufacturer's pin configuration. ([Scribd][1])

### With black probe on GND

Assuming **black probe → board GND**, the important thing is:

|   Pin | Name        | What it connects to                       | Resistance to GND                                  |
| ----: | ----------- | ----------------------------------------- | -------------------------------------------------- |
| **1** | BOOT        | Bootstrap capacitor / gate-driver circuit | Usually **not a simple short**                     |
| **2** | UGATE       | High-side MOSFET gate                     | Usually **high / variable**                        |
| **3** | **GND**     | Ground                                    | **~0 Ω**                                           |
| **4** | LGATE/OCSET | Low-side MOSFET gate + current setting    | Usually **not 0 Ω**                                |
| **5** | VCC         | IC power supply                           | Usually **some resistance**, not necessarily low   |
| **6** | FB          | Output-voltage feedback divider           | Usually **some measurable resistance**             |
| **7** | COMP        | Compensation network                      | Usually **some measurable resistance/capacitance** |
| **8** | PHASE       | MOSFET switching node                     | **Low/variable depending on MOSFETs**              |

The datasheet specifically says pin 3 is signal/power ground, pin 5 is the 5–12 V supply, pin 6 is feedback, pins 2/4 drive the high/low-side MOSFETs, and pin 8 is the PHASE node. ([Scribd][1])

### But here's the important repair point

**Don't interpret "resistance" as simply "this pin must have resistance" or "this pin must have OL."**

For example:

```text
Pin 6 FB
   │
   ├── resistor ── VOUT
   │
   └── resistor ── GND
```

So measuring:

```text
black → GND
red   → Pin 6
```

can give you a finite resistance.

But:

```text
Pin 8 PHASE
   │
   └── MOSFET ── GND
```

can also give a finite/low resistance because you're measuring through the **external MOSFET circuit**, not necessarily through the APW8720 itself.

### What I would measure on your Quadro 410

**Power OFF first.**

Set multimeter to resistance Ω.

Black probe:

```text
BLACK → PCB GND
```

Then measure:

```text
RED → 1
RED → 2
RED → 3
RED → 4
RED → 5
RED → 6
RED → 7
RED → 8
```

Record the actual values, e.g.:

```text
1:  18.2 kΩ
2:  OL
3:  0.2 Ω
4:  12.4 kΩ
5:  2.1 kΩ
6:  4.7 kΩ
7:  8.3 kΩ
8:  1.2 Ω
```

**Those numbers would be much more useful than simply saying "has resistance."**

Also, **pin 8 is particularly interesting** on a GPU VRM because PHASE is the switching node between the high-side and low-side MOSFETs. The APW8720 datasheet explicitly identifies it as the high-side return / low-side MOSFET current-sensing node. ([Scribd][1])

For the **V5F20 5-pin**, I still need the PCB/photo to identify its exact pinout. `V5F20` by itself isn't enough to safely assign pins 1–5.

[1]: https://www.scribd.com/document/806408647/APW8720-ANPEC?utm_source=chatgpt.com "Apw8720 Anpec | PDF | Electrical Engineering | Electronics"
