---
audio: false
generated: true
image: false
lang: en
layout: post
title: Oscilloscope Basics for PCB Testing
translated: false
type: note
---

**Question:** What is an oscilloscope (示波器), and how do you use it on a PCB or circuit?

---

**Answer:**

## What is an Oscilloscope?

An **oscilloscope** (示波器) is a test instrument that displays electrical signals as a waveform on a screen — showing **voltage over time**. It lets you *see* what's happening inside a circuit: signal shape, frequency, amplitude, noise, timing, and more.

---

## Key Parts

| Part | Purpose |
| --- | --- |
| **Probe** | Connects to the circuit; has a tip (signal) and ground clip |
| **Display** | Shows the waveform (X = time, Y = voltage) |
| **Timebase** | Controls how fast the X-axis sweeps (time/div) |
| **Voltage scale** | Sets the Y-axis sensitivity (volts/div) |
| **Trigger** | Stabilizes the waveform on screen |

---

## How to Use It on a Board/Circuit

**1. Connect Ground First**
Clip the probe's **ground lead** to the circuit's GND. This is critical — bad ground = noisy/wrong readings.

**2. Touch the Probe Tip to a Test Point**
Place the probe tip on a pin, pad, or component leg you want to measure (e.g., a microcontroller clock pin, power rail, or output signal).

**3. Adjust Voltage Scale (V/div)**
Rotate the volts-per-division knob until the waveform fills roughly 3–6 divisions on screen — not clipped, not tiny.

**4. Adjust Timebase (Time/div)**
Set the time scale to match the signal's period. For a 1 kHz signal, you'd want ~0.5–1 ms/div to see a couple of full cycles.

**5. Set the Trigger**
Set trigger to the signal's channel and a threshold near the midpoint. This locks the waveform so it's stable and readable.

**6. Read the Waveform**

- **Amplitude** = peak-to-peak voltage
- **Frequency** = 1 / period (read from the time axis)
- **Shape** = tells you if a signal is clean (square, sine) or distorted/noisy

---

## Common Uses on a PCB

- Verify a **clock signal** is running at the right frequency
- Debug **UART / SPI / I2C** communication signals
- Check **PWM duty cycle** on motor or LED drivers
- Measure **power supply ripple** on a voltage rail
- Find **noise or glitches** causing resets or data errors
- Confirm **rise/fall times** of digital signals

---

## Tips

- Always connect **ground before signal**
- Use **10x probe attenuation** for most work (reduces probe loading)
- Use **AC coupling** to isolate ripple on a DC power rail
- Use **cursors** to measure exact time/voltage differences

---

**References:**

- [How to Use an Oscilloscope — SparkFun](https://learn.sparkfun.com/tutorials/how-to-use-an-oscilloscope/all)
- [Oscilloscope Basics — Tektronix](https://www.tek.com/en/documents/primer/oscilloscope-primer)
- [Using an Oscilloscope on a PCB — Adafruit Learning](https://learn.adafruit.com/using-an-oscilloscope)
