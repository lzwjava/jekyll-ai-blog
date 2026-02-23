---
audio: false
generated: true
image: false
lang: en
layout: post
title: PAM Bits per Symbol Calculation
translated: false
type: note
---

Question: In a Phase-Amplitude Modulation (PAM) system using 8 phases and 2 amplitude values per phase, how many binary bits can a single signal symbol represent?

Answer: 

### Analysis and Calculation

To determine the number of binary bits a single signal symbol (baud) can represent, we need to calculate the total number of distinct states available in the modulation scheme.

1.  **Identify the parameters:**
    *   Number of phases ($N_{phase}$) = 8
    *   Number of amplitude values per phase ($N_{amp}$) = 2

2.  **Calculate the total number of distinct states ($M$):**
    The total number of unique combinations is the product of the number of phases and the number of amplitudes.
    $$M = N_{phase} \times N_{amp}$$
    $$M = 8 \times 2 = 16$$
    There are 16 distinct signal states.

3.  **Calculate the number of bits per symbol ($n$):**
    The number of bits represented by one symbol is the base-2 logarithm of the total number of states.
    $$n = \log_2(M)$$
    $$n = \log_2(16)$$
    Since $2^4 = 16$:
    $$n = 4$$

### Conclusion

Each signal symbol can represent **4** binary bits.

Therefore, the correct option is **C**.