---
audio: false
generated: true
lang: en
layout: post
title: Shannon's Capacity Formula
translated: false
type: note
---

Shannon's capacity formula is actually written as:

C = B log₂(1 + S/N)

Where:
- C is the channel capacity in bits per second
- B is the bandwidth in Hertz
- S/N is the signal-to-noise ratio (power ratio)
- log₂ is the logarithm with base 2

This formula represents the theoretical maximum data rate that can be reliably transmitted over a communications channel with bandwidth B and a signal-to-noise ratio of S/N.

To understand why this is correct:

1. **Bandwidth factor (B)**: The bandwidth directly scales the capacity - doubling the bandwidth doubles the capacity.

2. **Logarithmic relationship**: The log₂ shows that capacity increases logarithmically with S/N, not linearly. This means:
   - Doubling S/N doesn't double capacity
   - Each additional "bit" of capacity requires doubling the S/N

3. **1 + S/N term**: The addition of 1 ensures that capacity is always positive, even with very small S/N values.

This formula is fundamental to information theory because it establishes the theoretical upper limit for how much information can be transmitted through a noisy channel, regardless of the coding scheme used.

Would you like me to explain any particular aspect of this formula in more detail?
