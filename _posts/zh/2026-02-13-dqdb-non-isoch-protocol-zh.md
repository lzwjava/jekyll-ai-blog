---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DQDB非等时协议问答
translated: true
type: note
---

问题：在 DQDB 双总线子网中，规定使用哪种媒体访问控制协议来提供非等时服务（non-isochronous services）？

A. Carrier Sense Multiple Access
B. Pre-arbitrated Access
C. Distributed Queue Access
D. Time Division Multiple Access

你的答案：D
正确答案：C

回答：

**正确答案是 C – Distributed Queue Access (分布式排队访问)**

**解析：**

DQDB (Distributed Queue Dual Bus) 是 IEEE 802.6 定义的城域网 (MAN) 标准。它使用两条单向总线（前向总线和反向总线），旨在同时支持 **isochronous**（时间敏感、恒定比特率）和 **non-isochronous**（异步、可变比特率）流量。

在 DQDB 中，主要有两种媒体访问控制机制：

- **QA (Queued Arbitrated) slots** → 使用 **Distributed Queue Access** 协议
  → 主要用于 **non-isochronous**（无连接、尽力而为、异步）服务，如数据流量、局域网类通信、文件传输等。

- **PA (Pre-Arbitrated) slots** → 使用预分配的固定时隙
  → 主要用于 **isochronous** 服务（恒定比特率、延迟敏感），如语音和视频。

因此：

- 在 DQDB 中提供 **non-isochronous services** 的协议是 **Distributed Queue Access** (分布式排队访问)，对应选项 **C**。

**为什么其他选项不正确：**

- **A. Carrier Sense Multiple Access (CSMA)**
  这是 Ethernet (IEEE 802.3) 中使用的访问方法，而非 DQDB。

- **B. Pre-arbitrated Access**
  这存在于 DQDB 中，但它用于 **isochronous** 服务，而不是 non-isochronous。

- **D. Time Division Multiple Access (TDMA)**
  虽然 DQDB 使用基于时隙的访问（概念上类似于 TDMA），但 DQDB 中针对非等时流量的具体机制名称是 **Distributed Queue Access**，而不仅仅被称为 TDMA。

**总结：**

DQDB 双总线子网 → non-isochronous services → **Distributed Queue Access (QA protocol)** → 正确答案是 **C**。

参考资料：

- IEEE 802.6 standard (DQDB) 文档
- 涵盖 MAN 标准的计算机网络教材（如 Tanenbaum, Kurose & Ross 等）
