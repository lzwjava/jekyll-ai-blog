---
audio: false
generated: true
image: false
lang: en
layout: post
title: CRC Zero Append Rule Explained
translated: false
type: note
---

Question: When using CRC校验 (Cyclic Redundancy Check) with a generator polynomial bit string of 11001, how many zeros must be appended to the end of the information bit string before performing polynomial division over GF(2) to calculate the CRC redundancy bits?

Answer:

The correct answer is **C (4)**.

### Explanation

1. **Understand the Generator Polynomial**:
    The problem states that the bit string corresponding to the generator polynomial is `11001`.
    - In binary representation, this corresponds to the polynomial coefficients from the highest degree to the lowest ($x^4, x^3, x^2, x^1, x^0$).
    - Therefore, the polynomial is $G(x) = 1\cdot x^4 + 1\cdot x^3 + 0\cdot x^2 + 0\cdot x^1 + 1\cdot x^0 = x^4 + x^3 + 1$.

2. **Determine the Degree of the Polynomial**:
    - The highest power of $x$ in $G(x)$ is 4.
    - Alternatively, you can determine the degree by counting the number of bits in the generator string and subtracting 1.
    - Length of `11001` = 5 bits.
    - Degree ($r$) = $5 - 1 = 4$.

3. **CRC Calculation Rule**:
    - To calculate the CRC redundancy bits (also known as the Frame Check Sequence or FCS), you must append $r$ zeros to the original message (information bits), where $r$ is the degree of the generator polynomial.
    - Since the degree is 4, you must append **4** zeros to the information bit string before performing the modulo-2 division.

4. **Why Option B is Incorrect**:
    - Option B suggests adding 3 zeros. This would be correct if the generator polynomial had a degree of 3 (e.g., a 4-bit string like `1101`). However, since the string `11001` has 5 bits, the degree is 4, requiring 4 zeros.

**Conclusion**:
Since the generator polynomial `11001` has a degree of 4, **4** zeros must be appended to the information bits.
