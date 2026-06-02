---
audio: false
generated: true
image: false
lang: en
layout: post
title: T1 Frame Structure and Timing
translated: false
type: note
---

Question: In the T1 carrier standard, what are the number of bits per frame and the time to transmit one frame?

Answer:

## T1 Carrier Standard – Frame Structure Explained

### Correct Answer: **A** — 193 bits, 125 μs

---

## Key Concepts

### 1. T1 Carrier Overview
T1 is a North American digital transmission standard that multiplexes **24 voice channels** using **Time Division Multiplexing (TDM)**.

---

### 2. Frame Calculation

| Parameter | Value | Explanation |
|---|---|---|
| Number of voice channels | 24 | T1 standard supports 24 DS0 channels |
| Bits per channel per frame | 8 bits | Each voice sample = 8-bit PCM encoding |
| Data bits total | 24 × 8 = **192 bits** | All 24 channels combined |
| Framing/Sync bit | **+1 bit** | One synchronization bit added per frame |
| **Total bits per frame** | **193 bits** | 192 + 1 = 193 |

> **Formula:**
> Total bits = (Number of channels × bits per sample) + 1 sync bit
> = (24 × 8) + 1 = **193 bits**

---

### 3. Frame Duration Calculation

The frame duration comes from **voice sampling theory**:

- According to **Nyquist theorem**, voice (bandwidth ~4 kHz) must be sampled at **8,000 times per second**
- Therefore, each sample occurs every:

$$\text{Frame period} = \frac{1}{8000} = 0.000125 \text{ seconds} = \mathbf{125\ \mu s}$$

---

### 4. Why Option B is Wrong

| Option | Bits | Time | Status |
|---|---|---|---|
| A | 193 bits | 125 μs | ✅ Correct |
| B | 193 bits | 250 μs | ❌ Wrong – frame period should be 125 μs, not 250 μs |
| C | 256 bits | 125 μs | ❌ Wrong – 256 bits is E1 standard, not T1 |
| D | 256 bits | 250 μs | ❌ Wrong – both values incorrect |

> **250 μs** would correspond to a sampling rate of only **4,000 Hz**, which violates Nyquist sampling theorem for voice signals.

---

### 5. T1 vs E1 Comparison (Common Exam Trap)

| Feature | T1 (North America) | E1 (Europe) |
|---|---|---|
| Channels | 24 | 32 (30 voice + 2 control) |
| Bits per frame | **193** | **256** |
| Frame period | **125 μs** | **125 μs** |
| Total bit rate | 1.544 Mbps | 2.048 Mbps |

> ⚠️ **Exam tip:** If you see **256 bits**, that's **E1**, not T1!

---

### Summary

- T1 = 24 channels × 8 bits + 1 sync bit = **193 bits/frame**
- Sampling rate = 8000 Hz → frame period = **125 μs**
- T1 total bit rate = 193 bits × 8000 frames/sec = **1.544 Mbps**
