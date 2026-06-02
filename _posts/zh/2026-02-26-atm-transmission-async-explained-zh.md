---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ATM异步传输详解
translated: true
type: note
---

**问题**：在 ATM 传输模式中，由于包含信息的 cells 不需要在信道上周期性地出现，这种传输模式是 asynchronous 还是 synchronous？

**答案**：

正确答案是 **asynchronous**。

### 解释

**Asynchronous Transfer Mode (ATM)** 的名称正是因为其在 cell 传输时机方面的 **asynchronous** 特性而得名。以下是全面的分析：

1. **此上下文中 Asynchronous 的定义**：
    在传统的 synchronous 传输（如 TDM - Time Division Multiplexing）中，时间槽被预先分配给特定信道。即使信道没有数据要发送，其时间槽仍保持空闲但被保留，并在线路上传输时周期性地出现。

    相比之下，ATM 使用 **statistical multiplexing**。cells 仅在有实际数据要发送时才传输。没有为特定连接分配固定的、周期性的时间槽。包含用户信息的 cell 可以随时出现，来自同一源的 cells 之间的间隙会根据流量负载而变化。

2. **为什么不是 Synchronous**：
    如果传输是 synchronous 的，则属于特定 virtual circuit 的 cells 会以规律、可预测的间隔（周期性地）到达，无论它们携带有效负载数据还是仅为闲置填充。该问题明确指出 cells “不需要周期性地出现”，这是排除 synchronous 传输的定义特征。

3. **ATM 的关键特性**：
    * **Fixed-length cells**：ATM 使用称为 cells 的小型固定大小数据包（53 bytes：5-byte header + 48-byte payload）。
    * **Connection-oriented**：在数据传输前建立 virtual circuit。
    * **Statistical Multiplexing**：带宽根据需求动态分配，导致问题中描述的 cells 非周期性到达。

因此，由于承载信息的 cells 的出现不与每个单独信道的严格、周期性时钟周期绑定，该模式是 **asynchronous**。
