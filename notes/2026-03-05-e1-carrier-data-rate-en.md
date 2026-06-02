---
audio: false
generated: true
image: false
lang: en
layout: post
title: E1 Carrier Data Rate Calculation
translated: false
type: note
---

Question: In the E1 carrier standard, one frame consists of 256 bits and is transmitted in 125 microseconds. What is the data transmission rate of the E1 carrier?

A. 1.544 Mbps
B. 2.048 Mbps
C. 3.045 Mbps
D. 4.025 Mbps

Answer:

**B. 2.048 Mbps**

**Calculation explanation:**

The transmission rate can be calculated using the formula:

Data rate = (number of bits per frame) ÷ (time per frame in seconds)

- Bits per frame = 256 bits
- Time per frame = 125 microseconds = 125 × 10⁻⁶ seconds = 0.000125 seconds

Data rate = 256 ÷ 0.000125 = 2,048,000 bits per second = **2.048 Mbps**

This matches the standard E1 rate.

**Additional context (why E1 is 2.048 Mbps):**

E1 uses synchronous time-division multiplexing and contains:

- 30 voice channels × 64 kbps = 1,920 kbps
- 2 signaling/control channels × 64 kbps = 128 kbps (usually implemented as 16 time slots of 8 bits each, but effectively 2 × 64 kbps)
- Plus 1 framing bit per frame

Total per frame: 32 time slots × 8 bits = 256 bits
Frames are sent 8,000 times per second (125 μs interval, matching 8 kHz sampling rate of PCM voice)

Therefore: 256 bits/frame × 8,000 frames/second = 2,048,000 bps = **2.048 Mbps**

This is the internationally standardized E1 rate (ITU-T G.703/G.704), different from the North American T1 rate of 1.544 Mbps.

References:

- None (standard telecommunications knowledge; calculation is deterministic)
