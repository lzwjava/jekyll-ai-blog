---
audio: false
generated: true
image: false
lang: en
layout: post
title: Oscilloscope Measurements on L-IG41M3
translated: false
type: note
---

Question: You just want to **learn how to get real oscilloscope measurements from the L-IG41M3**, not diagnose a specific fault yet.

Answer: Perfect. Start with **easy DC measurements**. Your oscilloscope should show actual voltage values and waveforms.

### 1. Start with +5VSB

The easiest point is the **24-pin ATX connector**.

Set your scope:

```text
Probe:       ×10
Coupling:    DC
Vertical:    2 V/div
Time:        1 ms/div
```

Connect:

```text
scope GND clip → motherboard GND
probe tip      → purple PSU wire (+5VSB)
```

You should see approximately:

```text
      ~5 V
       ─────────────────────
```

So you're already measuring a real value:

```text
V ≈ 5.0 V
```

This is a good first oscilloscope exercise because it should be stable.

### 2. Measure +12 V

Move the probe tip to a **yellow wire** on the ATX connector.

Expected:

```text
V ≈ 12 V
```

You should see:

```text
12V ───────────────────────
```

### 3. Measure +5 V

Probe a **red wire**:

```text
V ≈ 5 V
```

### 4. Measure +3.3 V

Probe an **orange wire**:

```text
V ≈ 3.3 V
```

So you can literally make yourself a little oscilloscope exercise:

```text
purple → ~5 V
yellow → ~12 V
red    → ~5 V
orange → ~3.3 V
black  → GND
```

**Do not put the scope ground clip on anything except GND.**

---

### 5. Then try the F_PANEL signal

Once you're comfortable, connect:

```text
GND clip → pin 11
probe    → pin 9
```

Use:

```text
1 V/div
500 ms/div
DC coupling
```

Now briefly touch:

```text
pin 9 ↔ pin 11
```

Instead of a constant voltage, you should see a **pulse/transition**.

That's much more interesting than simply measuring a DC rail:

```text
HIGH ────────────┐
                 │
                 └──────────── HIGH
                 ↑
             button press
```

You can then experiment with the scope's:

* `Vmax`
* `Vmin`
* `Vpp`
* frequency
* period
* trigger

That will teach you what the numbers actually mean.

### If you just want to practice

You don't even need the motherboard initially. Take your oscilloscope + probe and measure:

```text
5VSB → DC voltage
12V  → DC voltage
5V   → DC voltage
3.3V → DC voltage
```

Then measure **F_PANEL pin 9 while pressing the button**. That's probably the best next step for learning the scope on this board.

If you send me a photo of your **DSO153 screen + probe + L-IG41M3 board**, I can tell you exactly where to put the probe and what values you should expect.