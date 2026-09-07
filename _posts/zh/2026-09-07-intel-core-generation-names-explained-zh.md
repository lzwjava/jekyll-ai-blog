---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英特尔酷睿处理器代际名称详解
translated: true
type: note
---

Question: 英特尔第12、13、14代处理器名称的含义是什么？

Answer:

这些“代”标签指的是英特尔的 **Core 处理器系列**，每一代都基于特定的微架构和制造工艺：

| 代 | 代号 | 架构 | 制程节点 | 发布年份 |
|-----|----------|-------------|--------------|-------------|
| 第12代 | Alder Lake | Hybrid（P+E 核心） | Intel 7（10nm） | 2021 |
| 第13代 | Raptor Lake | Hybrid（P+E 核心） | Intel 7（10nm） | 2022 |
| 第14代 | Raptor Lake Refresh | Hybrid（P+E 核心） | Intel 7（10nm） | 2023 |

**关键概念：**

- **代数**只是英特尔用来按时间顺序组织产品线的营销标签。数字越大 = 越新。
- **第12代（Alder Lake）** 是一次重大飞跃——它引入了英特尔的 *hybrid 核心设计*，在同一芯片上混合了 **性能核心（P-cores）** 和 **能效核心（E-cores）**，其灵感来自 ARM 的 big.LITTLE 方案。
- **第13代（Raptor Lake）** 对 Alder Lake 进行了改进——更多 E-core、更高时钟频率、相同插槽（LGA1700）。这是一次有意义但属于增量式的升级。
- **第14代（Raptor Lake Refresh）** 本质上就是第13代，只是时钟频率略高并有一些小调整。相同的硅片、相同的插槽、相同的制程节点——与其说是新一代，不如说是改名。这一代还与一些高端 SKU（i9 芯片）上众所周知的 **稳定性/退化问题** 有关。

**如何解读型号**，例如 `Intel Core i7-**13**700K`：
- 破折号后的前两位数字 = 代数（13 = 第13代）
- 其余数字 = SKU 等级
- 后缀字母（K、F、T 等）= 特性（K = 解锁倍频，F = 无集成显卡，等）

参考：
- [Intel Core 处理器世代概述 – Intel ARK](https://ark.intel.com)
- [Alder Lake 架构 – AnandTech](https://www.anandtech.com/show/17047/the-intel-12th-gen-core-i9-12900k-review-hybrid-performance/2)
- [Raptor Lake 对比 Alder Lake – Tom's Hardware](https://www.tomshardware.com/reviews/intel-core-i9-13900k-review)