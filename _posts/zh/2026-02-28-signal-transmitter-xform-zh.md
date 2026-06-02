---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 发射机信号变换
translated: true
type: note
---

问题：在通信系统模型中，哪个部分适当变换信源产生的信号以进行传输？

答案：

**A. 发送设备 (Transmitter / Sending equipment)**

**正确答案：A**

**解释：**

在经典通信系统模型（如 Shannon model）中，主要功能块有：

- **Information source** (信源)：产生原始消息或信号
- **Transmitter / Sending equipment** (发送设备)：对源信号进行必要的变换，使其适合通过信道传输。最常见的变换包括：
  - **Source coding**（减少冗余并压缩数据）
  - **Channel coding**（添加错误保护）
  - **Modulation**（将信号转换为适合物理信道的形式，例如将其变为更高频率的载波）
- **Channel** (信道)：传输信号的物理介质（有线、无线、光纤等）
- **Receiver / Receiving equipment** (接收设备)：执行逆操作（解调、信道解码、源解码）以恢复原始消息
- **Destination** (信宿)：接收最终信息
- **Noise source** (噪声源)：表示传输过程中添加的所有不需要的干扰

只有 **transmitter (发送设备)** 负责将信源产生的原始信号变换（"适当的变换"）成适合通过信道传输的形式。

因此，正确答案是 **A. 发送设备**。

参考文献：

- 无（标准通信理论知识）
