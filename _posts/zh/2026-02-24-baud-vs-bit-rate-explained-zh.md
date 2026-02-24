---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 波特率与比特率详解
translated: true
type: note
---

问题：网络中“baud”的定义和意义是什么？

回答：在网络和电信中，**baud**（或 baud rate）指的是每秒传输的**signal units** 或 "symbols" 的数量。虽然经常与 bit rate 混淆，但它具体测量的是电信号或光信号的变化速率，而不是通过线路传输的原始数据总量。

### 理解区别：Baud 与 Bit Rate

要理解 baud，必须区分“容器”（symbol）和“内容”（bits）。

* **Baud Rate：** 信号状态每秒变化的次数（pulses、voltage shifts 或 phase changes）。
* **Bit Rate：** 每秒实际传输的 1 和 0 的数量。

### 关系公式

两者之间的关系由调制复杂度决定。如果单个信号变化（一个 baud）携带不止一位数据，则 bit rate 将高于 baud rate。这可以用公式表示：

$$\text{Bit Rate} = \text{Baud Rate} \times \text{Bits per Symbol}$$

### 关键特性

* **Efficiency：** 现代调制解调器使用高级调制（如 QAM）将多个 bits 打包到一个 symbol 中。例如，如果系统使用 16-QAM，每个 "symbol" 代表 4 bits。如果 baud rate 为 1,000，则 bit rate 为 4,000 bps。
* **Physical Limits：** 高 baud rate 在长距离上传输更难维持，因为快速信号变化更容易受到噪声和失真的影响。
* **Origin：** 该术语以**Émile Baudot**命名，他是用于电报的 Baudot code 的发明者。

---

您想让我解释特定的调制技术，如 QAM 或 PSK，这些技术允许我们将更多 bits 装入单个 baud 吗？