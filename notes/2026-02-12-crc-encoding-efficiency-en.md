---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: CRC Encoding Efficiency Explained
translated: false
type: note
---

Question: In cyclic redundancy check (CRC), if the codeword has k information bits and r redundancy bits are added during encoding, what is the encoding efficiency?

Answer:

The correct answer is **D. k/(k+r)**.

**Explanation:**

Encoding efficiency (also called code rate or information rate) measures how much of the total transmitted bits actually carry useful information.

- Information bits (payload): **k** bits
- Redundancy bits (check bits, parity bits): **r** bits
- Total codeword length: **k + r** bits

Therefore, the encoding efficiency is defined as:

**Efficiency = (number of information bits) / (total number of bits in the codeword) = k / (k + r)**

This matches option **D**.

**Quick memory tip (as provided):**
"信息位k，总长k+r，效率k/(k+r)"

**Why the other options are incorrect:**

- A. r/(r+k) → This would be the redundancy ratio, not the efficiency.
- B. 1/(k+r) → This has no meaningful interpretation in this context.
- C. r/k → This is the relative redundancy, opposite of efficiency.

So the correct choice is indeed **D**.

References:

- None (standard coding theory definition, no external reference required)
