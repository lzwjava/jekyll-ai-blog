---
audio: false
generated: true
image: false
lang: en
layout: post
title: Baud Rate vs Bit Rate Explained
translated: false
type: note
---

Question: What is the definition and significance of "baud" in networking?

Answer: In networking and telecommunications, **baud** (or baud rate) refers to the number of **signal units** or "symbols" transmitted per second. While often confused with bit rate, it specifically measures the rate of change in an electrical or optical signal rather than the total amount of raw data moving through the line.

### Understanding the Difference: Baud vs. Bit Rate

To understand baud, you have to distinguish between the "container" (the symbol) and the "content" (the bits).

* **Baud Rate:** The number of times the signal state changes per second (pulses, voltage shifts, or phase changes).
* **Bit Rate:** The actual number of 1s and 0s transmitted per second.

### The Relationship Formula

The relationship between these two is determined by the complexity of the modulation. If a single signal change (one baud) carries more than one bit of data, the bit rate will be higher than the baud rate. This is expressed by the formula:

$$\text{Bit Rate} = \text{Baud Rate} \times \text{Bits per Symbol}$$

### Key Characteristics

* **Efficiency:** Modern modems use advanced modulation (like QAM) to pack many bits into a single symbol. For example, if a system uses 16-QAM, each "symbol" represents 4 bits. If the baud rate is 1,000, the bit rate is 4,000 bps.
* **Physical Limits:** High baud rates are harder to maintain over long distances because rapid signal changes are more susceptible to noise and distortion.
* **Origin:** The term is named after **Émile Baudot**, the inventor of the Baudot code for telegraphy.

---

Would you like me to explain the specific modulation techniques, such as QAM or PSK, that allow us to fit more bits into a single baud?