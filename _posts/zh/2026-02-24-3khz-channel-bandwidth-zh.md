---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 3 kHz 信道带宽详解
translated: true
type: note
---

Question: What is channel bandwidth (H) = 3 KHz?

Answer:

**Channel Bandwidth** 是电信和信号处理中的一个基本概念，指通信信道可以传输的频率范围。

**Definition:**

Channel bandwidth (H) = 3 KHz 表示信道可以在 3,000 Hz（3 kilohertz）的频率范围内传输信号。这代表信道支持的最高频率和最低频率之间的差值。

**Mathematical Expression:**

Bandwidth (H) = f_max - f_min

In this case:
- The frequency span available for signal transmission is 3,000 Hz
- If the channel starts at frequency f_min and ends at f_max, the difference equals 3 KHz

**Key Characteristics:**

1. **Measurement Unit:** Kilohertz (KHz), where 1 KHz = 1,000 Hz

2. **Frequency Range:** A 3 KHz bandwidth means the channel can accommodate signals with frequencies spanning 3,000 cycles per second

3. **Data Capacity:** Wider bandwidth allows higher data transmission rates. A 3 KHz bandwidth is relatively narrow (typical for voice channels or older communication systems)

4. **Signal Constraints:** Any signal transmitted through this channel must fit within the 3 KHz frequency spectrum

**Practical Context:**

在您之前提出的 Nyquist theorem 问题中，3 KHz bandwidth 用于计算最大符号率（6 kilobaud = 2 × 3 KHz），然后结合可用信号电平数量确定最大数据传输率。

**Example Applications:**
- Telephone voice channels typically use approximately 3-4 KHz bandwidth
- Historical data communication systems operated within similar bandwidth constraints
- Modern systems often use much wider bandwidths (MHz or GHz range) for higher data rates