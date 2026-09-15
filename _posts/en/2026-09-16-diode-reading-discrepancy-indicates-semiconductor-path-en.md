---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diode Reading Discrepancy Indicates Semiconductor Path
translated: false
type: note
---

Question: `100C07` reads **1.6 V in one probe direction and 0.4 V in the reverse direction** in diode mode. What does that mean?

Answer: **That is not a normal short indication.** The fact that you get **different readings in the two directions** means there is semiconductor behavior / circuitry between that node and ground.

Your measurement is roughly:

```text
Direction 1:  → 1.6 V
Direction 2:  → 0.4 V
```

The important part is:

```text
0.4 V ≠ 0.0 V
1.6 V ≠ 0.0 V
```

So this is **very different from your `5KA51` measurement of ~0.1 Ω**.

### But I need one clarification

You said:

> test 1 one is 1.6v, one is 0.4v test 2

I think you mean you measured `100C07` **both directions**:

```text
RED → 100C07, BLACK → GND = 1.6 V
BLACK → 100C07, RED → GND = 0.4 V
```

If that's correct, tell me **exactly what `100C07` is**:

* Is it a **capacitor**?
* A **resistor**?
* A **diode**?
* Or can you send a close-up photo of the PCB marking?

Because the marking `100C07` by itself isn't enough to identify the component reliably.

Also, **don't use the continuity beep to judge this component**. For this measurement, the diode-mode voltage readings are the useful information.
