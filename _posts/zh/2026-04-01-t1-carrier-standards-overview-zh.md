---
audio: false
generated: true
image: false
lang: zh
layout: post
title: T1 载波标准概述
translated: true
type: note
---

问题：什么是 T1 carrier？

回答：

**T1 carrier** 是一种 **digital transmission standard**，用于电信中通过单根线路承载多个语音或数据信道。它是北美广泛使用的 **T-carrier system** 的一部分。

### 1. 基本概念

**T1 line** 使用 **Time Division Multiplexing (TDM)** 将 **24 separate voice channels** 组合成一个数字信号。

* 每个语音信道：**64 kbps**
* 信道数量：**24**
* 总有效载荷：
  ( 24 \times 64 \text{ kbps} = 1.536 \text{ Mbps} )

加上 **framing bit**，总速率：

**T1 total bit rate = 1.544 Mbps**

---

### 2. T1 帧结构

每个 **T1 frame** 包含：

* 24 信道 × 8 比特 = **192 bits**
* * 1 个 framing bit
    = **193 bits per frame**

帧持续时间：

* 每秒 8000 帧（与 PCM 采样率相同）
* 帧时间 = **125 μs**

因此：

* **193 bits per frame**
* **125 μs per frame**
* **1.544 Mbps total rate**

这就是为什么正确考试答案是：

**193 bits, 125 μs**

---

### 3. 为什么是 8000 帧/秒？

因为语音使用 **PCM** 采样：

* 采样率 = **8 kHz**
* 每个样本 = **8 bits**
* 每个帧每个信道一个样本

因此每个帧承载 **24 个信道的一个样本**。

---

### 4. 总结表格

| 项目                  | 值          |
| --------------------- | ----------- |
| 信道数                | 24          |
| 每信道比特数          | 8 bits      |
| 帧大小                | 193 bits    |
| 帧时间                | 125 μs      |
| 每秒帧数              | 8000        |
| 比特率                | 1.544 Mbps  |

---

### 5. 直观理解

可以将 T1 想象成一个 **round-robin scheduler**：

帧：

CH1 CH2 CH3 ... CH24 + FrameBit
（每个 8 bits）

每 **125 μs**：

* 发送 CH1 样本
* 发送 CH2 样本
* ...
* 发送 CH24 样本

无限重复。

---

### 6. 相关概念（考试热门）

**E1 (European standard)**

* 32 信道
* 2.048 Mbps
* 256 bits/frame

**T1 vs E1**

|            | T1         | E1           |
| ---------- | ---------- | ------------ |
| 信道数     | 24         | 32           |
| 速率       | 1.544 Mbps | 2.048 Mbps   |
| 地区       | US/Japan   | Europe/China |
| 帧比特数   | 193        | 256          |

---

### 7. 典型考试题

**Q1:** T1 帧大小？
→ **193 bits**

**Q2:** T1 帧时间？
→ **125 μs**

**Q3:** T1 数据速率？
→ **1.544 Mbps**

**Q4:** 信道数量？
→ **24**

**Q5:** 为什么是 125 μs？
→ 1 / 8000 采样率

---

参考资料：

* [https://en.wikipedia.org/wiki/T-carrier](https://en.wikipedia.org/wiki/T-carrier)
* [https://www.techtarget.com/searchnetworking/definition/T1](https://www.techtarget.com/searchnetworking/definition/T1)
