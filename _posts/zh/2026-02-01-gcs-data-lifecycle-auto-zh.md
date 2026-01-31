---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 利用生命周期规则自动管理 GCS 数据
translated: true
type: note
---

Google Cloud 中的 Lifecycle management policies 帮助您更高效地管理数据，根据您定义的条件在 storage classes 之间转换对象或删除对象。这主要用于 **Google Cloud Storage (GCS)**，以优化成本并保持数据整洁。

## Key Concepts

**Object Lifecycle Management** 允许您设置规则，当满足某些条件时自动对对象执行操作。两个主要操作是：

- **Delete** - 永久删除对象
- **SetStorageClass** - 将对象转换到不同的 storage classes（例如从 Standard 移动到 Nearline、Coldline 或 Archive）

## Common Use Cases

您可以使用 lifecycle policies 来：

- 90 天后删除旧的 log files
- 30 天后将不经常访问的数据移动到更便宜的 storage classes
- 7 天后删除不完整的 multipart uploads
- 将超过 1 年的数据存档到 Archive storage class

## How Conditions Work

Lifecycle rules 基于以下条件触发：

- **Age** - 对象创建后的天数
- **CreatedBefore** - 特定日期
- **IsLive** - 是否为当前版本（用于启用了 versioning 的 buckets）
- **MatchesStorageClass** - 当前的 storage class
- **NumberOfNewerVersions** - 用于版本控制
- **DaysSinceNoncurrentTime** - 用于非当前版本

## Basic Example

一个简单的 lifecycle policy 在 JSON 中可能如下所示：

```json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 365}
      }
    ]
  }
}
```

这会删除早于 365 天的对象。

Lifecycle policies 每天评估一次，更改通常在 24 小时内生效。它们是自动化存储管理和降低成本的一种强大方式，无需人工干预。

您想了解更多关于设置特定策略或不同场景的最佳实践吗？