---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Symbol Rate Unit Explained
translated: false
type: note
---

Question: What is the unit of symbol rate (also known as baud rate or symbol transmission rate)?

Answer:

The correct answer is **B. Baud**.

**Explanation in English:**

- **Symbol rate** (also called **baud rate**, **symbol transmission rate**, or **modulation rate**) measures how many **symbols** (distinct signal elements) are transmitted per second.
- One symbol can represent one or more bits, depending on the modulation scheme (e.g., in BPSK 1 symbol = 1 bit, in 16-QAM 1 symbol = 4 bits).
- The **standard unit** for symbol rate is **Baud** (written as **Bd** or simply called "baud").

Common units and their meanings:

- **Bit/s** (bps) → bit rate = number of bits transmitted per second
- **Baud** → symbol rate = number of symbols transmitted per second
- **Byte** → 8 bits (not a rate unit)
- **Word** → usually 16 or 32 bits depending on system (not a rate unit)

Key relationship:

```
Bit rate (bps) = Symbol rate (baud) × bits per symbol (log₂M)
```

Examples:

- BPSK: 1 bit per symbol → bit rate = baud rate
- QPSK: 2 bits per symbol → bit rate = 2 × baud rate
- 16-QAM: 4 bits per symbol → bit rate = 4 × baud rate

So the **direct unit of symbol rate (码元速率)** is **Baud**, not bit, byte, or word.

Therefore the correct choice is **B. Baud**.

References:

- None needed for this standard communication theory concept.
