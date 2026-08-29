---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multimeter Display Flashes to Zero
translated: false
type: note
---

Question: When using a multimeter to measure resistance, the display briefly shows a number then flashes to 0 — what does this mean?

Answer:

This behavior typically means one of two things:

**1. The resistance is too low for the selected range (most common)**

- If you're on a high range like **200kΩ** and the actual resistor is only a few ohms, the meter reads it as essentially **0** relative to that scale.
- **Fix:** Switch to a lower range (e.g., 200Ω or 2kΩ) to get a proper reading.

**2. Auto-ranging settling behavior**

- Some multimeters briefly display a number while the internal circuit is stabilizing, then "snaps" to the stable reading — which could legitimately be near 0Ω.
- This is normal for low-resistance components like wire, fuses, or coil windings.

**3. The resistor may be shorted or damaged**

- A reading that goes to **0Ω** and stays there on a low range means the resistor has failed short-circuit (内部短路).

---

**Quick Diagnosis Guide:**

| Situation | Meaning |
| --- | --- |
| Shows number → flashes 0, on high range | Range too high, scale mismatch |
| Shows 0 on low range (e.g. 200Ω) | Resistor is shorted / very low resistance |
| Flashes briefly then stabilizes | Normal auto-range settling |
| Shows **OL** or **1.** | Resistance is too HIGH for the range |

**General tip:** Always start from a **higher range** and work your way **down** until you get a stable, non-zero reading in the middle of the scale for best accuracy.

References:

- [How to Use a Multimeter – Measuring Resistance](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter/measuring-resistance)
- [Multimeter Basics – Fluke](https://www.fluke.com/en-us/learn/blog/electrical/how-to-measure-resistance)
