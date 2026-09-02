---
audio: false
generated: true
image: false
lang: en
layout: post
title: DC Voltage Measurements on PC Hardware
translated: false
type: note
---

Question: How can you use a multimeter to experiment with DC voltages on a Lenovo L-IG41M3 motherboard and a GT730 GPU?

Answer: Yes. This is a good hands-on way to learn electronics. **For a powered-on board, use DC voltage mode and measure relative to GND.** Start with large, obvious rails and headers—not tiny IC pins.

### 1. Set up the multimeter

```text
Black probe → COM
Red probe   → VΩ
Dial         → DC Voltage (V⎓)
```

Use the **20 V range** if your meter is not autoranging.

Then:

```text
BLACK = GND
RED   = test point
```

Your meter measures:

```text
V(test point) - V(GND)
```

---

## 2. Lenovo L-IG41M3: good places to start

If the board is running, these are much better experiments than randomly probing chips.

### ATX power connector

Find the large **24-pin ATX connector**.

Use a black probe on a ground pin and red probe on different power pins.

Typical values:

```text
Yellow → ~12 V
Red    → ~5 V
Orange → ~3.3 V
Black  → ~0 V
Purple → ~5 V standby
```

The **purple 5VSB** is especially interesting:

```text
PC OFF but PSU connected
        ↓
purple wire
        ↓
~5 V
```

That teaches you that a motherboard can have power even when the computer appears "off."

### Power switch header

The front-panel connector is another excellent experiment.

The power button is basically a **momentary switch**:

```text
PWR_SW pin ──────┐
                 │ button
GND ─────────────┘
```

With the machine powered off, you can use **continuity mode** to identify the two switch pins.

With the machine running/standby, switch back to **DC voltage** and measure each pin relative to GND.

**Do not inject voltage into the header.** You're only measuring.

---

## 3. F_AUDIO is NOT a good place to start

`F_AUDIO` is the front-panel audio connector.

It contains audio signals and ground, rather than being a convenient power rail.

You can experiment with it later, but don't expect:

```text
F_AUDIO → 12 V
```

It's not a power connector.

Similarly, don't randomly probe USB/data/PCIe signal pins expecting meaningful DC voltages. High-speed differential signals aren't what you want for your first experiments.

---

# 4. Then experiment with the GT730

This gets much more interesting.

First determine whether your particular GT730 gets power from:

```text
PCIe slot only
```

or

```text
PCIe slot + auxiliary power connector
```

Many GT730 variants are slot-powered, but **GT730 is a family of different board designs**, so don't assume the exact voltage arrangement without looking at your PCB.

With the card installed and powered:

### PCIe slot

You can measure the slot's power rails.

Conceptually:

```text
PCIe slot

3.3 V  ──────────→ GPU
12 V   ──────────→ GPU
GND    ──────────→ probe reference
```

Put:

```text
BLACK → metal bracket / known GND
RED   → PCIe power pin
```

You should find approximately:

```text
3.3 V rail → ~3.3 V
12 V rail  → ~12 V
```

This is a much better experiment than randomly touching GPU IC pins.

---

# 5. Learn the difference between voltage and current

This is **very important**.

Your multimeter in voltage mode measures:

```text
          ┌──── meter ────┐
          │               │
          └─── parallel ──┘
                 │
       ┌─────────┴─────────┐
       │    motherboard    │
       └───────────────────┘
```

You're measuring **voltage**.

You are **not measuring current**.

To measure current, the meter has to be inserted **in series**:

```text
PSU ─── meter ─── motherboard
             ↑
          current
```

Don't try this experiment on your motherboard yet. Accidentally putting the multimeter's current input across 12 V and GND can effectively short the power supply.

---

# 6. A really useful repair-learning experiment

Once you're comfortable with DC voltage, do this:

### PC OFF

Set:

```text
Ω / resistance
```

Measure resistance between:

```text
12V → GND
5V  → GND
3.3V → GND
```

Then:

### PC ON

Set:

```text
V⎓
```

Measure the same rails:

```text
12V → GND
5V  → GND
3.3V → GND
```

Now you're beginning to build a very useful diagnostic table:

```text
             OFF             ON
12V → GND    resistance      ~12V
5V → GND     resistance      ~5V
3.3V → GND   resistance      ~3.3V
```

And later you can investigate **VRM power sequencing**:

```text
PSU
 │
 ├── 12V
 │
 ├── 5V
 │
 └── 3.3V
       │
       ↓
 motherboard regulators
       │
       ├── CPU Vcore
       ├── RAM voltage
       └── chipset rails
```

That's where a cheap dead motherboard becomes a really good electronics laboratory.

**One thing I'd strongly recommend:** if you can take a clear photo of the **L-IG41M3 motherboard, especially the connectors and the printed labels around the headers**, upload it. I can mark out **specific pins to probe—ATX 24-pin, CPU 4-pin, front-panel/PWR_SW, F_AUDIO, PCIe slot—and give you a probe-by-probe experiment sequence.**
