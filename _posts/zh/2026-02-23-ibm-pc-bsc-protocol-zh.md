---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IBM PC BSC 协议概述
translated: true
type: note
---

### IBM PC BSC (Binary Synchronous Communication) 全面介绍

**Binary Synchronous Communication (BSC)**，通常称为 **Bisync**，是一种面向字符的同步数据链路层协议，由 IBM 于 1967 年在 System/360 系列推出后开发[[8]]。它主要设计用于 **half-duplex** 传输线，即数据可以双向传输但不能同时进行[[9]]。该协议取代了较旧的 Synchronous Transmit-Receive (STR) 协议，并成为早期主帧和个人电脑通信的标准[[11]]。

#### 1. BSC 协议的核心特性

* **Character-Oriented（面向字符）**：与位向协议（如 SDLC 或 HDLC）不同，BSC 将数据视为字符流。使用特殊控制字符（如 SOH、STX、ETX）来 framing 消息并管理数据流[[17]]。
* **Synchronous Transmission（同步传输）**：数据以由时钟信号同步的块发送，无需为每个单个字符添加起始位和停止位，从而比异步方法更高效[[16]]。
* **Half-Duplex Operation（半双工操作）**：该协议基于“turn-around（转向）”机制。一台站发送数据块后，线路必须转向前（涉及延迟过程），接收站才能发送确认（ACK）或否定确认（NAK）[[13]]。这种固有设计使其不适合全双工环境，除非采用复杂变通方法[[28]]。
* **Error Checking（错误检查）**：BSC 使用垂直和纵向冗余检查（VRC/LRC）或 Cyclic Redundancy Check (CRC) 来确保数据完整性[[15]]。

#### 2. IBM PC BSC 通信适配器

在 20 世纪 80 年代初，随着 IBM Personal Computer (PC) 和 PC AT 在企业环境中流行，有迫切需求将这些新机器连接到现有的 IBM 主帧（如 System/370）和依赖 Bisync 终端的中端系统。

* **Hardware Function（硬件功能）**：**IBM Binary Synchronous Communications (BSC) Adapter** 是一张扩展卡（通常用于 PC/XT/AT 型号的 ISA bus），提供专为同步半双工通信配置的 RS-232C 兼容接口[[3]]。
* **Configuration Limits（配置限制）**：在 IBM PC AT 等系统上，最多可安装两张 BSC 适配器。但是，如果存在 SDLC (Synchronous Data Link Control) 适配器，则仅允许一张 BSC 适配器，由于资源冲突或架构限制[[4]]。
* **Usage Scenario（使用场景）**：此适配器允许 PC 模拟传统的 3270 或其他 Bisync 终端，使用户能够运行 Remote Job Entry (RJE) 任务或访问尚未迁移到较新 SNA/SDLC 协议的主机应用程序[[31]]。

#### 3. BSC 与 SDLC 的比较

虽然 BSC 被广泛使用，但最终被 **SDLC (Synchronous Data Link Control)** 以及后来的 **SNA (Systems Network Architecture)** 取代。

* **Efficiency（效率）**：SDLC 是一种位向协议，支持全双工通信，允许同时发送和接收，比 BSC 的 stop-and-wait 特性提供显著更高的吞吐量[[28]]。
* **Transparency（透明性）**：BSC 在“data transparency（数据透明性）”方面存在问题，因为其控制字符可能出现在实际数据负载中，需要转义序列（如 DLE）。SDLC 使用 bit stuffing 更自然地处理二进制数据[[34]]。
* **Legacy Status（遗留状态）**：到 20 世纪 80 年代末和 90 年代，IBM 将重点转向 5250 仿真适配器（用于 AS/400 系统）和基于 SDLC/SNA 的 3270 仿真，使专用 BSC 适配器成为维护旧连接的遗留组件[[19]]。

#### 4. 为什么“Half-Duplex”是其定义特性

考题正确指出该适配器设计用于 **half-duplex** 线路，因为 BSC 协议本身规定了此模式。该协议依赖明确的“turnaround（转向）”序列，其中发送站发送 EOT (End of Transmission) 字符并等待线路稳定，然后接收方才能响应。这种机械和逻辑约束已硬编码到 BSC 适配器的设计中，将其与异步适配器（可全双工）或 SDLC 适配器（支持全双工）区分开来[[13]]。

### 总结

**IBM PC BSC Communication Adapter** 是一种专用硬件接口，使早期 IBM PC 能够使用 **Binary Synchronous Communication (Bisync)** 协议与遗留主帧系统通信。其设计本质上与 Bisync 的 **half-duplex**、面向字符特性相关，需要严格的 turn-around 程序进行数据交换。虽然如今已基本过时，但它在企业计算的过渡时代发挥了关键作用，桥接了 PC 革命与既有的主帧基础设施。

参考文献：

* [Binary Synchronous Communications - Wikipedia](https://en.wikipedia.org/wiki/Binary_Synchronous_Communications)
* [IBM Binary Synchronous Communications Adapter PDF](https://minuszerodegrees.net/oa/OA%20-%20IBM%20Binary%20Synchronous%20Communications%20Adapter.pdf)
* [IBM Personal Computer AT Product Announcement - Lo-tech Wiki](https://www.lo-tech.co.uk/wiki/IBM_Personal_Computer_AT_Product_Annoucement)
* [Binary Synchronous Communication (BISYNC) - GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/binary-synchronous-communication-bisync/)
* [SDLC and BSC on satellite links: a performance comparison](https://dl.acm.org/doi/10.1145/1024894.1024895)
