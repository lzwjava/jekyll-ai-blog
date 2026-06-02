---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Spanner 概览
translated: true
type: note
---

Question: What is an introduction to Cloud Spanner in Google Cloud?

Answer:

Cloud Spanner 是 **Google Cloud 的全托管、水平可扩展、全球分布式的 relational database service**。它专为关键业务应用设计，在不牺牲 SQL 支持的前提下，提供 **strong consistency**、高可用性以及几乎无限的扩展能力。

### Key Features of Cloud Spanner

- **Global distribution with strong consistency**
  Spanner 在跨地域和跨大洲时提供 **external consistency**（一种非常强的一致性形式），同时保持低延迟的读写操作。

- **Horizontal scalability**
  您可以从几个节点扩展到数千个节点。Compute 和 storage 独立扩展，Spanner 会自动处理 sharding 和 replication。

- **Fully managed**
  无需管理服务器、打补丁、备份、replication 或 failover —— Google 处理所有运维层面。

- **ACID transactions**
  完全支持符合 ACID 标准的事务，即使是跨全球分布的数据。

- **Standard SQL**
  使用带有扩展的 ANSI SQL 2011，兼容大多数适用于 PostgreSQL 或 MySQL 方言的工具和 ORM。

- **Multi-model capabilities（近期演进）**
  除了关系型数据，Spanner 现在还支持在同一个数据库中处理 **graph**、**key-value** 和 **vector search** 工作负载（根据最近的更新）。

- **High availability**
  多区域实例提供 99.999% 的可用性 SLA（五个 9）。

### Main Use Cases

- 需要从多个大洲进行低延迟访问的全球化应用（游戏、金融、电子商务）
- 因规模或一致性需求而超出 MySQL/PostgreSQL 等传统 RDBMS 承载能力的应用程序
- 需要跨区域严格 ACID 保证的金融系统
- 全球规模的实时库存、欺诈检测、个性化推荐
- 以前需要在应用程序代码中编写复杂 sharding 逻辑的工作负载

### Spanner vs Other Google Cloud Databases (Quick Comparison)

| Database       | Consistency     | Scale Style       | Global Replication | Best For                          |
|----------------|-----------------|-------------------|--------------------|-----------------------------------|
| **Cloud Spanner** | Strong         | Horizontal (unlimited) | Native, synchronous | Mission-critical, global apps    |
| **Cloud SQL**     | Strong         | Vertical + read replicas | Regional/multi-regional (async) | Traditional OLTP, smaller scale  |
| **AlloyDB**       | Strong         | Horizontal (cluster) | Regional           | PostgreSQL-compatible, high perf |
| **Bigtable**      | Eventual       | Horizontal        | Multi-regional     | High-throughput NoSQL            |
| **Firestore**     | Strong (per doc) | Serverless       | Multi-region       | Mobile/web apps, real-time       |

### When to Choose Cloud Spanner

当您**同时**需要以下特性时，请选择 Spanner：
- Relational model + SQL
- Global strong consistency
- 极大规模或极高的 transaction throughput
- 关键业务的运行时间保证（Mission-critical uptime）

如果您的工作负载较小、仅限区域性、或者不需要全球范围内的 strong consistency，Cloud SQL 或 AlloyDB 通常更具成本效益。

References:

- [Cloud Spanner Official Page](https://cloud.google.com/spanner)
- [Spanner Documentation Overview](https://docs.cloud.google.com/spanner/docs)
- [Google Research Paper on Spanner (2012)](https://research.google.com/archive/spanner-osdi2012.pdf)
