---
audio: false
generated: true
image: false
lang: en
layout: post
title: 200 Ohm Range Measurement Clarification
translated: false
type: note
---

Question: If the meter is on the **200 Ω range** and both sides of `5KA51` read `0.1–0.2`, do I multiply by 200?

Answer: **No. You do not multiply by 200.**

On a **200 Ω range**, the displayed number is already in ohms. So:

```text
0.1  →  0.1 Ω
0.2  →  0.2 Ω
10.0 →  10.0 Ω
50.0 →  50.0 Ω
```

The `200` is the **maximum/range**, not a multiplier. A typical 200 Ω range has 0.1 Ω resolution. ([Fluke][1])

### Your measurement

You have:

```text
5KA51

Pad A → GND = 0.1–0.2 Ω
Pad B → GND = 0.1–0.2 Ω
```

That means **both sides are essentially at ground**.

But there's a very important next test:

**Short the two probes together and read the 200 Ω range.**

For example:

```text
Probe + ─────┐
             ├── together
Probe - ─────┘

Meter = 0.1 Ω
```

If you get `0.1 Ω` or `0.2 Ω`, that's probably your **probe/lead resistance**. Fluke notes that test leads commonly contribute around `0.2–0.5 Ω`, and this should be accounted for when measuring very low resistance. ([Fluke][1])

So if:

```text
Probes shorted:     0.1 Ω
5KA51 pad → GND:    0.1 Ω
```

you **cannot conclude that the GPU rail is exactly 0.1 Ω**. Your meter may simply be measuring approximately the same resistance as the probes.

### One more important point

If **both capacitor pads** really remain ~0.1 Ω after accounting for probe resistance, then the capacitor is sitting between:

```text
GPU rail ──[ 5KA51 ]── GND
   │
   └──────── ~0 Ω ────── GND
```

That would indicate a **very low-resistance path from that GPU rail to ground**, which is suspicious for a power rail.

However, don't immediately assume `5KA51` itself is bad. Measuring a component while it is still soldered to the GPU measures **all parallel paths on the PCB**, not just the capacitor. ([Fluke][1])

**Do this next and give me the numbers:**

```text
1. Probe tips touching each other = ___ Ω

2. 5KA51 left pad → GND = ___ Ω
3. 5KA51 right pad → GND = ___ Ω
```

With those three numbers, we can determine whether the `0.1–0.2 Ω` is just your probe resistance or a genuine near-short on the RTX 3060 rail.

[1]: https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-measure-resistance?utm_source=chatgpt.com "How to Measure Resistance with a Digital Multimeter | Fluke"
