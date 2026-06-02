---
audio: false
generated: true
image: false
lang: en
layout: post
title: E1 Carrier Data Rate Explained
translated: false
type: note
---

Question: What is the data rate of the E1 carrier, the PCM carrier standard recommended by the ITU for Europe?

Answer:

The correct answer is **B: 2.048 Mbps**.

### Explanation:
The **E1 carrier** is a digital transmission format widely used in Europe and other parts of the world (excluding North America and Japan, which use the T1 standard). It was standardized by the **International Telecommunication Union (ITU)**.

- **Data Rate**: The total data rate of an E1 line is **2.048 Mbps**.
- **Channel Structure**:
  - It uses **Time Division Multiplexing (TDM)** to combine multiple channels into a single stream.
  - An E1 frame consists of **32 time slots** (channels), each operating at **64 kbps**.
    - **30 channels** are used for voice or user data (B-channels).
    - **1 channel** (Time Slot 0) is used for framing and synchronization.
    - **1 channel** (Time Slot 16) is typically used for signaling and control information.
- **Calculation**:
  $$32 \text{ channels} \times 64 \text{ kbps} = 2048 \text{ kbps} = 2.048 \text{ Mbps}$$

In contrast, the **T1 carrier** (used primarily in North America and Japan) has a data rate of **1.544 Mbps**, which corresponds to option A. Options C and D are incorrect values not associated with standard PCM carrier systems.
