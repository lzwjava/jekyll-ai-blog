---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ATM 信元结构简单讲解
translated: true
type: note
---

我将搜索有关 ATM cell structure 的信息，为您提供全面的解释。## 问题：

ATM (Asynchronous Transfer Mode) 的固定 cell length 是什么？cell structure 的组成是什么？

## 答案：

正确答案是 **C: 53 bytes**。

### ATM Cell Structure Breakdown

ATM cell 总共由 53 bytes 的固定长度组成，包括 5-byte header（包含 cell header 数据）和 48-byte payload（包含用户数据）。

### Detailed Composition

**Header (5 bytes)：** Header 包含关键的路由和控制信息，包括：
- Virtual Path Identifier (VPI) 和 Virtual Channel Identifier (VCI)，它们标识 cell 通过 ATM switches 传输时的下一个目的地
- Payload Type (PT)，指示 cell 是否包含用户数据或控制数据
- Cell Loss Priority (CLP)，指示在遇到极端拥塞时是否应移除该 cell
- Header Error Control (HEC)，仅对 header 的前 4 bytes 进行校验和评估

**Payload (48 bytes)：** 48 bytes 的 payload 可选择性地包含 4-byte ATM adaptation layer 和 44 bytes 的实际数据，或者全部 48 bytes 均为数据，取决于 header 控制字段中的一位。

### Why 53 Bytes?

48-byte payload 是美国提出的 64-byte payload（针对数据传输优化）和欧洲提出的 32-byte payload（针对实时语音应用优化）之间的折衷方案。5-byte header 的选择是因为认为 payload 的 10% 是路由信息可接受的最大开销。

### Key Advantages

53 bytes 的固定 cell 大小实现了快速硬件交换和低抖动，这对于实时应用至关重要，并允许可预测的延迟和最小排队。

---

## 参考文献：

- [https://www.tutorialspoint.com/explain-the-atm-cell-structure-in-computer-network](https://www.tutorialspoint.com/explain-the-atm-cell-structure-in-computer-network)
- [https://en.wikipedia.org/wiki/Asynchronous_Transfer_Mode](https://en.wikipedia.org/wiki/Asynchronous_Transfer_Mode)
- [https://www.sciencedirect.com/topics/computer-science/asynchronous-transfer-mode](https://www.sciencedirect.com/topics/computer-science/asynchronous-transfer-mode)
- [https://www.ou.edu/class/telecomm/lect08_atm_b.htm](https://www.ou.edu/class/telecomm/lect08_atm_b.htm)
- [https://networkencyclopedia.com/cell-in-atm/](https://networkencyclopedia.com/cell-in-atm/)
