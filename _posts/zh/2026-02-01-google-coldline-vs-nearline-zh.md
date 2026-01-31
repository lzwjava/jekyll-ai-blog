---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Google Coldline 与 Nearline 详解
translated: true
type: note
---

Google Cloud Storage 提供针对不同访问模式和成本要求而优化的不同 Storage classes。Coldline 和 Nearline 是两种专为低频访问场景设计的 Storage classes，各具特色。

## Storage Class Overview

**Nearline Storage** 专为每月访问次数少于一次的数据而设计。它非常适合数据 Backups、长尾多媒体内容以及仍需偶尔访问的数据 Archiving。

**Coldline Storage** 适用于每季度（90 天）访问次数少于一次的数据。它非常适合 Disaster recovery、Archival storage 以及极少需要检索的合规性数据。

## Key Characteristics

### Nearline Storage

**Pricing Structure**：Nearline 的存储成本低于 Standard storage，但检索成本较高。您需要按每月每 GB 支付存储费用，并在访问数据时支付检索费用。

**Minimum Storage Duration**：30 天。如果您在 30 天之前删除数据，仍将按完整的 30 天计费。

**Access Speed**：Nearline 提供毫秒级的访问时间，与 Standard storage 相同。在需要检索数据时没有延迟。

**Use Cases**：每月 Backups、业务连续性可能需要的数据、偶尔访问的多媒体内容、数据 Analytics pipelines 的 Staging areas。

### Coldline Storage

**Pricing Structure**：Coldline 提供比 Nearline 更低的存储成本，但检索费用更高。与 Standard storage 相比，其存储成本大幅降低。

**Minimum Storage Duration**：90 天。提前删除将产生截至 90 天为止剩余天数的费用。

**Access Speed**：同样提供与其他 Storage classes 相同的毫秒级访问时间。尽管被称为“Cold”，但没有检索延迟。

**Use Cases**：Disaster recovery 文件、合规性档案、用于偶尔分析的历史数据、极少访问的 Cold backups。

## Cost Considerations

这两类存储的经济模式都遵循一个规律：您节省了存储成本，但在检索数据时支付更多费用。这使得它们仅在访问确实不频繁时才具有成本效益。

**Storage Costs**：Coldline < Nearline < Standard

**Retrieval Costs**：Standard < Nearline < Coldline

**Operations Costs**：Nearline 和 Coldline 的单次操作费用（Class A 和 Class B operations）均高于 Standard storage。

## Practical Implementation

您可以在创建 Bucket 或上传 Objects 时设置 Storage class。此外，Object Lifecycle Management 策略可以根据存留时间或其他条件自动在 Storage classes 之间转换 Objects。

例如，您可以配置 Lifecycle policy，在 30 天后将 Standard storage 对象移动到 Nearline，然后在 90 天后移动到 Coldline，从而随着数据变旧和访问频率降低来优化成本。

这两种 Storage classes 都能与所有 Google Cloud Storage 功能无缝集成，包括 Encryption、IAM 权限、Versioning 以及地理冗余选项（Regional、Dual-regional 或 Multi-regional）。

## Choosing Between Nearline and Coldline

该决策主要取决于您的预期访问频率。如果您预计每月访问一次，Nearline 比较合适。对于每季度或更低频的访问，Coldline 则更经济。您还可以结合使用两者，创建分层存储策略，在不同的数据生命周期内优化成本。