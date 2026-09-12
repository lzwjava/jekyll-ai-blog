---
audio: false
generated: true
image: false
lang: en
layout: post
title: Folded Binary Code Explained
translated: false
type: note
---

Question: What is folded binary code (折叠二进制码)?

Answer:

Folded binary code (also called **reflected binary** in some contexts, but specifically "folded binary" refers to a distinct concept) is a type of binary encoding used primarily in **analog-to-digital converters (ADCs)** and **communication systems**.

## Key Characteristics

**Basic idea:** In folded binary, the numerical sequence "folds back" on itself at the midpoint, creating a mirrored/symmetric pattern rather than counting straight up like standard binary.

**Example comparison (3-bit):**

| Decimal | Standard Binary | Folded Binary |
|---------|----------------|---------------|
| 0 | 000 | 000 |
| 1 | 001 | 001 |
| 2 | 010 | 010 |
| 3 | 011 | 011 |
| 4 | 100 | 011 ← folds back |
| 5 | 101 | 010 |
| 6 | 110 | 001 |
| 7 | 111 | 000 |

The code counts up to the midpoint, then **counts back down** — like a folded mirror.

## Where It's Used

- **Flash ADCs / Folding ADCs** — reduces the number of comparators needed by exploiting the folded symmetry of the input signal
- **Signal processing** — simplifies certain arithmetic operations by taking advantage of the symmetric structure
- **Error-resilient encoding** — adjacent values differ by minimal bit changes near the fold point

## Relationship to Other Codes

It is related to but distinct from:
- **Gray code** — also minimizes bit transitions, but uses a different reflection pattern
- **Two's complement** — standard signed binary, no folding
- **Offset binary** — used in ADCs but counts linearly

The "folding" concept is especially powerful in **folding-and-interpolating ADCs**, where the analog signal itself is folded before quantization, allowing high-speed, lower-power conversion.

References:
- [Folding ADC – Wikipedia](https://en.wikipedia.org/wiki/Folding_ADC)
- [Binary code types overview – All About Circuits](https://www.allaboutcircuits.com/textbook/digital/chpt-13/binary-codes/)
