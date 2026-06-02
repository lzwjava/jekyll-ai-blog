---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: IEEE 802.3 SFD Sequence Explained
translated: false
type: note
---

Question: In the IEEE 802.3 standard, what is the Start Frame Delimiter (SFD) field sequence in the MAC frame?

A. 10101011 (left=LSB, right=MSB)
B. 11010101 (left=LSB, right=MSB)
C. 01111110 (left=LSB, right=MSB)
D. 01111111 (left=LSB, right=MSB)

Answer:

The correct answer is **A. 10101011** (read from left to right as LSB to MSB).

**Detailed explanation:**

In IEEE 802.3 (Ethernet), the frame structure includes:

- **Preamble**: 7 bytes of 10101010 … 10101010
- **Start Frame Delimiter (SFD)**: 1 byte = **10101011**

This makes the complete 8-byte synchronization sequence:
10101010 10101010 10101010 10101010 10101010 10101010 10101010 **10101011**

The purpose of changing the last byte from 10101010 to 10101011 is to provide a clear, unambiguous indication that the frame data is about to start (breaking the repeating 1010 pattern).

Key points:

- IEEE 802.3 uses **10101011** as SFD.
- This differs from Ethernet V2 (DIX Ethernet), which also uses 10101011 but has an 8-byte preamble of all 10101010.
- The choice of 10101011 in IEEE 802.3 was also made to improve compatibility/distinguishability with IEEE 802.4 (Token Bus) and IEEE 802.5 (Token Ring) frame formats.

Your choice was B (11010101), which is incorrect.
11010101 is not used as the SFD in IEEE 802.3 Ethernet.

Correct answer: **A**

References:

- IEEE 802.3 standard (Clause 4 - MAC frame format)
- [https://standards.ieee.org/ieee/802.3/2022/](https://standards.ieee.org/ieee/802.3/) (official IEEE 802.3 standard documentation)
