---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 可靠传输的信道编码方法
translated: true
type: note
---

问题：现代数据通信系统中通过 channel coding 实现的典型错误控制方法有哪些，以提高传输可靠性？

答案：

数据通信系统中的错误控制主要通过 **channel coding** 技术实现，该技术为传输的信息添加冗余。这允许检测传输错误，并根据机制进行纠正或其他处理。它是增强噪声信道数据传输可靠性的关键方法。

该语句列出了四种典型的错误控制方法：

1. **检错重发 (Error Detection with Retransmission / ARQ - Automatic Repeat reQuest)**  
   发送方添加错误检测码（例如，CRC 或 parity bits）。接收方检查错误。如果检测到错误，则丢弃错误帧，并通过反馈信道向发送方发送请求，重传相同数据。  
   这是计算机网络中最广泛使用的方法（例如，TCP、数据链路层协议如 HDLC）。它提供高可靠性，但由于重传引入可变延迟。

2. **前向纠错 (Forward Error Correction / FEC)**  
   发送方使用纠错码（例如，Hamming code、Reed-Solomon、Turbo codes、LDPC）添加足够的冗余，使得接收方能够自动检测 **并纠正** 一定数量的错误，而无需向发送方反馈。  
   优点：无需重传、固定延迟，适用于实时应用（例如，卫星通信、流媒体、5G/6G 广播信道）。  
   缺点：由于更高冗余，需要更多带宽。

3. **反馈校验 (Feedback Verification / Feedback Check)**  
   这是现代教材中较少强调的类别。它通常指接收方进行错误检测并向发送方发送验证信息（例如，ACK/NACK 或部分反馈）的机制。发送方随后决定是否重传或调整编码。  
   在一些中文教育材料中，它被单独列出，但实践中往往与 ARQ 或混合方案重叠。它强调反馈信道在验证中的作用，而非单纯的重传请求。

4. **检错丢弃 (Error Detection with Discard)**  
   发送方仅添加错误检测能力。接收方检查数据：如果正确，则接受；如果检测到任何错误，则静默丢弃整个帧/分组。没有重传或反馈。  
   这是一种简单的方法，常见于偶尔分组丢失可容忍的应用（例如，基于 UDP 的实时音频/视频流媒体、一些局域网协议如基本 Ethernet 无上层恢复）。

其中，**检错重发 (ARQ)** 和 **前向纠错 (FEC)** 是现代系统中两种主导的基本类别。许多实际实现使用 **Hybrid ARQ (HARQ)**，它结合 FEC（用于初始纠错）和 ARQ（当纠错失败时重传），如 4G/5G 移动网络中所见。

这些方法根据应用需求在可靠性、吞吐量、延迟和带宽使用之间进行权衡。

参考文献：  

- [https://zhuanlan.zhihu.com/p/612162113](https://zhuanlan.zhihu.com/p/612162113)
- [https://en.wikipedia.org/wiki/Error_detection_and_correction](https://en.wikipedia.org/wiki/Error_detection_and_correction)
- [https://www.geeksforgeeks.org/computer-networks/error-control-in-data-link-layer](https://www.geeksforgeeks.org/computer-networks/error-control-in-data-link-layer)