---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RS-232C 逻辑1电压详解
translated: true
type: note
---

问题：RS-232C 电气规范中逻辑 "1" 的电压水平是什么？

答案：

## RS-232C 逻辑 "1" 电压水平 — 正确答案：**D (-15V ~ -5V)**

---

### RS-232C 的关键电气特性

RS-232C 在数据传输线上使用 **inverted (negative logic)** 电压方案，这与大多数数字逻辑标准相比有些反直觉。


| State | Driver Output Voltage | Receiver Threshold |
|---|---|---|
| **Logic "1" (MARK)** | **-5V to -15V** | -3V to -15V |
| **Logic "0" (SPACE)** | **+5V to +15V** | +3V to +15V |
| **Undefined / Invalid** | -3V to +3V | — |

---

### 为什么答案是 D，而不是 C

问题特别询问 **driver output** 电压要求：

- 驱动器必须为逻辑 1 提供 **-5V to -15V**，为逻辑 0 提供 **+5V to +15V**。
- 考虑到 2V 噪声裕度，低电平 (-3V to -15V) 在 **receiver** 输入被定义为逻辑 1 (marking)。

因此区别是：
- **Driver output** （发送器发送的内容）：** -5V to -15V** → 这是 **答案 D**
- **Receiver threshold** （被接受为有效逻辑 1 的内容）：-3V to -15V → 这对应选项 C

选项 C (-13V to -3V) 描述了 **receiver** 检测范围（带噪声裕度），而不是驱动器输出要求。考试答案 **D (-15V ~ -5V)** 指的是 **driver** 所需输出电压，以正确表示逻辑 "1"。

---

### 总结

> RS-232C 使用 **negative voltage for logic "1"**（称为 "MARK"）和 **positive voltage for logic "0"**（称为 "SPACE"）。驱动器必须输出 **-5V 到 -15V** 以表示有效的逻辑 "1"。这与标准 TTL/CMOS 逻辑相反。

参考文献：

- [Fundamentals of RS-232 Serial Communications – Analog Devices](https://www.analog.com/en/resources/technical-articles/fundamentals-of-rs232-serial-communications.html)
- [RS-232 – Wikipedia](https://en.wikipedia.org/wiki/RS-232)
- [Understanding the RS-232 Standard – DigiKey](https://www.digikey.com/en/maker/blogs/2023/understanding-the-rs-232-standard)
