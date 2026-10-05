---
audio: false
generated: true
image: false
lang: en
layout: post
title: Analog Signal Explained
translated: false
type: note
---

**Question: What is 模拟信号 (analog signal)?**

**Answer:**

A **模拟信号 (analog signal)** is a signal whose value changes **continuously over time**. It represents information by changing a physical quantity such as **voltage, current, sound pressure, or electromagnetic wave amplitude**.

Mathematically, an analog signal can be represented as:

$$
x(t)
$$

where:

* \\(t\\) = continuous time
* \\(x(t)\\) = signal value, which can take any value within a range

Example:

```
Voltage

5V       /‾‾\      /‾‾\
        /    \    /
0V ____/      \__/______ time
```

The voltage changes smoothly. At any moment, it could be:

* 1.234V
* 2.567V
* 3.891V

There are infinitely many possible values.

### Common examples of analog signals

**1. Human voice**

Your voice creates air pressure waves:

```
Sound wave:

     /\      /\
    /  \    /  \
___/    \__/    \___
```

A microphone converts this continuous air vibration into a continuously changing electrical voltage.

**2. Radio broadcasting**

Traditional AM/FM radio uses analog electromagnetic waves. The information is encoded by changing:

* amplitude (AM: Amplitude Modulation)
* frequency (FM: Frequency Modulation)

**3. Old telephone systems**

Old landline phones transmitted voice as analog electrical signals.

---

### Analog vs Digital signal

|                  | Analog               | Digital     |
| ---------------- | -------------------- | ----------- |
| Value            | Continuous           | Discrete    |
| Example          | 2.345V, 2.346V, etc. | 0 or 1      |
| Waveform         | Smooth               | Square-like |
| Noise resistance | Lower                | Higher      |
| Storage          | Harder               | Easier      |

Example:

Analog:

```
~~~~~~~ continuous wave ~~~~~~~
```

Digital:

```
___|‾‾‾|___|‾‾‾|___
 0   1   0   1
```

---

Modern systems often convert analog signals into digital signals:

```
Real world
(sound/light/temperature)
        |
        v
 Analog signal
        |
        v
 ADC (Analog-to-Digital Converter)
        |
        v
 Digital data
        |
        v
 Computer processing
```

For example, a smartphone microphone:

1. Air vibration → analog sound wave
2. Microphone → analog electrical signal
3. ADC → digital samples (44.1 kHz, 48 kHz, etc.)
4. Phone processes the data

So the key idea:

**Analog signal = information carried by a continuously varying physical signal. Digital signal = information represented by discrete values (usually bits 0 and 1).**

I can also explain how **ADC sampling converts an analog wave into digital data (Nyquist theorem)** if useful.
