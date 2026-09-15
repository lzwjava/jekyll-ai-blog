---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 3060 Capacitor Beep Meaning
translated: false
type: note
---

Question: What does the **beep** mean when testing the RTX 3060 capacitor `5KA51` with a multimeter?

Answer:
If your multimeter is in **resistance/continuity mode**, the beep usually means it initially sees a **low resistance path to ground**.

For a GPU capacitor, that **does not automatically mean the capacitor is bad**.

If you have:

* Black probe → HDMI shield/ground
* Red probe → one side of `5KA51`
* Meter initially beeps
* As you turn the range/dial toward ~**200 Ω**, the beep changes or disappears

that behavior can be completely normal because you're measuring **the entire power rail**, not just the capacitor. The capacitor charges from the meter's test voltage, so the measured resistance can change with time.

### The important test

Don't judge it by the beep alone. Measure the actual resistance:

```text
Black → GND
Red   → capacitor pad

Read Ω
```

Then reverse the probes:

```text
Red   → GND
Black → same capacitor pad
```

If this is a GPU power rail, something like:

```text
0.0–1 Ω       ← suspicious / possible short
1–10 Ω        ← potentially suspicious, depends on the rail
10–100 Ω      ← can be completely normal on some GPU rails
100+ Ω        ← generally less suspicious
```

The exact expected value depends heavily on **which rail `5KA51` belongs to**.

Also, if you're using a **200 Ω range**, the meter's beep threshold may simply be telling you that the resistance is below its continuity threshold. That's why the beep alone isn't useful for diagnosing the RTX 3060.

If you can send me a **photo of the `5KA51` capacitor and surrounding PCB area**, I can help identify which rail you're measuring and what resistance you should expect.
