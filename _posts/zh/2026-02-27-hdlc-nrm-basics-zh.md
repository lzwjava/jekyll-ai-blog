---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HDLC 正常响应模式基础
translated: true
type: note
---

问题：在 HDLC 中，由 **primary station**（主站）发起传输过程，且 **secondary station**（从站）只能在接收到主站的命令帧后作为响应向主站发送信息的操作模式称为什么？

A. Normal Response Mode (NRM)
B. Asynchronous Response Mode (ARM)
C. Asynchronous Balanced Mode (ABM)
D. Synchronous Balanced Mode

您的答案：B
正确答案：A

答案：

正确答案是 **A. 正常响应模式 (Normal Response Mode, NRM)**。

### 解释

HDLC 定义了三种主要操作模式：

- **Normal Response Mode (NRM)**
  这是一种 **master-slave**（主从，不平衡）配置。
  - 只有 **primary station**（主站）可以发起传输。
  - **secondary station**（从站）在接收到主站的命令帧（通常 P/F 位设置为 poll 轮询）之前，不允许发送任何内容。
  - 被轮询后，从站可以发送一个或多个响应帧（最后一个帧设置 F 位）。
  - 主站完全负责链路管理、轮询、超时、重传和错误恢复。
  → 这完全符合问题中的描述。

- **Asynchronous Response Mode (ARM)**
  这仍然是不平衡的（主站 + 从站），但 **secondary station**（从站）可以随时发送帧，而无需等待主站的许可（即可以异步发起传输）。
  → 这**不是**问题中描述的模式。

- **Asynchronous Balanced Mode (ABM)**
  这是一种 **balanced**（平衡）配置（双方均为 combined stations 组合站）。
  任一站都可以随时发起传输，而无需其他方的许可。
  → 与描述的行为明显不同。

- **Synchronous Balanced Mode**
  该术语不是标准的 HDLC 模式（官方 HDLC 标准中不存在）。

因此，所描述的场景——**仅由主站启动传输**，且**从站只能在接收命令后响应**——正是 **Normal Response Mode (NRM)** 的定义。

您的错误：您选择了 **B (Asynchronous Response Mode)**，这是相反的情况——从站允许在未被轮询前发起传输。

参考资料：

- HDLC 协议规范 (ISO 13239 / ITU-T Recommendation X.25 LAPB 文档)
- 大多数涵盖数据链路层协议的计算机网络教科书（例如 Tanenbaum、Kurose & Ross、Forouzan）
