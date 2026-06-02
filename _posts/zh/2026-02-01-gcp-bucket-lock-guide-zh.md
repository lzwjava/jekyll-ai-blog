---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Google Cloud 存储桶锁定详解
translated: true
type: note
---

我将搜索有关 Google Cloud 中 Bucket Lock 功能的最新信息。

# Google Cloud Bucket Lock: 全面介绍

Google Cloud 的 Bucket Lock 是 Cloud Storage 的一项强大功能，允许你强制执行数据 Retention policies 并确保符合合规性。以下是你需要了解的内容：

## 什么是 Bucket Lock？

Bucket Lock 允许你配置 Retention policy，该策略规定了 Bucket 中的对象必须保留多长时间，并允许你锁定此策略以永久防止其被缩减或删除。这在 Google Cloud Storage 上创建了 Immutable storage，对于满足监管要求特别有价值。

## 核心概念

**Retention Policy**: 当你在 Bucket 上设置 Retention policy 时，只有当对象的存在时间大于保留期时，才能删除或替换该对象。该策略追溯适用于所有现有对象，并自动覆盖添加到 Bucket 中的任何新对象。

**Locking the Policy**: 这是 Bucket Lock 的关键点。当你锁定 Retention policy 时，该操作是**不可逆的**。一旦锁定，你将无法删除策略或缩减保留期。如有需要，你只能增加保留期。

## 工作原理

具有 Retention policy 的 Bucket 中的每个对象在其 Metadata 中都有一个 Retention expiration date。Bucket 的 Retention policy 还包括一个生效时间（Effective time），在此时间之后，所有对象都保证符合保留期要求。

在锁定之前，你可以自由修改或删除 Retention policy。锁定之后，你“删除”策略的唯一选择是等待每个对象都满足其保留期，然后删除整个 Bucket。如果 Bucket 包含任何未满足保留要求的对象，你无法删除具有锁定策略的 Bucket。

## Regulatory Compliance

配合 Detailed audit logging 模式，Bucket Lock 可以帮助满足 FINRA、SEC 和 CFTC 相关的监管和合规要求，并有助于解决医疗保健行业的某些保留规定。

## 额外的保护功能

除了基础的 Retention policies，Google Cloud Storage 还提供补充功能：

- **Temporary holds**: 你可以对单个对象设置临时持有，以防止在释放持有之前被删除。
- **Event-based holds**: 这些功能会延迟 Retention policy 的倒计时，直到特定事件发生（例如贷款结清），此时保留期才开始计算。

## 重要注意事项

当你锁定 Retention policy 时，Cloud Storage 会自动对包含该 Bucket 的 Project 的 projects.delete 权限应用 Lien，防止在 Lien 存在期间删除 Project。

即使对象本身受 Retention policy 保护，其 Object metadata 仍然可以编辑。该策略还支持 Object Versioning，保护 Bucket 中对象的所有版本。

## Bucket Lock vs Object Retention Lock

值得注意的是，Google Cloud 还提供 Object Retention Lock，它允许你按对象定义数据保留要求，而 Bucket Lock 则统一适用于 Bucket 中的所有对象。

当你需要对 Bucket 中的所有数据执行一致的保留要求时，Bucket Lock 是理想的选择，这使其特别适用于 Log buckets、财务记录或任何对整个数据集有统一合规要求的场景。
