---
audio: false
generated: true
image: false
lang: zh
layout: post
title: E1载波数据速率计算
translated: true
type: note
---

问题：在 E1 carrier 标准中，一帧由 256 bits 组成，并在 125 微秒内传输。E1 carrier 的数据传输速率是多少？

A. 1.544 Mbps
B. 2.048 Mbps
C. 3.045 Mbps
D. 4.025 Mbps

答案：

**B. 2.048 Mbps**

**计算说明：**

传输速率可以使用以下公式计算：

Data rate = (每帧 bits 数) ÷ (每帧时间，秒)

- Bits per frame = 256 bits
- Time per frame = 125 microseconds = 125 × 10⁻⁶ seconds = 0.000125 seconds

Data rate = 256 ÷ 0.000125 = 2,048,000 bits per second = **2.048 Mbps**

这与标准的 E1 速率匹配。

**附加上下文（为什么 E1 是 2.048 Mbps）：**

E1 使用 synchronous time-division multiplexing，并包含：
- 30 voice channels × 64 kbps = 1,920 kbps
- 2 signaling/control channels × 64 kbps = 128 kbps（通常实现为 16 个时隙各 8 bits，但有效为 2 × 64 kbps）
- 加上每帧 1 个 framing bit

每帧总计：32 time slots × 8 bits = 256 bits
帧以每秒 8,000 次发送（125 μs 间隔，匹配 PCM voice 的 8 kHz 采样率）

因此：256 bits/frame × 8,000 frames/second = 2,048,000 bps = **2.048 Mbps**

这是国际标准化的 E1 速率（ITU-T G.703/G.704），不同于北美 T1 的 1.544 Mbps 速率。

参考文献：

- 无（标准 telecommunications 知识；计算是确定的）
