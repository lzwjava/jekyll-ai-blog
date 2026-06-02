---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 奈奎斯特公式计算出 24 Kbps
translated: true
type: note
---

问题：根据 Nyquist formula，如果信道带宽 H = 3 KHz，每个信号符号可以取 N = 16 个离散值，则信道的最大数据传输速率是多少？

答案：

Nyquist formula 决定了无噪信道中的最大数据传输速率。以下是解决方案：

**Given Information:**

- Channel bandwidth (H) = 3 KHz
- Number of discrete signal levels (N) = 16

**Solution Process:**

根据 Nyquist theorem，在无噪信道中，最大符号率（baud rate）为：

**Maximum symbol rate = 2 × H**

因此：

- Maximum symbol rate = 2 × 3 KHz = 6 kilobaud (symbols per second)

数据传输速率与符号率的关系为：

**Data transmission rate = Symbol rate × log₂(N)**

其中 log₂(N) 表示每个符号的比特数。

由于 N = 16：

- log₂(16) = 4 bits per symbol

因此：
**Maximum data transmission rate = 6 × 4 = 24 kbps**

**Explanation:**

Nyquist theorem 确立了最大符号率是带宽的两倍。每个符号有 16 个可能的离散值，每个符号可以编码 log₂(16) = 4 bits 的信息。将最大符号率乘以每个符号的比特数，即得到最大数据传输速率。

**Correct Answer: B (24 Kbps)**

您的答案 C (48 Kbps) 似乎直接将带宽乘以 16，而没有正确应用 Nyquist theorem 的 2× 因子，或者错误地将 log₂(16) 计算为 8 而非 4。
