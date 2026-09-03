---
audio: false
generated: true
image: false
lang: en
layout: post
title: Connecting Probes on DSO153
translated: false
type: note
---

Question: How do I connect the red and black probes on a FNIRSI DSO153 portable oscilloscope?

Answer:

The key idea is:

* **Black probe = ground/reference (GND)**
* **Red probe = measurement point**
* The oscilloscope measures **voltage difference: `V(red) − V(black)`**

For example, if you want to measure a **12 V DC power rail**:

```text
12 V PSU / motherboard

       +12V ────────────────●  ← red probe
                            │
       GND ─────────────────●  ← black probe
```

The screen should show approximately **+12 V DC**.

### For your motherboard/GPU experiments

If the board is powered on and you want to measure a GPU power rail:

```text
Multimeter / oscilloscope

BLACK ───────── GND
RED   ───────── test point / coil / capacitor positive side
```

Good GND points are usually:

* motherboard metal shield / grounded chassis
* PSU GND
* large capacitor negative terminal
* clearly marked `GND` test point
* PCIe slot ground pin

Then touch the **red probe** to the voltage rail you want to inspect.

For example:

```text
             GPU
       ┌───────────────┐
       │               │
       │   VRM         │
       │  [coil]       │
       │    ●──────────┤ ← red probe
       │               │
       └───────────────┘
             │
             GND ──────── black probe
```

### Important difference from a multimeter

With a **multimeter**, you can put the probes across two points and read DC voltage.

With an **oscilloscope**, you normally want:

```text
black → stable GND
red   → signal/power rail
```

Then the DSO153 can show the **waveform over time**, not just the voltage.

For example, a switching regulator might look roughly like:

```text
Voltage
  ^
  |    ┌───┐   ┌───┐   ┌───┐
  |    │   │   │   │   │   │
  |────┘   └───┘   └───┘   └───→ time
  |
  +---------------------------->
```

### ⚠️ One very important warning

**Do not blindly connect the black probe to an arbitrary point.**

On a normal grounded DC motherboard, finding GND is straightforward. But if you're measuring **mains AC, an isolated power supply primary side, or other high-voltage circuitry**, the probe connection can create a short circuit or shock hazard.

For your current **Lenovo L-IG41M3 + GT730 repair experiments**, start with the **low-voltage DC side**:

```text
BLACK → motherboard GND
RED   → 12V / 5V / 3.3V / GPU VRM test point
```

If you upload a **photo of your DSO153 and its probe/connectors**, I can point out exactly which connector is the probe input and show you where to put red/black for your Lenovo board.
