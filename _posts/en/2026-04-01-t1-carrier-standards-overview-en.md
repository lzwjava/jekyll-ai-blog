---
audio: false
generated: true
image: false
lang: en
layout: post
title: Overview of T1 Carrier Standards
translated: false
type: note
---

Question: What is a T1 carrier?

Answer:

**T1 carrier** is a **digital transmission standard** used in telecommunications to carry multiple voice or data channels over a single line. It is part of the **T-carrier system** widely used in North America.

### 1. Basic Idea

A **T1 line** combines **24 separate voice channels** into one digital signal using **Time Division Multiplexing (TDM)**.

* Each voice channel: **64 kbps**
* Number of channels: **24**
* Total payload:
  ( 24 \times 64 \text{ kbps} = 1.536 \text{ Mbps} )

Plus **framing bit**, total rate:

**T1 total bit rate = 1.544 Mbps**

---

### 2. T1 Frame Structure

Each **T1 frame** contains:

* 24 channels × 8 bits = **192 bits**
* * 1 framing bit
    = **193 bits per frame**

Frame duration:

* 8000 frames per second (same as PCM sampling rate)
* Frame time = **125 μs**

So:

* **193 bits per frame**
* **125 μs per frame**
* **1.544 Mbps total rate**

This is why the correct exam answer is:

**193 bits, 125 μs**

---

### 3. Why 8000 frames/sec?

Because voice is sampled using **PCM**:

* Sampling rate = **8 kHz**
* Each sample = **8 bits**
* One sample per channel per frame

So each frame carries **one sample of each of the 24 channels**.

---

### 4. Summary Table

| Item              | Value      |
| ----------------- | ---------- |
| Channels          | 24         |
| Bits per channel  | 8 bits     |
| Frame size        | 193 bits   |
| Frame time        | 125 μs     |
| Frames per second | 8000       |
| Bit rate          | 1.544 Mbps |

---

### 5. Intuitive Understanding

Think of T1 like a **round-robin scheduler**:

Frame:

CH1 CH2 CH3 ... CH24 + FrameBit
(8 bits each)

Every **125 μs**:

* send CH1 sample
* send CH2 sample
* ...
* send CH24 sample

Repeat forever.

---

### 6. Related Concepts (Exam Favorites)

**E1 (European standard)**

* 32 channels
* 2.048 Mbps
* 256 bits/frame

**T1 vs E1**

|            | T1         | E1           |
| ---------- | ---------- | ------------ |
| Channels   | 24         | 32           |
| Rate       | 1.544 Mbps | 2.048 Mbps   |
| Region     | US/Japan   | Europe/China |
| Frame bits | 193        | 256          |

---

### 7. Typical Exam Questions

**Q1:** T1 frame size?
→ **193 bits**

**Q2:** T1 frame time?
→ **125 μs**

**Q3:** T1 data rate?
→ **1.544 Mbps**

**Q4:** Number of channels?
→ **24**

**Q5:** Why 125 μs?
→ 1 / 8000 sampling rate

---

References:

* [https://en.wikipedia.org/wiki/T-carrier](https://en.wikipedia.org/wiki/T-carrier)
* [https://www.techtarget.com/searchnetworking/definition/T1](https://www.techtarget.com/searchnetworking/definition/T1)
