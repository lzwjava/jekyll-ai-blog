---
audio: false
generated: true
image: false
lang: en
layout: post
title: Networking Noise Explained
translated: false
type: note
---

Question: What is "噪声" (noise) in networking?

Answer: In networking, noise is any unwanted signal or interference that distorts or corrupts the data signal as it travels through a transmission medium. It makes it harder for the receiver to correctly interpret the original information, which can cause bit errors, retransmissions, and lower throughput.

**Common types of noise:**
- **Thermal noise (Johnson-Nyquist noise):** Caused by random motion of electrons in conductors and electronic components. It is always present and sets a baseline noise floor.
- **Crosstalk:** Signal leakage between adjacent wires or cables (e.g., in twisted pair). Near-end crosstalk (NEXT) and far-end crosstalk (FEXT) are the usual variants.
- **Electromagnetic interference (EMI) / radio-frequency interference (RFI):** Interference from motors, fluorescent lights, power lines, microwave ovens, and other wireless devices.
- **Impulse noise:** Short, high-amplitude spikes, often from lightning, power surges, or switching equipment. It tends to corrupt bursts of bits.
- **Intermodulation noise:** Created when multiple signals share a medium and interact, producing unwanted frequency components.
- **Attenuation-related and environmental noise:** Weak signals over long distances are more easily swamped by noise; in wireless, other transmitters on the same channel add interference.

**How it's measured:**
- **Signal-to-Noise Ratio (SNR):** The ratio of signal power to noise power, usually in decibels (dB). A higher SNR means a cleaner signal.
- **Shannon's capacity theorem:** C = B · log₂(1 + SNR), where C is the maximum channel capacity, B is bandwidth. It shows that more noise reduces the maximum achievable data rate.

**How it's reduced:**
- Shielded cables (STP, coax) and proper grounding
- Twisted-pair wiring, which cancels out common interference
- Fiber optic cabling, which is immune to EMI
- Error detection and correction (CRC, parity, FEC)
- Filtering, amplification/repeaters, and choosing less congested wireless channels

References:
- [Signal-to-noise ratio – Wikipedia](https://en.wikipedia.org/wiki/Signal-to-noise_ratio)
- [Noise (electronics) – Wikipedia](https://en.wikipedia.org/wiki/Noise_(electronics))
- [Shannon–Hartley theorem – Wikipedia](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem)
