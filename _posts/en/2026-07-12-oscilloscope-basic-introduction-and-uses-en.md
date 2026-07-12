---
audio: false
generated: true
image: false
lang: en
layout: post
title: Oscilloscope Basic Introduction and Uses
translated: false
type: note
---

Question: What is 示波器 (oscilloscope)?

Answer:

![Image](https://images.openai.com/static-rsc-4/LEfBgCBVsu0-UxUIFjJ59WV6tneLZN5qfv73bw6kYydr5WWwd2IWTPkJUQ8QItkVInEGPetL6QYmp_rhTqABef3FJx1CxAlA_PrPE2bTxC6p_b5sxazc0Kq24UTYV_lfrOrWWXfRWe2x2BbCiLQfL_Nmd41pmqlQO_5SNLTjw5aa0bsD_xOpnTIHAks8HNB9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/cJM-1UTRcdv2Z_4mFWaLox2N2ywUB2S6JOeed1VNHM5J-Sg6_5uUzdzy4YxKSmj8sk5cX94a-G6YYuxXeUO-_PUXdMFl2IhEaPm0DunYHBbXT3A8XbLpXsp35pkrDBWD_yM1ULo3jsWg6rDKaYWALN2-xz8f79Zd8Ssa8YTZxSoI5KzqQ5F3u-7hPCvYZfIm?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/KS0Do3WMB3szi4J3DDcindSUHQbTRQjrOgPj0_JCSHyD0KJMA1UfpDUdPcN3ORZP_7ZChPLGVNCzKer3B5Ji6goHp_5_uOoX4LIFHtSEs8WJIeH3vN-eIDTleYktEOlu7F0VTY9qwMi8s2mbk8Edkko4EeerHokmVJSZN6j1baL5yhD-E6SBiTaIVSgAMRe4?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GwDXX3tH9GJDzrIdZZxyrQPlSH4imz2sJz2HIdaWl5vWSLDle6qR88iNIJsryRhp_uZXkcJBdzakAHuZ42Lwmat8S0aWc22dMe1PGic7GbVoo9tKTCfOTfV6Sfgx-W65R83tVCavvnmFe8Zn2ltw8ahRiCNVAhaTkdXhV8hZqwbNwqelF0h86qOEmrBnYiV2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/T8dZE8IodlkYQISYr1guzz76609gJ3BRvekuL4WtTKZlmV8uWWE_G8ITQcu11uLoMpiNV47Z2aISiwipGLZR-Ucb1NGM7qjoYDRbV_5OaJPKP8qpiGVRjYqMQdqr05xRN1dlfmK0a62DouCtZunfq7Bwrh1lUO9_q1JR7KMKg4nQE7TCA-EJwmo_W8hkfRnf?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NiDqOwf64CJO4DHk2vep6vsbM36a4kG5l1zQfhasc-V3CxNR_9awphYbU9sss7tqPgBRXvnawxD5AY_4_J38VF1MvwzNNO77RtuL_epFuuTtRExA4sFK2gFBnGHjLjWV-1JcZgtJ7bmeDrUOzGOsZALQNe1ymVIawwT0LwL0YUToplnLsqb6y6_KHWgBIn-_?purpose=fullsize)

A **示波器 (shìbōqì)** is an **oscilloscope**. It is a laboratory instrument that lets you **see electrical signals as waveforms over time**.

A multimeter tells you a single number:

```
Voltage = 3.3V
Current = 0.5A
Resistance = 10Ω
```

An oscilloscope shows the **shape of the signal**:

```
Voltage
  |
5V|       ┌───┐     ┌───┐
  |       │   │     │   │
0V|───────┘   └─────┘   └──── Time
```

You can see:

* voltage changes
* frequency
* noise
* glitches
* timing problems
* communication signals

---

## Basic working principle

An oscilloscope has:

```
Circuit signal
      |
      v
 Oscilloscope probe
      |
      v
 ADC (analog → digital)
      |
      v
 Memory buffer
      |
      v
 Display waveform
```

Modern oscilloscopes are basically:

```
high-speed ADC + computer + display
```

The key specs:

### 1. Bandwidth

How fast a signal it can measure.

Example:

* 20 MHz oscilloscope → good for Arduino/simple electronics
* 100 MHz → common hobby/professional entry
* 1 GHz+ → high-speed CPUs, PCIe, DDR signals

A 100 MHz scope cannot accurately see a 500 MHz signal.

---

### 2. Sampling rate

How many measurements per second.

Example:

```
1 GS/s = 1 billion samples per second
```

For a 100 MHz signal, you need several samples per cycle.

---

### 3. Channels

How many signals simultaneously:

* 1 channel: observe one signal
* 2 channels: compare clock vs data
* 4 channels: debug complex systems

---

## Common use cases

### Arduino / ESP32 debugging

Example:

ESP32 sends PWM:

```
GPIO pin

0V  ____      ____
       |____|
       1ms  1ms
```

Oscilloscope shows:

* Is PWM frequency correct?
* Is duty cycle correct?
* Is there noise?

---

### Debugging power problems

Your board randomly resets.

Multimeter:

```
3.3V
```

Looks normal.

Oscilloscope:

```
3.3V ──────────
          |
          ↓
       1.8V spike
```

You discover a power drop lasting 20 microseconds.

---

### Serial communication

UART:

```
TX:

101101001011
```

Oscilloscope can show:

* baud rate
* signal integrity
* voltage levels

For SPI:

```
CLK  ─+-+-+-+-+
MOSI ─01011010
```

---

### CPU/GPU hardware

Engineers use oscilloscopes for:

* DDR memory signals
* PCIe lanes
* USB signals
* VRM power delivery
* clock circuits

For example, debugging a GPU board:

```
12V PSU
 |
 VRM
 |
 GPU core voltage
```

A scope can see:

```
1.0V rail:

1.00V ─────────
       ↑
     ripple/noise
```

---

## Oscilloscope vs Logic Analyzer

They overlap but are different.

### Oscilloscope

Measures **analog reality**:

```
Voltage waveform

0V ----/\----/\----
```

Good for:

* power
* noise
* analog circuits
* signal quality

### Logic analyzer

Only sees digital 0/1:

```
0 1 1 0 1 0
```

Good for:

* protocols
* UART
* SPI
* I2C

Cheap logic analyzer:

```
$10 USB logic analyzer
```

Cheap oscilloscope:

```
$200-500
```

---

## For your AI + hardware experiments

Given you are playing with:

* ESP32
* GPUs
* custom hardware
* servers

A scope becomes useful when you move from:

```
software debugging
        |
        v
firmware debugging
        |
        v
electrical debugging
```

Example:

ESP32 + sensor:

```
Python code ❌
Firmware ❌
GPIO voltage?
Signal timing?
Power noise?
```

The oscilloscope answers the last questions.

A reasonable beginner/prototyping scope:

* 100 MHz bandwidth
* 1 GS/s sampling
* 2 channels

Examples:

* Rigol DS1054Z
* Siglent Technologies SDS1104X-E

The mindset is similar to using `gdb` for software:
**a debugger lets you see program state; an oscilloscope lets you see electrical state.**
