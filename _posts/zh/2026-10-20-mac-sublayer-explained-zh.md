---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MAC子层详解
translated: true
type: note
---

问题：在网络中，MAC子层是什么意思？

答案：

**MAC（媒体访问控制）子层**是OSI模型中**数据链路层（第2层）**的下半部分。数据链路层分为两个子层：

```
OSI 第2层 — 数据链路层
┌─────────────────────────────────────┐
│  LLC  （逻辑链路控制）  ← 上层 │
├─────────────────────────────────────┤
│  MAC  （媒体访问控制）  ← 下层 │
└─────────────────────────────────────┘
         ↓
     物理层（第1层）
```

---

### MAC的作用

| 职责 | 描述 |
|---|---|
| **介质访问控制** | 决定设备*何时*允许在共享信道上传输（例如以太网使用CSMA/CD，Wi-Fi使用CSMA/CA） |
| **MAC寻址** | 每个网卡（NIC）有一个唯一的48位硬件地址（例如 `AA:BB:CC:DD:EE:FF`），用于在同一本地网络中标识设备 |
| **帧定界** | 标记数据帧的起始和结束位置 |
| **错误检测** | 附加CRC/FCS校验和以检测传输错误（但不进行纠正） |

---

### 为什么它很重要

如果没有MAC，同一有线/无线信道上的多个设备会同时传输并发生冲突。MAC在硬件层面提供了**交通管制规则**，使得每次只有一台（或正确的）设备进行通信。

---

### 快速示例：以太网 vs Wi-Fi

- **以太网（802.3）** 使用 **CSMA/CD** —— 设备在传输前先侦听；如果检测到冲突，则退避并重试。
- **Wi-Fi（802.11）** 使用 **CSMA/CA** —— 设备在传输前等待信道空闲，以*避免*冲突。

两者都是MAC层机制。

---

参考资料：
- [IEEE 802概述 —— MAC和LLC子层](https://standards.ieee.org/ieee/802/5956/)
- [OSI模型 —— 数据链路层（Cloudflare）](https://www.cloudflare.com/learning/network-layer/what-is-the-network-layer/)
- [介质访问控制 —— 维基百科](https://en.wikipedia.org/wiki/Medium_access_control)