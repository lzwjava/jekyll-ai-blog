---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GreptimeDB：统一时序数据库
translated: true
type: note
---

### GreptimeDB 概述

GreptimeDB 是一款开源、云原生、分布式的时序数据库，主要面向可观测性数据（包括指标、日志和追踪数据）设计。它将这三类数据统一存储在单一数据库中，支持在 PB 级数据规模下实现亚秒级查询响应的实时洞察。该数据库能够高效处理高基数数据，支持通过 SQL、PromQL 及流式处理进行查询。GreptimeDB 针对物联网、边缘计算和云环境进行了优化，并可无缝集成 Prometheus、OpenTelemetry 和 Grafana 等工具。

### 基础设施架构

GreptimeDB 采用云原生架构，实现了计算与存储分离，通过利用对象存储（如 AWS S3 或 Azure Blob）进行数据持久化，实现了弹性扩展和成本效益。相较于传统块存储，该设计将存储成本降低了 3-5 倍，同时通过缓存和列式格式等优化保持高性能。

核心组件包括：

- **Metasrv**：中央元数据服务器，负责管理数据库模式、表信息和数据分布（分片）。它监控数据节点健康状况、更新路由表并确保集群可靠性。在集群模式下，至少需要三个节点以保证高可用性。
- **Frontend**：无状态层，处理传入请求，执行身份验证，将协议（如 MySQL、PostgreSQL、REST API）转换为内部 gRPC，并根据 Metasrv 的指导将查询路由到数据节点。该层可水平扩展以应对增加的负载。
- **Datanodes**：负责存储和处理数据区域（分片）。它们执行读写操作、管理本地缓存并返回结果。数据持久化存储在对象存储中，以确保持久性和可扩展性。

交互流程：请求通过前端进入，前端查询 Metasrv 获取路由信息，然后将请求转发到相关数据节点进行处理和响应。该架构支持独立模式（所有组件集成在一个二进制文件中，适用于本地或嵌入式使用）或集群模式（适用于生产环境的 Kubernetes 友好模式）。

存储细节：GreptimeDB 使用针对时序数据定制的日志结构合并树（LSM），并通过预写日志（WAL）确保持久性。数据按时间分区，以 Parquet 格式压缩，并缓存在多层系统中（写缓存处理近期数据，具有 LRU 淘汰策略的读缓存处理历史数据，以及元数据缓存）。这有效缓解了对象存储的延迟问题，实现了热数据的亚毫秒级低延迟查询，并通过预取机制高效处理冷数据。可靠性特性包括多副本存储、校验和及跨区域复制。

### 技术栈与产品服务

- **采用 Rust 编写**：是的，整个数据库使用 Rust 实现，以获得高性能、内存安全性和效率。它利用 Apache DataFusion 和 Arrow 等库进行向量化执行和并行处理，并通过 SIMD 指令优化 CPU 使用。
- **GitHub 开源**：完全开源，基于 Apache 2.0 许可证，托管在 <https://github.com/GreptimeTeam/greptimedb。截至> 2025 年，项目处于测试阶段，预计 2025 年中正式发布。项目积极维护，定期发布版本（如 2025 年 4 月的 v0.14），重点关注全文索引和双引擎支持等功能。社区参与活跃，包括外部贡献者，并已被早期采用者用于生产环境。
- **GreptimeDB Cloud**：基于开源核心构建的全托管无服务器云服务，提供按需付费、自动扩展和零运维负担。它提供企业级功能，如增强安全性、高可用性和专业支持，同时支持多云对象存储。云版本与开源版本的关系在于将其扩展至大规模、业务关键型用例，并保持统一的 API 以便轻松迁移。

### 创新与工作质量

GreptimeDB 在可观测性领域具有创新性，它将指标、日志和追踪数据统一到一个数据库中，减少了传统多工具栈（如 Prometheus + Loki + Jaeger 的组合）的复杂性。其计算存储分离架构在 Kubernetes 环境中实现了“无限扩展”，能够处理大规模基数而不会降低性能，并通过对象存储集成和智能缓存将运营/存储成本降低高达 50 倍。Rust 实现带来了卓越的可靠性和速度，基准测试显示其表现优于竞争对手：在 ClickHouse 的 JSONBench 中冷启动排名第一、热启动排名第四，在摄入吞吐量、查询延迟和资源效率方面优于 InfluxDB、Elasticsearch 和 Grafana Mimir（例如在 TSBS 测试中快 6 倍）。丰富的索引（倒排、全文、向量）和原生 OpenTelemetry 支持等功能进一步增强了其在实时物联网和监控场景中的优势。

总体而言，团队表现出色：该项目从 2022 年的新参与者成长为具有实际应用案例的稳健解决方案（如在 Poizon 用于可观测性，在 OB Cloud 用于日志管理）。积极的开发、积极的社区反馈和强劲的基准测试结果表明，其工程专注于性能、成本和可用性，质量很高。尽管仍处于测试阶段，但其发展轨迹表明它有望在云原生数据库领域产生更广泛的影响。

[Greptime 官网](https://greptime.com/)
[GreptimeDB 文档 - 架构](https://docs.greptime.com/user-guide/concepts/architecture)
[GreptimeDB GitHub 仓库](https://github.com/GreptimeTeam/greptimedb)
[GreptimeDB 存储架构深度解析](https://greptime.com/blogs/2025-03-26-greptimedb-storage-architecture)
[GreptimeDB 与竞争对手基准测试](https://medium.com/@greptime/comprehensive-benchmark-report-how-greptimedb-stacks-up-against-influxdb-elasticsearch-69ce97cf6acb)
[GreptimeDB v0.14 发布](https://greptime.com/blogs/2025-04-27-greptimedb-version-released-index-flow-trace)
[Poizon 的可观测性扩展实践](https://medium.com/@greptime/scaling-observability-at-poizon-building-a-cost-effective-and-real-time-monitoring-architecture-07a42e217c02)
