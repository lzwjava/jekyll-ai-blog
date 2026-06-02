---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Compute Engine 实例创建角色
translated: true
type: note
---

Question: What is the recommended way to grant a user the ability to create Compute Engine instances in a specific project without giving them broader permissions? A) roles/compute.instanceAdmin B) roles/compute.instanceAdmin.v1 C) roles/editor D) roles/owner

Answer:

正确且**推荐**的答案是 **A) roles/compute.instanceAdmin**。

### Explanation:

- **roles/compute.instanceAdmin**
  这是用于管理 Compute Engine 实例的标准且最常推荐的预定义 IAM role。它包含以下权限：
  - Create, start, stop, delete, 以及 update instances
  - Attach/detach disks
  - 设置 machine type, labels, metadata 等
  - 执行大多数日常的 instance 管理任务

  它的范围有意设计得比 `roles/editor` 或 `roles/owner` 更窄，是当你希望允许 instance 创建和管理，而**不**授予其他 Google Cloud services 广泛权限时的首选。

- **roles/compute.instanceAdmin.v1**
  此角色主要为了 **backward compatibility** 而存在。
  Google 建议在所有新设置中使用 `roles/compute.instanceAdmin`（不带 .v1）。
  `.v1` 后缀用于该角色的早期版本，而无后缀版本是当前的首选角色。

- **roles/editor**
  授予非常广泛的权限 — 允许创建和管理项目中几乎所有的 resources（Cloud Storage, BigQuery, Cloud Functions, networking 等）。
  这**不符合** least-privilege 原则。

- **roles/owner**
  对项目的完全控制权，包括 billing 和 IAM policy 的更改。
  这更严重地违反了 least-privilege 原则。

### Summary – Best Practice (2025/2026)

当你希望让用户在遵循 least-privilege 原则的同时，在项目中创建并完全管理 Compute Engine 实例时，请使用 **roles/compute.instanceAdmin**。

Correct answer: **A**

References:

- [https://cloud.google.com/compute/docs/access/iam](https://cloud.google.com/compute/docs/access/iam)
- [https://cloud.google.com/iam/docs/understanding-roles#compute-engine-roles](https://cloud.google.com/iam/docs/understanding-roles#compute-engine-roles)
