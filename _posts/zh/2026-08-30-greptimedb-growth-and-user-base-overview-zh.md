---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GreptimeDB 增长与用户基础概览
translated: true
type: note
---

**问题：** GreptimeDB 近年来增长如何？是否有大量用户基础？

**回答：**

GreptimeDB 自开源以来展现了稳健且持续的增长。以下是关键维度的概述：

**时间线与里程碑**

GreptimeDB 自 2022 年 11 月 15 日开源以来持续稳步发展，项目迭代迅速：

- v1.0 GA 原计划于 2026 年 1 月 10 日发布，目标是冻结 API 和协议以确保长期兼容性。
- v1.0.0 于 2026 年 4 月 8 日正式发布——这是他们的首个 GA 版本。
- v1.1.0 于 2026 年 6 月 14 日发布，被描述为继 v1.0 GA 之后又一个面向生产的版本。
- v1.2.0 beta 已在进行中，重点聚焦更安全的表管理、更好的 Flow 可观测性以及查询/存储正确性修复。

**GitHub 与社区**

截至 2025 年初至年中，主 GitHub 仓库已积累约 6,000–6,400 颗星，拥有 457 个 fork。对于一个专注于时序/可观测性的数据库而言，这是相当可观的数量，但远不及 InfluxDB 或 ClickHouse 等巨头。

从 v1.0 Beta 到 GA 期间，仅合并了 474 个 PR，涉及 27 位贡献者，其中 8 位是首次为 GreptimeDB 做贡献。

**内容与可见度**

2024 年，GreptimeDB 社交媒体账号新增数千粉丝，其表现最佳的文章阅读量超过 10,000 次，被分享超过 300 次。

2025 年，他们发布了 93 篇博客文章，其中“Observability 2.0”相关内容吸引了全年超过一半的流量——反映出可观测性领域的浓厚兴趣。

**产品方向**

GreptimeDB 现在定位为“Observability 2.0”数据库——可作为 Prometheus、Loki 和 Elasticsearch 的直接替代品，或作为单一的 OpenTelemetry 后端。这一更广泛的定位（从纯时序扩展到统一的指标、日志和链路）推动了其近期的可见度提升。

**总体评估**

GreptimeDB 是一个持续发展的项目，拥有活跃的开发者社区，但与 InfluxDB 或 TimescaleDB 相比仍相对小众。它未公开披露具体的用户或客户数量。项目成熟速度很快——经过 3.5 年于 2026 年 4 月达到 v1.0 GA 是一个有意义的信号——但仍在建立企业级采用，而非当前广泛主导的产品。

---

**参考文献：**

- [GreptimeDB 2025 Roadmap Released](https://medium.com/@greptime/greptimedb-2025-roadmap-released-f768cbc7d5e9)
- [GreptimeDB v1.0 GA Is Here](https://www.greptime.com/blogs/2026-04-14-greptimedb-v1-ga-release)
- [Three Years in the Making — v1.0 Highlights](https://www.greptime.com/blogs/2025-11-05-greptimedb-v1-highlights)
- [GreptimeDB v1.1.0 Release](https://www.greptime.com/blogs/2026-06-14-greptimedb-v1-1-0-release)
- [Greptime GitHub Organization](https://github.com/greptimeteam)
