---
audio: false
generated: true
image: false
lang: zh
layout: post
title: T1 帧结构和定时
translated: true
type: note
---

Question: 在 T1 carrier 标准中，每帧的比特数和传输一帧的时间是多少？

Answer:

## T1 Carrier Standard – 帧结构详解

### 正确答案：**A** — 193 bits, 125 μs

---

## 关键概念

### 1. T1 Carrier 概述

T1 是北美数字传输标准，使用 **Time Division Multiplexing (TDM)** 多路复用 **24 voice channels**。

---

### 2. 帧计算

| 参数 | 值 | 解释 |
| --- | --- | --- |
| Voice channels 数量 | 24 | T1 标准支持 24 DS0 channels |
| 每通道每帧比特数 | 8 bits | 每个语音样本 = 8-bit PCM 编码 |
| 数据比特总数 | 24 × 8 = **192 bits** | 所有 24 个通道的总和 |
| Framing/Sync bit | **+1 bit** | 每帧添加一个同步比特 |
| **每帧总比特数** | **193 bits** | 192 + 1 = 193 |

> **公式：**
> 总比特数 = (通道数 × 每样本比特数) + 1 sync bit
> = (24 × 8) + 1 = **193 bits**

---

### 3. 帧持续时间计算

帧持续时间来源于 **voice sampling theory**：

- 根据 **Nyquist theorem**，语音（带宽 ~4 kHz）必须以 **8,000 次/秒** 采样
- 因此，每个样本间隔为：

$$\text{Frame period} = \frac{1}{8000} = 0.000125 \text{ seconds} = \mathbf{125\ \mu s}$$

---

### 4. 为什么选项 B 错误

| 选项 | Bits | Time | 状态 |
| --- | --- | --- | --- |
| A | 193 bits | 125 μs | ✅ 正确 |
| B | 193 bits | 250 μs | ❌ 错误 – 帧周期应该是 125 μs，而不是 250 μs |
| C | 256 bits | 125 μs | ❌ 错误 – 256 bits 是 E1 标准，不是 T1 |
| D | 256 bits | 250 μs | ❌ 错误 – 两个值都错误 |

> **250 μs** 对应采样率为仅 **4,000 Hz**，这违反了语音信号的 Nyquist 采样定理。

---

### 5. T1 与 E1 比较（常见考试陷阱）

| 特性 | T1 (北美) | E1 (欧洲) |
| --- | --- | --- |
| Channels | 24 | 32 (30 voice + 2 control) |
| 每帧比特数 | **193** | **256** |
| 帧周期 | **125 μs** | **125 μs** |
| 总比特率 | 1.544 Mbps | 2.048 Mbps |

> ⚠️ **考试提示：** 如果看到 **256 bits**，那是 **E1**，不是 T1！

---

### 总结

- T1 = 24 channels × 8 bits + 1 sync bit = **193 bits/frame**
- 采样率 = 8000 Hz → 帧周期 = **125 μs**
- T1 总比特率 = 193 bits × 8000 frames/sec = **1.544 Mbps**
