---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nyquist Formula Calculates 24 Kbps
translated: false
type: note
---

Question: According to the Nyquist formula, if the channel bandwidth H = 3 KHz and each signal symbol can take N = 16 discrete values, what is the maximum data transmission rate of the channel?

Answer:

The Nyquist formula determines the maximum data transmission rate in a noiseless channel. Here's the solution:

**Given Information:**
- Channel bandwidth (H) = 3 KHz
- Number of discrete signal levels (N) = 16

**Solution Process:**

According to the Nyquist theorem, the maximum symbol rate (baud rate) in a noiseless channel is:

**Maximum symbol rate = 2 × H**

Therefore:
- Maximum symbol rate = 2 × 3 KHz = 6 kilobaud (symbols per second)

The relationship between data transmission rate and symbol rate is:

**Data transmission rate = Symbol rate × log₂(N)**

Where log₂(N) represents the number of bits per symbol.

Since N = 16:
- log₂(16) = 4 bits per symbol

Therefore:
**Maximum data transmission rate = 6 × 4 = 24 kbps**

**Explanation:**

The Nyquist theorem establishes that the maximum symbol rate is twice the bandwidth. With 16 possible discrete values per symbol, each symbol can encode log₂(16) = 4 bits of information. Multiplying the maximum symbol rate by the bits per symbol gives us the maximum data transmission rate.

**Correct Answer: B (24 Kbps)**

Your answer of C (48 Kbps) appears to have multiplied the bandwidth by 16 directly without properly applying the Nyquist theorem's 2× factor, or incorrectly calculated log₂(16) as 8 instead of 4.