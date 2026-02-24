---
audio: false
generated: true
image: false
lang: en
layout: post
title: RS-232C Logic 1 Voltage Explained
translated: false
type: note
---

Question: What is the voltage level for logic "1" in the RS-232C electrical specification?

Answer:

## RS-232C Logic "1" Voltage Level — Correct Answer: **D (-15V ~ -5V)**

---

### Key Electrical Characteristics of RS-232C

RS-232C uses an **inverted (negative logic)** voltage scheme for data transmission lines, which is counterintuitive compared to most digital logic standards.

| State | Driver Output Voltage | Receiver Threshold |
|---|---|---|
| **Logic "1" (MARK)** | **-5V to -15V** | -3V to -15V |
| **Logic "0" (SPACE)** | **+5V to +15V** | +3V to +15V |
| **Undefined / Invalid** | -3V to +3V | — |

---

### Why the Answer is D, Not C

The question specifically asks about the **driver output** voltage requirement:

- Drivers must supply **-5V to -15V** for a logic 1, and **+5V to +15V** for a logic 0.
- Taking the 2V noise margin into account, a low level (-3V to -15V) is defined as a logic 1 (marking) at the **receiver** input.

So the distinction is:
- **Driver output** (what the transmitter sends): **-5V to -15V** → This is **Answer D**
- **Receiver threshold** (what is accepted as valid logic 1): -3V to -15V → This corresponds to Option C

Option C (-13V to -3V) describes the **receiver** detection range (with noise margin), not the driver output requirement. The exam answer **D (-15V ~ -5V)** refers to the **driver's required output voltage** to properly signal logic "1."

---

### Summary

> RS-232C uses **negative voltage for logic "1"** (called "MARK") and **positive voltage for logic "0"** (called "SPACE"). The driver must output between **-5V and -15V** to represent a valid logic "1". This is the opposite of standard TTL/CMOS logic.

References:

- [Fundamentals of RS-232 Serial Communications – Analog Devices](https://www.analog.com/en/resources/technical-articles/fundamentals-of-rs232-serial-communications.html)
- [RS-232 – Wikipedia](https://en.wikipedia.org/wiki/RS-232)
- [Understanding the RS-232 Standard – DigiKey](https://www.digikey.com/en/maker/blogs/2023/understanding-the-rs-232-standard)