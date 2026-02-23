---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ATM 技术应用与演进
translated: true
type: note
---

我将搜索关于 ATM 技术和其应用的全面信息。

## 问题：

ATM (Asynchronous Transfer Mode) 是什么，它用于什么？

## 答案：

### ATM 是什么？

ATM (Asynchronous Transfer Mode) 是一种电信网络使用的交换技术，它使用异步时分复用来将数据编码成小型固定大小的 cell。它是一种 cell 交换技术，提供电路交换和分组交换网络特征的组合功能。

### 关键特性

**固定 Cell 结构：** 在 ATM 中，基本传输单元是固定长度的 53 octets（bytes）帧，称为 cell，这与 Internet Protocol (IP) 或 Ethernet 等使用可变大小 packet 或 frame 的方法不同。每个 cell 由 5-byte header 和 48-byte payload 组成。

**Virtual Circuits：** ATM 作为基于 channel 的传输层运行，使用 virtual circuits，每个 ATM cell 在其 header 中定义 8-bit 或 12-bit virtual path identifier (VPI) 和 16-bit virtual channel identifier (VCI) 对，以标识 cell 通过一系列 ATM switches 时下一个目的地。

**处理多种流量类型：** ATM 可以处理传统高吞吐量数据流量以及实时低延迟内容，如 telephony（voice）和 video。

### ATM 用于什么？

ATM 有众多应用，包括电信网络，由于其能够在同一网络上传输 voice、video 和 data 的能力而被广泛使用，作为 WAN 的 backbone network，具有高速数据传输能力，以及商业广播，由于其实时传输能力。

**具体应用：**
- 电信用于高速 voice 和 data 传输，企业网络用于安全且可扩展的企业通信，以及 video conferencing 以确保低延迟和高品质 video stream
- ATM 是 public switched telephone network 的 synchronous optical networking 和 synchronous digital hierarchy (SONET/SDH) backbone 以及 Integrated Services Digital Network (ISDN) 中的核心 protocol

### 优势

ATM 提供独特特性，包括固定大小 cell 确保统一数据传输、低延迟最小化数据传输延迟、高可靠性提供一致性能、可扩展性轻松适应不断增长的网络需求，以及 quality of service 保证不同类型流量的性能。

### 现代状态

ATM 在 1990 年代被视为 Ethernet 和承载 IP 流量的网络的竞争者，因为它更快，并且不像 Ethernet 那样设计时考虑了 quality-of-service，但一旦 Ethernet 达到 1 gigabit per second 的速度，它就失宠了。ATM 是 SONET/SDH backbone 的核心 protocol，但已大部分被基于 IP 技术的下一代网络取代。

---

## 参考文献：

- [https://en.wikipedia.org/wiki/Asynchronous_Transfer_Mode](https://en.wikipedia.org/wiki/Asynchronous_Transfer_Mode)
- [https://www.gartner.com/en/information-technology/glossary/atm-asynchronous-transfer-mode](https://www.gartner.com/en/information-technology/glossary/atm-asynchronous-transfer-mode)
- [https://www.geeksforgeeks.org/computer-networks/asynchronous-transfer-mode-atm-in-computer-network/](https://www.geeksforgeeks.org/computer-networks/asynchronous-transfer-mode-atm-in-computer-network/)
- [https://lightyear.ai/tips/what-is-asynchronous-transfer-mode](https://lightyear.ai/tips/what-is-asynchronous-transfer-mode)
- [https://www.ninjaone.com/it-hub/it-service-management/what-is-asynchronous-transfer-mode-atm/](https://www.ninjaone.com/it-hub/it-service-management/what-is-asynchronous-transfer-mode-atm/)
- [https://www.nfon.com/en/get-started/cloud-telephony/lexicon/knowledge-base-detail/atm/](https://www.nfon.com/en/get-started/cloud-telephony/lexicon/knowledge-base-detail/atm/)
- [https://www.dialogic.com/glossary/asynchronous-transfer-mode-atm](https://www.dialogic.com/glossary/asynchronous-transfer-mode-atm)