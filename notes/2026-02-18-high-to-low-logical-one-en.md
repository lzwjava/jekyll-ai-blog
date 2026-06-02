---
audio: false
generated: true
image: false
lang: en
layout: post
title: High to Low Means Logical One
translated: false
type: note
---

Question: In Manchester encoding, a level transition occurs in the middle of each bit duration. What does a transition from high level to low level represent?

Answer:

Based on the provided reference answer, a transition from **high level to low level** represents a logical **1**.

### Comprehensive Explanation

**Manchester Encoding** is a synchronous clock encoding technique used by the physical layer of the Open System Interconnection (OSI) model to encode clock and data of a synchronous bit stream. In this encoding scheme, each bit period is divided into two halves, and a voltage transition occurs in the middle of each bit duration.

**Conventions and Ambiguity:**
It is important to note that there are two common conventions for defining the logic levels in Manchester encoding, which often leads to confusion:

1.  **G.E. Thomas Convention:**
    *   **High-to-Low transition:** Represents logical **1**.
    *   **Low-to-High transition:** Represents logical **0**.
2.  **IEEE 802.3 (Ethernet) Convention:**
    *   **Low-to-High transition:** Represents logical **1**.
    *   **High-to-Low transition:** Represents logical **0**.

**Context for This Question:**
Since the provided reference answer is **1**, this specific question adheres to the **G.E. Thomas convention**. Therefore, within the context of this exam problem, a transition from high电平 (high level) to low电平 (low level) in the middle of the bit duration signifies a binary **1**.

References:

- [Manchester code - Wikipedia](https://en.wikipedia.org/wiki/Manchester_code)
