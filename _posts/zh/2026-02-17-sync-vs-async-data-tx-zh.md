---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 同步与异步数据传输
translated: true
type: note
---

问题：在通信系统中，数据传输可通过多种方式进行分类。根据发送方和接收方是否保持数据传输步调同步，可分为异步通信和_______。

答案：

答案为 **synchronous communication**（同步通信）。

## 解释

在通信系统中，数据传输方式根据发送方和接收方之间的同步机制进行分类：

**异步通信（Asynchronous Communication）** 是指发送方和接收方无需保持同步时钟或定时的数据传输方式。每个数据单元（通常为字符）独立传输，并使用起始位和停止位对数据进行帧定界。接收方通过检测这些帧信号确定数据的开始和结束。此方法较为简单，不需发送方和接收方之间精确的时钟同步，但由于帧位开销，效率较低。

**同步通信（Synchronous Communication）** 是其对应的分类方式。在同步传输中，发送方和接收方保持同步时钟或使用共同的定时参考。数据以连续的块形式传输，无需为单个字符添加起始位和停止位。此方法更高效，因为消除了帧开销，但需要更复杂的硬件来维持双方时钟同步。

这两种方法代表了基于定时同步需求的数据传输基本分类。关键区别在于：是否需要为每个数据单元提供显式定时信号（异步），还是双方基于共享的定时参考运行（同步）。

参考资料：

- [Communication System Architecture - Synchronous vs Asynchronous Transmission](https://en.wikipedia.org/wiki/Asynchronous_serial_communication)
