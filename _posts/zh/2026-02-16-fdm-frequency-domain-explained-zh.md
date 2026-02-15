---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 频域中的 FDM 详解
translated: true
type: note
---

问题：在频域中，信道带宽被划分为多个子信道，原始信号被调制到这些子信道对应的载波信号上，从而允许在一个信道上同时传输多个信号。这种信道复用技术被称为 ( )

A Frequency Division Multiplexing (FDM)  
B Time Division Multiplexing (TDM)  
C Wavelength Division Multiplexing (WDM)  
D Code Division Multiplexing (CDM)  

答案：A

回答：

正确答案是 **A. Frequency Division Multiplexing (FDM)**。

**解析：**

Frequency Division Multiplexing (FDM) 是一种完全在**频域**中工作的复用技术。

FDM 的核心思想是：

- 信道可用的总带宽被划分为数个较小的、互不重叠的频段（子信道）。
- 每个数据信号（或用户）被调制到其各自的载波频率上。
- 这些调制后的信号随后被合并，并同时在同一物理介质上传输。
- 由于每个信号占据不同的频率范围，它们互不干扰（只要频段被妥善分离并使用了 guard bands）。
- 在接收端，使用带通滤波器（bandpass filters）来分离不同的频段并恢复每个原始信号。

**与其他选项的简要对比：**

- **B. Time Division Multiplexing (TDM)**  
  将信道划分为**时间片（time slots）** —— 不同的信号在不同的时刻轮流使用全部带宽。

- **C. Wavelength Division Multiplexing (WDM)**  
  原理与 FDM 相似，但专门用于 **optical fiber** 系统。它划分的是光谱（不同的波长 / 光的颜色）而不是电频率带宽。

- **D. Code Division Multiplexing (CDM) / CDMA**  
  所有信号在**同一时间使用同一频段**，但每个信号都乘以一个唯一的扩频码（spreading code）。接收端使用相同的代码来提取其目标信号（广泛应用于 3G 移动通信系统）。

只有 **FDM** 符合描述：在频域中将带宽划分为多个子信道，并在不同的载波频率上同时传输多个调制信号。

因此，正确答案是 **A**。

参考资料：

- 无（标准数据通信概念，无需特定外部来源）