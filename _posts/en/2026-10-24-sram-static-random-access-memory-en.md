---
audio: false
generated: true
image: false
lang: en
layout: post
title: "SRAM: Static Random-Access Memory"
translated: false
type: note
---

Question: What does the acronym SRAM stand for, and what is it?

Answer: **SRAM** stands for **Static Random-Access Memory**. It is a type of computer memory with two main characteristics:

- **Static** — it retains data as long as power is supplied, without needing periodic refresh cycles (unlike DRAM, which must be refreshed constantly).
- **Random-Access** — any memory location can be read or written in roughly the same amount of time, regardless of its physical position.

**How it works:** Each bit is stored using a circuit called a *bistable latch* (typically 6 transistors), which holds its state stably until power is removed or the bit is overwritten.

**Key traits compared to DRAM:**

| | SRAM | DRAM |
| --- | --- | --- |
| Speed | Faster | Slower |
| Cost | Higher | Lower |
| Density | Lower (more transistors per bit) | Higher |
| Needs refresh? | No | Yes |
| Typical use | CPU cache (L1/L2/L3) | Main system RAM |

**Common uses:**

- CPU caches (L1, L2, L3)
- Registers and buffers in microcontrollers
- Networking equipment (routers, switches)
- Embedded systems where speed matters more than capacity

References:

- [Static random-access memory – Wikipedia](https://en.wikipedia.org/wiki/Static_random-access_memory)
