---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Asynchronous vs Synchronous Efficiency Comparison
translated: false
type: note
---

Question: For data links with the same transmission rate, when using asynchronous protocol or synchronous protocol to control large-volume data transmission, what is the transmission efficiency ratio (asynchronous protocol / synchronous protocol)?

A. Close to 80%
B. Close to 1
C. Close to 50%
D. Equal to 1

Answer:

**A**

**Explanation:**

In serial data communication:

- **Asynchronous protocol** (most commonly referring to UART-style asynchronous serial communication):
  Each character/byte is independently framed with **1 start bit + 8 data bits + 1 stop bit** (most common format is 8N1).
  → Total bits per byte = 10 bits
  → Efficiency = 8 / 10 = **80%**

- **Synchronous protocol** (e.g. HDLC, SDLC, synchronous serial protocols, or modern high-speed synchronous links):
  Usually transmits data in blocks/frames with only a small amount of overhead for frame synchronization, flags, headers, CRC/checksum, etc.
  When transmitting **large volumes of data**, the overhead per byte becomes very small (often <1–5%).
  → Efficiency is typically **very close to 100%** (or 95%+ for practical large-block transfers)

Therefore, for **large-batch / bulk data transmission**, the efficiency ratio is:

Asynchronous efficiency / Synchronous efficiency ≈ 80% / ~100% ≈ **80%**

Hence the correct answer is **A. close to 80%**.

**Why not the other options?**

- **B. close to 1** → This would be true only if both protocols had similar overhead, which is not the case for large data volumes.
- **C. close to 50%** → This is too pessimistic; even asynchronous UART is 80%, not 50%.
- **D. equal to 1** → Clearly incorrect due to the fixed start/stop bit overhead in asynchronous mode.

**Memory tip** (as given in the explanation):
"异步低效八成满，同步高效更划算"
→ Asynchronous is about 80% full (efficient), synchronous is more cost-effective (higher efficiency).

References:

- None (standard data communication theory)
