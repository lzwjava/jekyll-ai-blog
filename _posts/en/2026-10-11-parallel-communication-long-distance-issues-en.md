---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parallel Communication Long Distance Issues
translated: false
type: note
---

**Question:** Why is parallel communication unsuitable for long-distance communication in computer networking?

---

**Answer:**

Parallel communication sends multiple bits simultaneously over multiple wires. While this seems faster, several physical problems make it impractical over long distances:

**1. Skew (Timing Mismatch)**
This is the most critical issue. Bits sent together at the source arrive at *different times* at the destination because each wire has slightly different electrical characteristics (capacitance, resistance, inductance). Over short distances, this difference is negligible — but over long distances, the skew grows large enough to cause data corruption. The receiver can no longer tell which bits "belong together."

**2. Signal Attenuation**
All electrical signals weaken (attenuate) over distance. In parallel communication, each of the multiple wires degrades independently and at different rates, making it increasingly difficult to maintain consistent signal strength across all channels simultaneously.

**3. Crosstalk / Electromagnetic Interference (EMI)**
Multiple wires running in parallel over long distances act as antennas, inducing interference *into each other* (crosstalk) and picking up external EMI. This corrupts data on individual lines, and the problem worsens with distance.

**4. High Infrastructure Cost**
A parallel bus requires many physical wires (e.g., 8, 16, or 32). Deploying dozens of cables over long distances is far more expensive than a single serial line — with no real performance benefit due to the problems above.

**5. Clock Synchronization Difficulty**
Parallel communication is typically synchronous — all bits must be clocked in together. Distributing a reliable, precise clock signal across long distances is technically very difficult and expensive to maintain.

---

**Why Serial Communication Wins for Long Distance**

Serial communication sends bits *one at a time* over a single wire. It avoids skew entirely, suffers from only one signal path's attenuation, and is far cheaper to deploy. Modern high-speed serial protocols (like USB, PCIe, Ethernet, and fiber optics) use sophisticated encoding and error correction to achieve speeds far beyond what parallel buses ever could at long range.

> **In short:** Parallel = fast in theory, impractical in reality for distance. Serial = simpler, more reliable, scalable.

---

**References:**

- [Serial vs. Parallel Communication – All About Circuits](https://www.allaboutcircuits.com/technical-articles/serial-vs-parallel-transmission/)
- [Signal Integrity and Skew in Digital Systems – Texas Instruments](https://www.ti.com/lit/an/szza036/szza036.pdf)
- [Data Transmission – Parallel vs. Serial – Cisco Networking Academy](https://www.netacad.com/)
