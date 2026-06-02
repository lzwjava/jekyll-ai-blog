---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 为 ChatGPT 用户扩展 PostgreSQL 规模
translated: true
type: note
---

**Question:** <https://openai.com/index/scaling-postgresql/> 上的 OpenAI blog post 说了什么？

**Answer:**

这篇标题为 **"Scaling PostgreSQL to power 800 million ChatGPT users"** 的 blog post 由 OpenAI 发布于 2026 年 1 月 22 日。它描述了 OpenAI 如何扩展单个 unsharded PostgreSQL 数据库（运行在 Azure PostgreSQL Flexible Server 上），以处理 ChatGPT 及其 API 的海量全球流量，支撑了 8 亿用户和每秒数百万次的 queries (QPS)，其中大部分是 read-heavy 负载。

### 文章核心要点

- **实现的规模 (Scale achieved)**
  PostgreSQL 负载在过去一年中增长了 10 倍以上。
  他们运行 **一个 primary instance**（负责所有 writes）+ **近 50 个 read replicas**，分布在多个 regions。
  该架构实现了数百万 QPS、低双位数毫秒级的 p99 latencies、近乎零的 replication lag 以及五个九（99.999%）的 availability。
  在过去的 12 个月中仅发生过 **一次 SEV-0 incident**（由 ChatGPT ImageGen 发布期间 1 亿新用户涌入导致的 10 倍 write 浪涌引起）。

- **核心架构决策**
  - PostgreSQL 数据库本身不进行 sharding（为了避免重写数百个 application endpoints）。
  - Write-heavy 的 workloads 被迁移到像 Azure Cosmos DB 这样的 sharded systems。
  - 新服务从一开始就默认使用 sharded databases。
  - 所有保留在 PostgreSQL 中的用途均为 read-heavy；不再向其添加新表。

- **用于扩展和稳定系统的主要技术**
  - **Read offloading** → 几乎所有的 reads 都流向 replicas；关键的 reads 受到保护以防止冲击 primary。
  - 使用 PgBouncer 进行 **Connection pooling**（将平均 connection time 从 50 ms 降低到 5 ms）。
  - **Aggressive caching** 并配合 cache locking/leasing，以防止 thundering-herd 形式的 cache-miss 冲击数据库。
  - **Multi-layer rate limiting**（应用层、proxy、pooler、query、ORM）并封堵高耗能的 query patterns。
  - **Workload isolation** — 为高优先级和低优先级流量分配独立的 instances。
  - **Query & schema 规范** — 避免昂贵的 joins、多表操作和 full-table rewrites；强制执行严格的 timeouts（例如 schema 变更限制在 5 秒内）。
  - **High availability** — primary 以 HA 模式运行并配备 hot standby；每个 region 拥有多个带容量预留的 replicas。
  - **Cascading replication**（测试中）旨在通过级联方式扩展超过 50 个 replicas，而不会因为 WAL streaming 导致 primary 过载。

- **提到的最大挑战**
  - Write spikes（由 cache misses、新功能发布、backfills 引起）导致单个 primary 过载。
  - 重负载 writes 下的 MVCC 相关问题（bloat、autovacuum 压力、read/write amplification）。
  - Connection exhaustion 和 idle connection storms。
  - WAL streaming 的 CPU/网络开销限制了可添加的 replicas 数量。
  - Noisy neighbors（干扰项）和高风险的 schema 变更。

- **结论与未来方向**
  OpenAI 证明了，通过精细的工程手段（replicas、caching、rate limiting、workload migration）进行优化后，PostgreSQL 可以在不进行 sharding 的情况下，可靠地处理远超通常认知的 read-heavy 巨量负载。
  他们计划继续将剩余的 write-heavy 部分从 PostgreSQL 中迁出，并在 production 环境中启用 cascading replication。

简而言之，这篇文章是一篇工程深度解析，展示了传统的 single-primary + many-replicas PostgreSQL 架构在经过深度优化后，能够支撑起像 ChatGPT 这种全球规模的 AI 产品。

**References:**

- [Scaling PostgreSQL to power 800 million ChatGPT users](https://openai.com/index/scaling-postgresql/)
