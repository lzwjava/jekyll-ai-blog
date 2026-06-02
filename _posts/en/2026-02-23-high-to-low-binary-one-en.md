---
audio: false
generated: true
image: false
lang: en
layout: post
title: High to Low Means Binary One
translated: false
type: note
---

Question: In Manchester encoding, a voltage transition occurs in the middle of each bit duration; what does a transition from high voltage to low voltage represent?

Answer:

In **Manchester encoding**, data is encoded such that there is always a transition in the middle of each bit period. This transition serves both as a clock signal and as the data carrier. The direction of the transition determines the binary value:

- A transition from **high to low** voltage in the middle of the bit period represents a binary **1**.
- A transition from **low to high** voltage in the middle of the bit period represents a binary **0**.

This scheme ensures synchronization between the sender and receiver, as there is guaranteed activity (a transition) in every bit interval, preventing long strings of identical bits from causing clock drift. It is widely used in Ethernet (specifically 10BASE-T) and other communication systems.

Therefore, a high-to-low transition indicates the value **1**.

References:

- [https://en.wikipedia.org/wiki/Manchester_code](https://en.wikipedia.org/wiki/Manchester_code)
