---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed Order Time Division Multiplexing
translated: false
type: note
---

Question: In time-division multiplexing, which type is characterized by allocating time slots to various signals in a fixed order?

Answer: 

The type of time-division multiplexing that allocates time slots to various signals in a **fixed order** is called **Synchronous Time-Division Multiplexing (STDM)**.

### Explanation:
- **Synchronous TDM**: 
  - Time slots are pre-assigned to each input channel in a round-robin fashion, regardless of whether the channel has data to send.
  - The order of transmission is fixed and predictable.
  - If a channel has no data, its time slot remains empty, which can lead to inefficiency.
  - Commonly used in traditional telephone systems (e.g., T1/E1 lines).

- **Asynchronous TDM (also known as Statistical TDM)**:
  - Time slots are allocated dynamically based on demand.
  - Only active channels get time slots, improving bandwidth efficiency.
  - The order is not fixed; it depends on which channels have data ready to transmit.

Since the question specifies "allocating time slots in a fixed order," the correct answer is **Synchronous Time-Division Multiplexing**.

References:  

- [Time-division multiplexing - Wikipedia](https://en.wikipedia.org/wiki/Time-division_multiplexing)