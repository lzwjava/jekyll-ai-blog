---
audio: false
generated: true
image: false
lang: en
layout: post
title: TDM Slot Definition Explained
translated: false
type: note
---

Question: What does "slot" (时隙) mean in the context of Time Division Multiplexing?

Answer: A **slot (时隙)** is a **fixed, brief window of time** within a repeating frame during which one specific source is allowed to transmit its data.

Think of it like this:

**Analogy — A roundtable meeting:**
Imagine 4 people sharing one microphone. Each person gets exactly 10 seconds to speak, in turn, repeating forever:

```
|  Person A  |  Person B  |  Person C  |  Person D  |  Person A  |  Person B  | ...
|  10 sec    |  10 sec    |  10 sec    |  10 sec    |  10 sec    |  10 sec    |
└────────────────── Frame 1 ──────────────────────┘└────── Frame 2 ──── ...
```

Each person's 10-second turn = **one slot**.

**In TDM technically:**

- The shared channel is divided into repeating **frames**
- Each frame is chopped into **N equal slots**
- Each slot = a tiny chunk of time (e.g., microseconds) reserved for one source to send bits
- The slot repeats every frame, so the source gets regular, periodic access

```
Frame:  [ Slot 1 | Slot 2 | Slot 3 | Slot 4 ][ Slot 1 | Slot 2 | Slot 3 | Slot 4 ] ...
Source:  [ Src A  |  Src B |  Src C |  Src D ][ Src A  |  Src B |  Src C |  Src D ] ...
```

In **synchronous TDM**, Slot 1 is *always* Src A's — even if Src A has nothing to send, that time window sits empty and wasted.

References:

- [Time-division multiplexing – Wikipedia](https://en.wikipedia.org/wiki/Time-division_multiplexing)
