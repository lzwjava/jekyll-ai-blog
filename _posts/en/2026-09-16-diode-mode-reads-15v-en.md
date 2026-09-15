---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diode Mode Reads 1.5V
translated: false
type: note
---

Question: In the `100C07` component, when using the **continuity/diode position**, the meter shows about **1.5 V**. What does that mean?

Answer: **If your 8901S is actually in diode-test mode, `1.5 V` means the meter is measuring a ~1.5 V forward voltage drop/path. It is not saying that the component has a resistance of 1.5 Ω.**

The key point is that your 8901S's shared position can contain **continuity + diode test**. In diode mode, the meter injects a small current and displays the voltage developed across the semiconductor junction/path. ([Fluke][1])

For example:

```text
Diode mode:

red probe ──> [ semiconductor / circuit ] ──> black probe

display: 1.5 V
         ↑
     voltage drop
```

### But 1.5 V is NOT automatically "bad"

`100C07` is apparently still **on the RTX 3060 PCB**, so you're not necessarily measuring an isolated diode. Other components and semiconductor junctions connected to that node can produce a reading. Fluke specifically warns that in-circuit diode measurements can be affected by other paths. ([Fluke][1])

For comparison, an ordinary silicon diode often shows roughly **0.5–0.8 V** forward drop. ([Fluke][1])

So:

```text
0.6 V   → common silicon diode forward drop
1.5 V   → could be a semiconductor/network path
OL      → no conducting path in that polarity
0.0 V   → very low-resistance path / possible short
```

### The most useful test for your GPU

Keep the GPU completely **unpowered**.

Measure `100C07` in **both directions**:

```text
Test 1:
RED   → 100C07
BLACK → GND
       = ____ V

Test 2:
BLACK → 100C07
RED   → GND
       = ____ V
```

Also tell me whether the meter **beeps continuously**, **beeps once**, or **doesn't beep** for each direction.

**Don't interpret `1.5 V` as `1.5 Ω` or multiply it by 200.** In diode mode, `1.5 V` is a voltage-drop measurement. ([Fluke][1])

References:

* [Fluke — How to Test Diodes with a Digital Multimeter](https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-test-diodes?utm_source=chatgpt.com)
* [Fluke — Multimeter manual: diode/continuity testing](https://assets.fluke.com/manuals/12______umeng0100.pdf?utm_source=chatgpt.com)

[1]: https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-test-diodes?utm_source=chatgpt.com "How to Test Diodes with a Digital Multimeter | Fluke"
