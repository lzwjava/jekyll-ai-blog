---
audio: false
generated: true
image: false
lang: en
layout: post
title: DSO153 Only for Motherboard Test
translated: false
type: note
---

Question: Should you connect a **DDS (function generator)** or your **DSO153 oscilloscope** to the motherboard?

Answer: **For simply measuring the L-IG41M3, use the DSO153 only.**

* **DSO153 = oscilloscope** → measures voltage/waveforms.
* **DDS = signal/function generator** → generates a voltage waveform.
* You normally **do not need DDS** for motherboard troubleshooting.

For example:

```text
L-IG41M3 ─────── probe ─────── DSO153
 motherboard       │
                   └── measures voltage
```

Start with:

```text
DSO153 GND clip → motherboard GND
DSO153 probe    → +5VSB / +5V / +12V / F_PANEL signal
```

The DDS becomes useful later when you deliberately want to **inject a known signal** into a circuit for testing. Don't inject a DDS signal into motherboard pins until you know exactly what the pin is and its allowable voltage.

If you show me your **DSO153 and DDS**, I can tell you what each connection should look like for your first measurement.