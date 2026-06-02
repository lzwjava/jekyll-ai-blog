---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Gray Code Fundamentals and Applications
translated: false
type: note
---

### What is Gray Code?

Gray code (also known as reflected binary code) is a binary numeral system designed such that **two consecutive (or adjacent) values differ by exactly one bit**. This property minimizes errors during transitions, as only a single bit needs to change when moving from one number to the next. It's particularly useful in applications like:
- **Rotary encoders** (e.g., in mechanical devices like knobs or wheels, where position changes gradually).
- **Error detection/correction** in digital communications.
- **Karnaugh maps** in digital logic design for simplifying Boolean algebra.

Unlike standard binary code, where adjacent numbers can differ in multiple bits (causing potential "glitches" or errors), Gray code ensures smooth, single-bit transitions.

### How Gray Code Works
The key rule is: **Any two successive codes differ in only one bit position**.

#### Simple Example: 2-Bit Gray Code Sequence (for numbers 0 to 3)
Here's a comparison of standard binary and Gray code:

| Decimal | Standard Binary | Gray Code | Bit Difference from Previous |
|---------|-----------------|-----------|------------------------------|
| 0       | 00              | 00        | (Starting point)             |
| 1       | 01              | 01        | 1 bit (least significant)    |
| 2       | 10              | 11        | 1 bit (least significant)    |
| 3       | 11              | 10        | 1 bit (most significant)     |

- In **standard binary**, the transition from 1 (01) to 2 (10) flips *two* bits, which could cause errors.
- In **Gray code**, every step flips *exactly one* bit, matching your description of "two continuous code only one is different."

#### Generating Gray Code
You can convert binary to Gray code using a simple XOR operation:
- Gray(n) = n XOR (n >> 1)  (where >> is right-shift by 1 bit).

For example:
- Binary 2 (10 in decimal): 10 XOR 01 = 11 (Gray code for 2).
- To go back: Binary(n) = Gray(n) XOR (Gray(n) >> 1).

This pattern can extend to any number of bits (e.g., 3-bit, 4-bit, etc.), always maintaining the single-bit difference property.

If you have a specific use case or want examples for more bits, let me know!
