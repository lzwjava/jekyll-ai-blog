---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GreptimeDB 基于 Apache DataFusion
translated: true
type: note
---

GreptimeDB 作为一款面向可观测性数据（如指标、日志和追踪）的开源云原生时序数据库，其查询引擎完全构建于 Apache DataFusion 之上，因此将 DataFusion 作为核心依赖。DataFusion 是一个用 Rust 编写的高性能、可扩展的查询规划、优化与执行框架，通过利用 Apache Arrow 的内存列式数据格式实现高效处理。

### 核心依赖关系的关键原因

- **性能与效率**：DataFusion 借助 Arrow 的零拷贝数据模型实现快速查询执行，该模型能最小化序列化开销并支持向量化操作。这对于 GreptimeDB 在处理海量时序数据时保持高速查询至关重要。

- **可扩展性与定制化**：GreptimeDB 对 DataFusion 进行了时序特化功能扩展，包括：
  - 支持将 PromQL（Prometheus 查询语言）作为可观测性查询方言
  - 针对时序工作负载优化的增强 SQL 语法
  - 与外部二级索引集成以加速查询
  - 在查询各阶段（如规划、重写、执行）应用的领域专用优化规则

- **模块化架构**：DataFusion 作为灵活框架，使 GreptimeDB 能够在其分布式组件（如计算存储分离架构）间协调查询。这种模块化特性有助于构建适应不同场景（实时分析与历史聚合）的定制化查询方案。

- **生态兼容性**：通过继承 DataFusion 的内置函数（标量函数、窗口函数、数组函数等），GreptimeDB 原生具备丰富的 SQL 能力，在减少开发工作量的同时确保与 Apache Arrow 等数据生态的兼容性。

若没有 DataFusion，GreptimeDB 需从零实现完整查询引擎，这将耗费大量资源且难以维护。而依托该依赖项，GreptimeDB 既能加速开发进程，又能提供生产级的查询性能。

[Greptime 工程师夏锐航在 CMUDB 研讨会分享——Apache DataFusion 数据库实践](https://greptime.com/blogs/2024-12-19-apache-datafusion-database-practices)
[函数列表 | GreptimeDB 技术文档](https://docs.greptime.com/reference/sql/functions/overview/)
