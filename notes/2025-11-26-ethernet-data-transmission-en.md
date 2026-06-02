---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: How Ethernet Transmits Data Electrically
translated: false
type: note
---

Here's how Ethernet actually "talks" over twisted-pair copper cables (like Cat5e, Cat6, etc.) and turns electricity into digital bits:

### 1. Basic idea: Voltage changes represent 1s and 0s
Ethernet sends data by changing the voltage on the copper wires.
Different voltage levels or transitions mean different bits.

### 2. Twisted-pair wiring in Ethernet (e.g., Cat5e/Cat6)
A typical Ethernet cable has 4 twisted pairs (8 wires).
For most modern Ethernet (100 Mbps and faster), only 2 or all 4 pairs are used bidirectionally.

### 3. How electrical signals become bits (by speed)

#### 10BASE-T and 100BASE-TX (old, but easy to understand)
- Uses Manchester encoding (10 Mbps) or 4B5B + MLT-3 encoding (100 Mbps).
- A transition in voltage = clock + data.
- Positive/negative voltage or transitions represent 1 or 0.
- Simple: you literally see voltage jumping up and down on the wire carrying the digital information.

#### 1000BASE-T (Gigabit Ethernet over copper) – this is where it gets clever
- Uses all 4 pairs simultaneously, in both directions at once.
- Employs PAM-5 encoding (5 voltage levels: –2, –1, 0, +1, +2 volts).
- Each pair sends 125 million symbols per second.
- 2 bits per symbol → 250 Mbps per pair × 4 pairs = 1000 Mbps.
- Echo cancellation and DSP (digital signal processing) in the Ethernet PHY chip subtract the transmitted signal from what is received on the same pair so it can hear the far end talking at the same time (full duplex on the same pair!).

#### 2.5GBASE-T, 5GBASE-T, 10GBASE-T (modern high-speed Ethernet)
- Uses PAM-16 (16 voltage levels) + LDPC error correction.
- Even more dense packing of bits into small voltage steps.
- Extremely sophisticated DSP to remove noise, echo, crosstalk between pairs, etc.

### 4. What actually happens inside the hardware (the PHY chip)
Your network card or switch has a PHY (Physical Layer) chip that does this:

1. MAC (Layer 2) gives it a stream of bits (frames).
2. The PHY encodes those bits into analog voltage waveforms using the rules above (PAM-5, PAM-16, etc.).
3. A DAC (digital-to-analog converter) turns numbers into precise voltages sent onto the twisted pair.
4. A strong line driver pushes ±2.5 V or so into the cable (through a transformer for galvanic isolation).
5. At the receiving end:
   - Transformer → analog front-end → high-speed ADC (samples the voltage hundreds of millions of times per second)
   - DSP cleans up noise, removes echo of its own transmission, equalizes the signal (because high frequencies weaken over long cables)
   - Decoder turns the cleaned-up voltage levels back into clean digital 1s and 0s.

### 5. Why twisted pair works so well
- Twisting cancels electromagnetic interference (noise).
- Differential signaling: each pair carries +V and –V. The receiver only looks at the difference (common-mode noise is rejected).
- Magnetics (transformers) at both ends isolate and protect against ground differences and surges.

### Summary in simple words
Electricity itself doesn't become bits.
The Ethernet PHY deliberately changes the voltage on the copper wires in very specific patterns and levels.
The receiver constantly measures that voltage, and through encoding rules + heavy math (DSP), it figures out exactly which bits you sent.

So:
Digital bits → encoding → precise voltage levels/timings → sent over copper → received → sampled → DSP magic → clean digital bits again.

That’s how 10 billion bits per second can fly reliably over ordinary copper twisted-pair cables you buy for a few dollars.
