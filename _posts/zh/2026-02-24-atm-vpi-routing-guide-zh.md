---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ATM VPI 字段路由详解
translated: true
type: note
---

我会搜索有关 ATM header format 和 VPI field 的信息，为您提供全面解释。问题：ATM header format 中 VPI field 的功能是什么？

答案：

在 ATM (Asynchronous Transfer Mode) cell header format 中，**VPI (Virtual Path Identifier) field 用于 routing selection**，这是正确答案（选项 A）。

## 详细解释

VPI field 与 VCI (Virtual Channel Identifier) field 结合，形成 ATM 网络中的 routing 机制：

**VPI 的功能：**
VCI 与 VPI 一起，用于标识 cell 在通过一系列 ATM switches 前往目的地的过程中下一个目的地。ATM switches 使用 VPI/VCI fields 来标识 cell 通往最终目的地的下一个网络的 virtual channel link (VCL)。

**技术细节：**
- 对于 UNI (User-Network Interface) cells，VPI 为 8 bits，而 NNI (Network-Network Interface) cells 使用 12 bits 的 VPI（因为 4-bit GFC field 被重新用作额外的 VPI bits）
- Virtual Path Identifier (VPI) 标识 ATM 网络中两个位置之间的一条路径，该路径为一群 virtual channels 提供传输，其中 virtual channel 表示两个通信 ATM 设备之间的连接。

**两级层次结构：**
Virtual Channel Identifier (VCI) 可以视为 ATM 使用的两级 routing 层次结构的第二部分，其中一群 virtual channels 用于形成一条 virtual path。

## 其他 ATM Header Fields

作为参考，考试问题中提到的其他 fields 有不同的用途：

- **HEC field** (Header Error Control)：用于错误检测和纠正
- **GFC field** (Generic Flow Control)：用于 flow control
- **CLP field** (Cell Loss Priority)：用于 congestion control

您的答案 **A** 是正确的。

参考资料：

- https://en.wikipedia.org/wiki/Asynchronous_Transfer_Mode
- https://www.sciencedirect.com/topics/computer-science/virtual-path-identifier
- https://www.informit.com/articles/article.aspx?p=680842&seqNum=4
- https://www.ccexpert.us/routing-switchin/atm-cell-format.html