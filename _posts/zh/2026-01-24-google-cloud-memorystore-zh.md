---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Memorystore 服务介绍
translated: true
type: note
---

Question: What is an introduction to Memorystore in Google Cloud Platform (GCP)?

Answer: 

Memorystore 是 **Google Cloud 的全托管 in-memory data store 服务**。它提供与流行的开源 in-memory 引擎兼容的实现，让你无需亲自管理服务器、打补丁、备份或设置高可用性（high-availability）即可使用它们。

截至 2025–2026 年，Memorystore 支持两种主要的引擎：

### 1. Memorystore for Redis (包括 Redis Cluster)

- 最原始且应用最广泛的选项
- 与开源 Redis 完全兼容
- 两种部署模式：
  - **Standard Tier**：具有基础 HA（replication）的独立实例
  - **Redis Cluster**：分片的、可扩展的集群模式，具有更高的吞吐量和零停机扩缩容
- 适用于 caching、session stores、leaderboards、real-time analytics、pub/sub messaging、geospatial indexes 等
- 提供亚毫秒级（sub-millisecond）延迟
- 自动故障转移（failover）、监控和扩展

### 2. Memorystore for Valkey

- 在 Redis 许可证变更（2024–2025）后推出的新选项
- 全托管 **Valkey**（由 Linux Foundation 维护的 Redis 7.2.4 开源分支）
- 与 Redis OSS ≤ 7.2 的协议 100% 兼容
- 支持 **Cluster Mode Enabled** 和 **Cluster Mode Disabled**
- 设计为大多数 Redis 工作负载的即插即用替代方案
- 提供与 Memorystore for Redis Cluster 类似的性能、扩展性和 HA 特性
- 许多用户正迁移到基于 Valkey 的 Memorystore 以获得长期的开源兼容性

### 3. Memorystore for Memcached (仍可用但不再是重点)

- 全托管 Memcached
- 更简单的 key-value caching（无 persistence、lists、sets 等）
- 多线程，针对纯 caching 提供极高吞吐量
- 随着 Redis/Valkey 覆盖了绝大多数用例，目前使用频率降低

### Key Benefits of Memorystore (所有变体的共同优势)

- **Fully managed** — 无需 OS 补丁，无需进行 Redis/Valkey 配置调优
- 亚毫秒级延迟 (in-memory)
- 自动 replication 和 failover
- 垂直和水平扩展（在 Cluster 模式下表现尤为强劲）
- VPC-native, private service connect, IAM 集成
- 通过 Cloud Monitoring 和 Cloud Logging 内置监控
- 符合 SOC, ISO, PCI DSS 标准

### When to choose Memorystore

| Use Case                     | Recommended Engine       | Why                              |
|------------------------------|---------------------------|----------------------------------|
| General caching              | Redis 或 Valkey           | 丰富的数据结构                   |
| Session store                | Redis / Valkey            | 快速 + 可选的 persistence        |
| Real-time leaderboards       | Redis / Valkey            | Sorted sets                      |
| Very simple high-throughput cache | Memcached              | 多线程，价格略低                 |
| Need guaranteed open-source fork | Valkey                 | 抵御未来许可证变更的影响         |
| Need > hundreds of GB or extreme throughput | Redis Cluster 或 Valkey Cluster | Sharding                         |

总结：Memorystore 让你在 Google Cloud 上以几乎为零的运维开销获得生产级的 Redis 兼容（或 Memcached）性能。在当今的大多数新项目中，你应该在 **Memorystore for Valkey**（面向未来、开放）或 **Memorystore for Redis Cluster**（如果你需要 Redis 7.2 之后新增的特性或已有 Redis 7.4+ 的依赖）之间做出选择。

References:  

- [Memorystore overview](https://cloud.google.com/memorystore)
- [Memorystore for Redis overview](https://cloud.google.com/memorystore/docs/redis/memorystore-for-redis-overview)
- [Memorystore for Valkey overview](https://cloud.google.com/memorystore/docs/valkey/product-overview)