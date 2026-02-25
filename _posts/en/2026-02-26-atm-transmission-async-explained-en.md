---
audio: false
generated: true
image: false
lang: en
layout: post
title: ATM Transmission Asynchronous Explained
translated: false
type: note
---

Question: In ATM transmission mode, since cells containing information do not need to appear periodically on the channel, is this transmission mode considered asynchronous or synchronous?

Answer:

The correct answer is **asynchronous**.

### Explanation

**Asynchronous Transfer Mode (ATM)** is named specifically because of its **asynchronous** nature regarding the timing of cell transmission. Here is a comprehensive breakdown:

1.  **Definition of Asynchronous in this Context**:
    In traditional synchronous transmission (like TDM - Time Division Multiplexing), time slots are pre-assigned to specific channels. Even if a channel has no data to send, its time slot remains empty but reserved, appearing periodically on the line.
    
    In contrast, ATM uses **statistical multiplexing**. Cells are transmitted only when there is actual data to send. There is no fixed, periodic time slot assigned to a specific connection. A cell containing user information can appear at any time, and gaps between cells from the same source vary depending on traffic load.

2.  **Why it is not Synchronous**:
    If the transmission were synchronous, the cells belonging to a specific virtual circuit would arrive at regular, predictable intervals (periodically), regardless of whether they carried payload data or just idle fillers. The question explicitly states that the cells "do not need to appear periodically," which is the defining characteristic that rules out synchronous transmission.

3.  **Key Characteristics of ATM**:
    *   **Fixed-length cells**: ATM uses small, fixed-size packets called cells (53 bytes: 5-byte header + 48-byte payload).
    *   **Connection-oriented**: It establishes a virtual circuit before data transfer.
    *   **Statistical Multiplexing**: Bandwidth is allocated dynamically based on demand, leading to the non-periodic arrival of cells described in the question.

Therefore, because the presence of information-bearing cells is not tied to a rigid, periodic clock cycle for each individual channel, the mode is **asynchronous**.