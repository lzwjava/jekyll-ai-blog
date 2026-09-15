---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multimeter Continuity Mode Explained
translated: false
type: note
---

Question: On the **Chanzhoudao 8901S**, the position just below `200 Ω` sometimes shows voltage and sometimes resistance. Is that the **beeper/continuity mode**?

Answer: **Yes — most likely you are on the combined diode/continuity position, not a normal 200 Ω resistance range.**

The important distinction is:

```text
200 Ω position
    ↓
Measures resistance
    ↓
Display: Ω
    ↓
Your 5KA51 → 0.1 Ω
```

The position **one step below 200 Ω** with the **buzzer/diode symbol** can have multiple functions selected by a button:

```text
       diode / continuity position
                  │
          ┌───────┴───────┐
          ↓               ↓
     🔊 Continuity      →| Diode
       beep + Ω            voltage
```

In **continuity mode**, the meter injects a small test signal and beeps when the resistance is below its internal threshold. The exact threshold varies by meter; ~30–50 Ω is common. ([Scribd][1])

In **diode mode**, the display shows a **voltage drop**, for example:

```text
0.000 V
0.500 V
0.650 V
1.200 V
OL
```

So if your 8901S is showing **volts**, you have likely selected the **diode function** within that combined position.

### For your RTX 3060 test

For what you're doing, I recommend using the **actual 200 Ω range** and reading the number:

```text
Black → HDMI shield / GND
Red   → 5KA51 pad

Display:
0.1 Ω  ← essentially short
10 Ω
50 Ω
150 Ω
OL
```

Don't use the beep alone to diagnose the GPU. **Beep = "below my beep threshold," not necessarily "GPU is shorted."** ([iTechGuides][2])

And one very important thing: **if the 200 Ω range gives 0.1 Ω, first touch the two probes together.** If they also show `0.1 Ω`, that's simply the resistance of your test leads/contact, and your actual PCB resistance may be close to that.

If you send me a **photo of the 8901S dial/display**, I can tell you exactly which function that position is on your particular meter.

[1]: https://www.scribd.com/document/559866223/ZT102?utm_source=chatgpt.com "Digital Multimeter User Manual | PDF | Switch | Diode"
[2]: https://www.itechguides.com/understanding-multimeter-symbols-and-ground-gnd-a-practical-safety-guide/?utm_source=chatgpt.com "Understanding Multimeter Symbols and Ground (GND) Safely"
