---
audio: false
generated: true
image: false
lang: en
layout: post
title: Digital Data Encoding Basics
translated: false
type: note
---

Question: What is digital data encoding?

Answer: **Digital data encoding** (数字数据编码) refers to the process of converting digital data (binary 0s and 1s) into physical signals (either digital voltage pulses or analog waveforms) so that the information can be transmitted over a communication medium or stored on hardware.

---

### Common Encoding Schemes

1. **Digital Data to Digital Signals (Baseband Transmission)**
* **Non-Return-to-Zero (NRZ):** Binary 1s and 0s are directly represented by two different voltage levels (e.g., high and low voltage). Simple, but lacks self-synchronization.
* **Manchester Encoding:** Represents binary data using voltage transitions in the middle of each bit period. A low-to-high transition represents one binary state, and high-to-low represents the other. Used in Ethernet (IEEE 802.3).
* **Differential Manchester Encoding:** Inversion at the start of a bit interval represents 0, while no inversion represents 1. Provides strong synchronization and noise resistance.


2. **Digital Data to Analog Signals (Modulation)**
* **Amplitude Shift Keying (ASK):** Binary values are represented by different amplitudes of a carrier signal wave.
* **Frequency Shift Keying (FSK):** Binary values are represented by shifting between two different carrier frequencies.
* **Phase Shift Keying (PSK):** Binary values are represented by shifting the phase of the carrier wave.



---

### Why Encoding Matters

* **Synchronization:** Allows receiver clocks to align with sender clocks using signal transitions.
* **Noise Immunity:** Enhances resistance to signal degradation and interference over long distances.
* **Bandwidth Efficiency:** Optimizes the spectrum utilization over physical media like copper wire, optical fiber, or radio waves.
