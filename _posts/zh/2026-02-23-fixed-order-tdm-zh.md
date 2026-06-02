---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 固定顺序时分复用
translated: true
type: note
---

在 time-division multiplexing 中，哪种类型以按照 **fixed order** 为各种信号分配 time slots 为特征？

Answer:

那种按照 **fixed order** 为各种信号分配 time slots 的 time-division multiplexing 类型称为 **Synchronous Time-Division Multiplexing (STDM)**。

### 解释

- **Synchronous TDM**：
  - Time slots 以 round-robin 方式预先分配给每个 input channel，无论该 channel 是否有数据要发送。
  - 传输顺序固定且可预测。
  - 如果 channel 没有数据，其 time slot 将保持为空，可能导致低效。
  - 常用于传统电话系统（例如，T1/E1 lines）。

- **Asynchronous TDM**（也称为 **Statistical TDM**）：
  - Time slots 根据需求动态分配。
  - 只有活跃的 channels 获得 time slots，从而提高带宽效率。
  - 顺序不是固定的；取决于哪些 channels 有数据准备传输。

由于问题指定了“按照 fixed order 分配 time slots”，正确答案是 **Synchronous Time-Division Multiplexing**。

References:

- [Time-division multiplexing - Wikipedia](https://en.wikipedia.org/wiki/Time-division_multiplexing)
