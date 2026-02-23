---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IBM PC BSC 适配器 半双工线路
translated: true
type: note
---

问题：IBM PC BSC communication adapter 主要设计用于哪种类型的传输线路？

答案：

**IBM PC BSC (Binary Synchronous Communication) communication adapter** 主要设计用于 **half-duplex transmission lines**。

### 解释：
- **BSC (Binary Synchronous Communication)** 是 IBM 开发的一种面向字符的同步数据链路层协议。
- 它在早期的 mainframe 和 PC 通信中常用。
- 在 **half-duplex** 通信中，数据可以双向传输，但 **不能同时**进行。这符合 BSC 的操作模型，其中发送方和接收方轮流传输。
- Full-duplex 允许同时双向通信，这在没有额外硬件或协议增强的情况下，通常不被基本的 BSC 实现支持。
- 因此，IBM PC BSC adapter 针对 **half-duplex** 环境进行了优化。

**正确答案：**  
**A. 半双工传输线路设计的 (Designed for half-duplex transmission lines)**

参考文献：