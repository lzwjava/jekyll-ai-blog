---
audio: false
generated: true
image: false
lang: en
layout: post
title: Oscilloscope Displays Voltage versus Time
translated: false
type: note
---

Question: Why does an oscilloscope sometimes show a sine/cosine wave, and sometimes a triangle or square wave?

Answer:

Because the oscilloscope is simply plotting **voltage versus time**:

$$
y = V(t)
$$

The **shape you see is the actual time-domain waveform produced by the circuit/device**.

### 1. Sine wave

A sine wave comes from something oscillating smoothly:

$$
V(t)=A\sin(2\pi ft+\phi)
$$

For example, AC mains, a function generator, or an oscillator.

genui{"learning_viz":{"type_id":"RIGHT_TRIANGLE","locale_override":"en-US"}}

Conceptually:

```text
Voltage
  ^
 A|      /‾\       /‾\
  |     /   \     /   \
  |----/-----\---/-----\----> time
  |   /       \ /       \
-A|__/         V         \__
```

The voltage changes **continuously and smoothly**.

---

### 2. Triangle wave

A triangle-wave generator makes voltage increase approximately linearly, then decrease linearly:

```text
Voltage
  ^
  |      /\
  |     /  \
  |    /    \
  |   /      \
  |__/        \__
  +-----------------> time
```

Mathematically, it is basically a **linear ramp + linear ramp down**.

So the oscilloscope doesn't somehow "turn a sine wave into a triangle." The circuit is actually generating a triangle waveform.

---

### 3. Square wave

A digital circuit can switch between two voltage levels:

```text
Voltage
  ^
  | ┌──────┐      ┌──────┐
  | │      │      │      │
  | │      │      │      │
  |─┘      └──────┘      └──> time
  |
```

For example:

```text
LOW  = 0 V
HIGH = 3.3 V
```

A microcontroller GPIO producing:

```python
while True:
    GPIO = 1
    GPIO = 0
```

will ideally produce a square wave.

---

### 4. The important idea

Think of the oscilloscope as a **voltage camera over time**.

It measures:

```text
time ───────────────>
        |
        v
     voltage
```

So:

| Circuit output | Oscilloscope       |
| -------------- | ------------------ |
| sine           | smooth sine        |
| triangle       | triangular         |
| square         | rectangular        |
| sawtooth       | ramp + sudden drop |
| DC             | horizontal line    |
| noisy signal   | irregular waveform |

And this is why the oscilloscope is so useful for your GPU-repair work: **you can probe a power rail and see whether its voltage is actually behaving correctly**, rather than only measuring its average DC voltage with a multimeter.

For example, a GPU VRM might say `1.0 V` on a multimeter, while the oscilloscope reveals `1.0 V + 50 mV ripple at hundreds of kHz`. That ripple can be extremely important.

I can also walk through **how an oscilloscope physically samples the voltage and reconstructs these waveforms**, including ADC → sample buffer → trigger → display.
