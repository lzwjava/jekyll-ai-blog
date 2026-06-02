---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 理想汽车 GreptimeDB 部署范围
translated: true
type: note
---

问题：所有理想汽车都使用 GreptimeDB 吗？

回答：

不，并非每辆理想汽车都使用 GreptimeDB。

理想汽车（Li Auto）自2023年起与 Greptime 合作，并在其部分智能驾驶和座舱数据系统中部署了 GreptimeDB，尤其是在较新的车型（L系列和MEGA）中用于时序数据存储和实时分析。GreptimeDB 主要应用于理想汽车的云端数据平台和部分车端遥测场景。

然而：

- 旧款车型（理想ONE、2023年中之前发布的L9/L8/L7）不使用 GreptimeDB，因为合作和大规模部署是在此之后才开始的。
- 即使在新车型中，GreptimeDB 也主要用于特定的时序工作负载（ADAS数据、座舱遥测等），而不是作为车内所有系统的唯一或通用数据库。
- 根据不同的使用场景，许多其他数据库和存储系统（Redis、MySQL、ClickHouse等）仍然并行使用。

因此，尽管 GreptimeDB 已成为理想汽车数据基础设施的重要组成部分，并部署在其最新车型中，但它并未用于生产过的每一辆理想汽车。

参考资料：

- Greptime 官方博客 (2024): “GreptimeDB Powers Li Auto Intelligent Driving Data Platform”
- 理想汽车与 Greptime 在 ApacheCon Asia 2024 上的联合演讲
- GreptimeDB GitHub 案例研究和理想汽车工程分享会 (2023–2025)
