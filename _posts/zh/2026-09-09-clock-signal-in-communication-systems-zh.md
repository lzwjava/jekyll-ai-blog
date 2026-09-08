---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通信系统中的时钟信号
translated: true
type: note
---

Question: 在通信系统中，什么是 clock signal？

Answer:

一个 clock signal 是一种周期性振荡信号，用于 **synchronize** 数字电路和通信系统的操作。它充当时间参考，协调数据的发送、接收和处理时间。

**核心特性**

- 通常是在 HIGH (1) 和 LOW (0) 状态之间交替的 square wave
- 由其 **frequency** (Hz) 定义——每秒的周期数
- 由其 **period** (T = 1/f) 定义——一个完整周期的持续时间
- 具有 **duty cycle**——HIGH 时间与总周期的比率（通常为 50%）

**在通信系统中的作用**

| Function | Description |
| --- | --- |
| **Synchronization** | 确保发送方和接收方在同一时刻采样数据 |
| **Bit timing** | 精确定义每个 bit 的开始和结束时刻 |
| **Data framing** | 将 bits 分组为 bytes、frames 或 packets |
| **Error reduction** | 防止因时序漂移而误读 bits |

**两种同步模型**

- **Synchronous** — 共享的 clock signal 与数据一同显式传输（例如 SPI、I²C、以及通过 baud rate 约定的 UART）
- **Asynchronous** — 没有共享 clock 线；时序通过 **CDR (Clock and Data Recovery)** 等技术从数据流本身恢复

**为什么重要**

如果没有 clock signal，接收方将不知道*何时*采样传入的 bit——导致错位、数据损坏或通信完全失败。每个现代协议（USB、Ethernet、PCIe、HDMI）都依赖于精确的 clock 管理。

参考文献：

- [Clock Signal – Wikipedia](https://en.wikipedia.org/wiki/Clock_signal)
- [Synchronous vs Asynchronous Communication – Electronics Hub](https://www.electronicshub.org/synchronous-and-asynchronous-transmission/)
- [Clock and Data Recovery (CDR) – Texas Instruments](https://www.ti.com/lit/an/slyt075/slyt075.pdf)
