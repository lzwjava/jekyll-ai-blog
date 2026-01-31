---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Firestore NoSQL 数据库指南精要
translated: true
type: note
---

我将为您全面介绍 Firestore，它是 Google Cloud 旗下的旗舰级 NoSQL document database。

## What is Firestore?

Firestore（官方称为 Cloud Firestore）是一款灵活、可扩展的 NoSQL 云端数据库，专为 mobile、web 和 server 开发而设计。它是 Google Cloud Platform 和 Firebase 的一部分，提供 real-time synchronization、offline support 和 automatic scaling。

## Key Characteristics

**Document-oriented structure**：数据存储在 documents 中（类似于 JSON objects），这些 documents 被组织在 collections 中。Documents 包含映射到值的 fields，而 collections 是 documents 的容器。

**Real-time synchronization**：数据的更改会在连接的 clients 之间进行实时同步，这使其成为协作类应用、chat apps 和 live dashboards 的理想选择。

**Offline support**：Mobile 和 web SDKs 会在本地缓存数据，允许您的 app 在离线状态下运行，并在恢复连接时自动同步。

**Serverless and auto-scaling**：无需管理基础设施。Firestore 会自动扩展以处理您的工作负载，从零到数百万并发用户。

## Data Model

层级结构如下：databases 包含 collections，collections 包含 documents，documents 包含 fields 和 subcollections。一个 document 可能如下所示：

```
users (collection)
  └─ user123 (document)
      ├─ name: "Alice"
      ├─ email: "alice@example.com"
      ├─ created: timestamp
      └─ orders (subcollection)
          └─ order456 (document)
              ├─ total: 99.99
              └─ items: [...]
```

Documents 限制为 1MB，并在其所属 collection 中由唯一的 IDs 标识。您可以自动生成 IDs 或指定自定义 IDs。

## Querying

Firestore 支持强大的 queries，包括 filtering、ordering 和 pagination。您可以链式调用多个 where 子句，但 compound queries 需要 composite indexes。默认情况下，Queries 是浅层的（shallow）——它们不会自动检索 subcollections。

## Pricing Model

您按照三个维度的使用量付费：document 的 reads、writes 和 deletes（按操作次数）、存储的数据（按 GB/month）以及 network egress。它为初学者提供了一个丰厚的 free tier。Real-time listeners 在连接时计为一次 read，并在每次 document 更改时计为一次 read。

## Security

安全性通过 Security Rules 强制执行——这是一种声明式语言，用于在 document 级别控制 read/write 权限。Rules 可以验证数据结构、检查 authentication 状态并实现复杂的 authorization 逻辑。它们在 Google 的服务器上运行，而不是在您的应用程序代码中。

## When to Use Firestore

Firestore 在 real-time applications、需要 offline support 的 mobile apps、快速原型开发以及具有不可预测扩展需求的应用程序中表现出色。当您需要 serverless 架构或在 Firebase 生态系统上构建时，它尤其强大。

然而，对于具有大量 joins 的复杂关系型数据、需要跨多个 documents 执行完整 ACID transactions 的应用、繁重的 analytical 工作负载（此时请考虑 BigQuery），或者当您需要关系型数据库处理得更好的极其复杂的 querying patterns 时，它可能不是理想选择。

## Getting Started

您可以通过 Firebase SDK（用于 mobile/web apps）或 Google Cloud client libraries（用于 server 应用程序）访问 Firestore。Firebase Console 和 Google Cloud Console 都提供了用于管理数据库、查看数据和监控使用情况的界面。

您是否希望我深入探讨某个特定方面，例如 security rules、query patterns 或集成示例？