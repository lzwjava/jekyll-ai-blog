---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 符号率单位详解
translated: true
type: note
---

Question: What is the unit of symbol rate (also known as baud rate or symbol transmission rate)?

Answer:

The correct answer is **B. Baud**。

**Explanation in English:**

- **Symbol rate**（也称为 **baud rate**、**symbol transmission rate** 或 **modulation rate**）衡量每秒传输多少个 **symbols**（截然不同的信号单元）。
- 一个 symbol 可以代表一个或多个 bits，具体取决于 modulation scheme（例如，在 BPSK 中 1 symbol = 1 bit，在 16-QAM 中 1 symbol = 4 bits）。
- symbol rate 的 **standard unit** 是 **Baud**（写作 **Bd** 或简称为 "baud"）。

常见单位及其含义：

- **Bit/s** (bps) → bit rate = 每秒传输的 bits 数量
- **Baud** → symbol rate = 每秒传输的 symbols 数量
- **Byte** → 8 bits（不是速率单位）
- **Word** → 通常为 16 或 32 bits，取决于系统（不是速率单位）

核心关系：

```
Bit rate (bps) = Symbol rate (baud) × bits per symbol (log₂M)
```

Examples：

- BPSK：每个 symbol 1 bit → bit rate = baud rate
- QPSK：每个 symbol 2 bits → bit rate = 2 × baud rate
- 16-QAM：每个 symbol 4 bits → bit rate = 4 × baud rate

所以 **symbol rate (码元速率)** 的直接单位是 **Baud**，而不是 bit、byte 或 word。

因此正确选项是 **B. Baud**。

References:

- 对于这一标准 communication theory 概念，无需参考资料。
