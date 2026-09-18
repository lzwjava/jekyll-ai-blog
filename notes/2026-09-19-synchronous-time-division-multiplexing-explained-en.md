---
audio: false
generated: true
image: false
lang: en
layout: post
title: Synchronous Time-Division Multiplexing Explained
translated: false
type: note
---

Question: What is **同步时分多路复用（Synchronous TDM, Synchronous Time-Division Multiplexing）**?

Answer:

**Synchronous TDM** is a technique that lets **multiple low-speed data streams share one high-speed communication link by taking turns in fixed time slots**.

![Image](https://images.openai.com/static-rsc-4/TBf4IvUxKLzd1irrBbNo-hyqbz8GdkEsxEwstey5oX_GsHMibfG1QBFFBRJex-oCJvFOzRACsaa3q-ckOnruGf_M7qpbJyJ10DWVzJRxUjHMzVkZEpF68jx-KjsHeB66j-NDHcD-5WgO-T8bijKgp5ETNNXhM3wdD7xsOHl_6bjFA6kCfYjoU1N8ESy_xUpg?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/QuUf3sULJA4PPOXyEQNDG8DFQjOQExHSgkYXg9EZVgzPCON1Cfc4NzR39Um2Kq1YAMtzft9XceLM2LrtsqyLfynLj-1s5uOlB5dpHyUI3ODqSXC1WqMYqvQ2mWER1Qs6hxkOdVu3XwvHIhQ82MTbr4lzpVqPcyJsBoy_d80J8WHF0FbpJOO8PP05UYMYL1f8?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NfvsF1s4cuNFzJYirPhHF-dBCTpjKxdzyvVc3P5qFBWl8ChwVSWqsvjgPOx71D8vrPPjTl-tr-3BNSqIpc-YOy8Mc61yu6A3pK1BA-iKbIeSA1sdmaZCVFEhDTQf1NYd0OZeEBV6vypKiiW3RSquG0Yqma8rY6RsCThYOu5cTUqnSQeVinxYascA4KnjTrr4?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/UAkHOF5GUcuHDGcTEG4A-KU_f5Z9DAPRWs966cvZ4zUVuxDi-riNaxL3srr2U1gviZJ9rQnsg9SeUPs7gROxHmdIyhEgePOnWDwwVv91u1yEPaDuIOP7r-dbmU3RxSvQ355G1i7nYPfErr1q3uP5v_uqAMa3kpGQLRv7MLEom3i2lYI6z59Q6EEDCMIjq4Bm?purpose=fullsize)

### 1. Basic idea

Suppose we have four input channels:

```text
Channel A ──┐
Channel B ──┤
Channel C ──┼──> [ Multiplexer ] ──> High-speed link
Channel D ──┘
```

TDM divides time into small **time slots**:

```text
Time ─────────────────────────────────────>

| A | B | C | D | A | B | C | D | A | B | ...
```

Each channel gets a **fixed position** in every frame.

For example:

```text
Frame 1: | A | B | C | D |
Frame 2: | A | B | C | D |
Frame 3: | A | B | C | D |
```

The receiver knows:

> slot 1 → A
> slot 2 → B
> slot 3 → C
> slot 4 → D

So it can demultiplex the combined stream.

---

### 2. Why is it called "synchronous"?

Because the transmitter and receiver are synchronized to the same **slot/frame structure**.

For example:

```text
             Frame
       ┌─────────────────┐
       │ A │ B │ C │ D   │
       └─────────────────┘
         ↑   ↑   ↑   ↑
       fixed fixed fixed
       slot  slot  slot
```

Even if channel C has **nothing to send**, its slot is normally still reserved:

```text
| A | B | -- | D | A | B | -- | D |
          ↑
       unused
```

This is the key characteristic of synchronous TDM.

---

### 3. Contrast with statistical TDM

This is probably the most important distinction for exams.

**Synchronous TDM:**

```text
| A | B | C | D | A | B | C | D |
```

Every channel gets a slot **regardless of whether it has data**.

**Statistical TDM:**

```text
| A | C | C | D | A | D | B | C |
```

Slots are dynamically assigned to channels that actually have data.

Therefore:

|                     | Synchronous TDM              | Statistical TDM                   |
| ------------------- | ---------------------------- | --------------------------------- |
| Slot assignment     | Fixed                        | Dynamic                           |
| Idle channel's slot | Usually wasted               | Can be used by others             |
| Efficiency          | Lower when traffic is bursty | Higher                            |
| Control complexity  | Simple                       | More complex                      |
| Synchronization     | Required                     | Required, plus addressing/control |

---

### 4. Example

Imagine four telephone channels, each producing:

```text
64 kb/s
```

With synchronous TDM:

```text
A = 64 kb/s
B = 64 kb/s
C = 64 kb/s
D = 64 kb/s
```

The multiplexer combines them:

```text
64 + 64 + 64 + 64 = 256 kb/s
```

Ignoring framing/overhead, the output link needs about:

```text
256 kb/s
```

The transmission looks like:

```text
A1 B1 C1 D1 A2 B2 C2 D2 A3 B3 C3 D3 ...
```

At the other end:

```text
                    ┌──> A
High-speed stream ──┼──> B
                    ├──> C
                    └──> D
```

The demultiplexer uses the known slot positions to recover each channel.

---

### 5. The core mental model

Think of a **round-robin CPU scheduler**:

```text
A → B → C → D → A → B → C → D → ...
```

Except instead of CPU time, we're allocating **communication time**.

So the one-sentence definition is:

> **Synchronous TDM divides a shared communication link into fixed, periodically repeating time slots and assigns each input channel a predetermined slot.**

The two words to remember are:

**fixed slot + periodic repetition**.

A useful next step would be for me to derive **TDM frame/slot duration and bit-rate calculations**, including the common Chinese networking-exam problems.
