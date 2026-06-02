---
audio: false
generated: true
image: false
lang: zh
layout: post
title: E1载波数据速率详解
translated: true
type: note
---

问题：ITU 为欧洲推荐的 PCM carrier 标准 E1 carrier 的数据速率是多少？

答案：

正确答案是 **B: 2.048 Mbps**。

### 解释：
**E1 carrier** 是一种数字传输格式，广泛用于欧洲和世界其他地区（北美和日本除外，它们使用 T1 标准）。它由 **International Telecommunication Union (ITU)** 标准化。

- **Data Rate**：E1 线路的总数据速率是 **2.048 Mbps**。
- **Channel Structure**：
  - 它使用 **Time Division Multiplexing (TDM)** 将多个信道组合成单个流。
  - E1 帧由 **32 time slots**（信道）组成，每个以 **64 kbps** 运行。
    - **30 channels** 用于语音或用户数据（B-channels）。
    - **1 channel**（Time Slot 0）用于 framing 和 synchronization。
    - **1 channel**（Time Slot 16）通常用于 signaling 和 control information。
- **Calculation**：
  $$32 \text{ channels} \times 64 \text{ kbps} = 2048 \text{ kbps} = 2.048 \text{ Mbps}$$

相比之下，**T1 carrier**（主要用于北美和日本）的数据速率是 **1.544 Mbps**，对应选项 A。选项 C 和 D 是与标准 PCM carrier 系统无关的不正确值。
