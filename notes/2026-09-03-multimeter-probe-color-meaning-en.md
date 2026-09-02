---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multimeter Probe Color Meaning
translated: false
type: note
---

Question: What do the **black and red probes** on a 晨洲岛 8901S multimeter mean, and how do I use them?

Answer:

The basic idea is very simple:

* 🔴 **Red probe = measurement / positive**
* ⚫ **Black probe = COM / reference / negative**

On the multimeter, plug them in like this:

```text
BLACK probe → COM
RED probe   → V / Ω / mA (depending on what you're measuring)
```

### For your motherboard/GPU experiments

Since you're testing **DC voltage**, set the meter to **DC voltage** (`V⎓`).

Then:

```text
           Motherboard
        ┌─────────────────┐
        │                 │
BLACK ──┤ GND             │
        │                 │
RED ────┤ test point      │
        └─────────────────┘

Display: voltage at RED relative to BLACK
```

For example, if you put:

```text
BLACK → motherboard metal ground / GND
RED   → 12V rail
```

you should see approximately:

```text
+12 V
```

If you reverse them:

```text
RED   → GND
BLACK → 12V
```

the meter will typically show:

```text
-12 V
```

The minus sign simply means **your red probe is at a lower voltage than your black probe**.

### Very important: voltage vs current

For what you're doing right now, **measure voltage first**.

Voltage:

```text
Meter is connected ACROSS two points

        ┌─── circuit ───┐
RED ────●               ●──── BLACK
        │               │
        └───────────────┘
```

Do **NOT** put the multimeter in current (`A`) mode and touch it across a power rail and GND. That's effectively creating a short through the meter and can damage the board/meter.

So for your Lenovo motherboard and GT730:

```text
DC voltage test:

BLACK → GND
RED   → point you're curious about
```

You can safely learn a lot by measuring **5V, 12V, 3.3V, USB VBUS, PCIe power rails, etc.**

If you upload a **photo of your 8901S and the Lenovo L-IG41M3 motherboard**, I can point out exactly where to put the black and red probes for your first measurements.
