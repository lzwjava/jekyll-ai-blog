---
audio: false
generated: true
image: false
lang: en
layout: post
title: Frequency, Vmin, Vmax on Oscilloscope
translated: false
type: note
---

Question: What do **Frequency, Vmin, and Vmax** mean on an oscilloscope?

Answer:

They describe the voltage waveform you are measuring:

* **Frequency (Hz)** — how fast the waveform repeats.

  * `1 Hz` = 1 cycle/second
  * `1 kHz` = 1,000 cycles/second
  * `1 MHz` = 1,000,000 cycles/second
  * Period and frequency are related by:

    $$
    f=\frac{1}{T}
    $$

* **Vmax** — the highest voltage reached by the waveform during the measurement window.

* **Vmin** — the lowest voltage reached.

For example, if your oscilloscope shows a square wave switching between **0 V and 5 V** at **1 kHz**:

```text
Voltage
  5V ──┐    ┌────┐    ┌────
       │    │    │    │
  0V ──┴────┘    └────┘
       <--- 1 ms --->

Frequency = 1 kHz
Vmax      = 5 V
Vmin      = 0 V
```

Then:

$$
V_{pp}=V_{max}-V_{min}=5V
$$

For your **motherboard/GPU repair measurements**, these three numbers are especially useful: **Vmin/Vmax tell you whether a power rail is actually reaching the expected voltage, while frequency tells you whether a switching regulator is running.**

For example, a buck converter might show something like:

```text
Vmin ≈ 0.2 V
Vmax ≈ 12 V
Frequency ≈ 500 kHz
```

That is very different from seeing a flat `12 V` DC signal.

If you want, I can next show you **exactly where to put the red/black oscilloscope probes on your motherboard to measure a switching regulator and actually get Frequency/Vmin/Vmax readings**.
