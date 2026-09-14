---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 差分曼彻斯特编码规则详解
translated: true
type: note
---

**问题：** Differential Manchester Encoding（差分曼彻斯特码）的编码规则是什么？

**回答：**

Differential Manchester Encoding 是一种自同步线路编码，其中每个 bit 周期被分成两半。关键规则如下：

**时钟脉冲（bit 中间跳变）：** 每个 bit 周期在**中间**都有一个强制跳变——这提供了时钟同步，并且无论 bit 值如何都存在。

**bit 编码（bit 起始处跳变）：**

- **bit 0：** 在 bit 周期开始处**有**跳变。
- **bit 1：** 在 bit 周期开始处**没有**跳变。

实际的信号电平无关紧要——重要的是是否发生跳变。bit 中间的跳变总是发生。

简要总结规则如下：

| 情况 | bit 起始处是否有跳变？ | bit 中间处是否有跳变？ |
| --- | --- | --- |
| bit = **0** | ✅ 是（总是） | ✅ 是（总是） |
| bit = **1** | ❌ 否 | ✅ 是（总是） |

**关键优势**：强制性的 bit 中间跳变使得无需单独的时钟线即可实现时钟恢复，并且由于编码基于*跳变*而非绝对信号电平，因此不受极性反转的影响。

---

**参考：**

- [Differential Manchester encoding — Wikipedia](https://en.wikipedia.org/wiki/Differential_Manchester_encoding)
- [Data encoding techniques — Forouzan, Data Communications and Networking](https://www.mheducation.com/highered/product/data-communications-networking-forouzan/M9780073376226.html)
