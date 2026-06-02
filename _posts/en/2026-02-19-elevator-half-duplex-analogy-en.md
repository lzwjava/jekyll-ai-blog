---
audio: false
generated: true
image: false
lang: en
layout: post
title: Elevator as Half Duplex Analogy
translated: false
type: note
---

Question: No, I mean that an elevator, at any one point in time, can only move either up or down (not both directions simultaneously), so it is half-duplex in that analogy.

Answer:

Yes, that's a very reasonable and commonly used analogy.

In communication theory:

- **Half-duplex** = two parties / directions can communicate, but **not at the same time**. One must wait (or yield) while the other is active. Classic examples: walkie-talkies, many older intercoms, turn-based chat.

The elevator direction behaves the **same way**:

| Property                          | Full-duplex communication          | Half-duplex communication          | Elevator movement                  |
|-----------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|
| Can both directions be active simultaneously? | Yes                                 | No                                  | No                                  |
| Directions / parties              | Both can send & receive at once     | Only one can send at a time         | Only one direction (up **or** down) at a time |
| Switching                         | No need to switch                   | Must switch / take turns            | Must reverse direction to change    |
| Resource sharing                  | Separate channels / full bandwidth both ways | Shared medium / channel             | Shared shaft / hoistway             |
| Real-world intuition              | Telephone call                      | Push-to-talk radio                  | Single elevator car in a shaft      |

So when people say “the elevator is half-duplex”, they are usually **not** talking about the emergency intercom, but using the **physical motion** of the elevator car as a teaching analogy for half-duplex communication.

This analogy appears quite often in:

- Networking textbooks and lectures (especially when explaining why Ethernet hub networks were half-duplex)
- Operating systems / concurrency lectures (shared resource that can only serve one direction at a time)
- Informal engineering & computer science discussions

Quick examples of the analogy in use:

- “Think of a single-lane bridge or an elevator: only one direction of traffic at a time → half-duplex.”
- “A half-duplex link is like an elevator in a building — it can go up or down, but not both at once.”

Your interpretation is correct and widely understood in exactly that sense.

References:

- None (this is a standard conceptual analogy taught in computer networking and does not rely on a specific external source)
