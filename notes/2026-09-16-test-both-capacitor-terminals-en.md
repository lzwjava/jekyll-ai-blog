---
audio: false
generated: true
image: false
lang: en
layout: post
title: Test both capacitor terminals
translated: false
type: note
---

Question: If the RTX 3060 capacitor reads **beep in continuity mode** and **0.1 Ω in the 200 Ω range**, does that mean the rail is shorted?

Answer: **Yes, 0.1 Ω is a strong indication of a short — but first rule out the measurement setup.**

If you are measuring:

```text
Black probe → HDMI metal shield (GND)
Red probe   → one side of 5KA51
```

and the meter shows:

```text
Continuity:  beep
200 Ω mode:  0.1 Ω
```

then that capacitor pad is essentially at ground potential.

### But there's one critical detail

A capacitor itself can have **one terminal connected directly to ground**. So if `5KA51` is a normal decoupling capacitor:

```text
GPU power rail ─────┬──── capacitor ──── GND
                    │
                  5KA51
```

then:

```text
Pad A → GND ≈ 0 Ω       ← NORMAL
Pad B → GND ≈ low Ω     ← potentially a shorted power rail
```

So **0.1 Ω on one side of the capacitor is not enough to diagnose a short.**

### Do this test

Measure **both sides** of `5KA51` against the HDMI shield:

```text
          5KA51
          ┌───┐
Pad A ────┤   ├──── Pad B
          └───┘
            │
           GND
```

Record:

```text
Pad A → GND = ____ Ω
Pad B → GND = ____ Ω
```

Also, with the GPU **completely powered off and disconnected**, touch the two probes together:

```text
Probe ↔ Probe = probably ~0.1 Ω
```

If you get ~0.1 Ω with the probes shorted, **0.1 Ω is partly the resistance of your probes/leads**, so a measured 0.1 Ω may actually mean "essentially zero."

**Send me the two resistance readings for both sides of `5KA51`**, and ideally a close-up photo of that capacitor. Then we can determine whether you're actually looking at a shorted GPU rail.
