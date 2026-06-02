---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud 层级根节点
translated: true
type: note
---

Question: Which Google Cloud resource hierarchy level is the root node where billing is attached and Organization Policies are typically enforced? A) Folder B) Project C) Organization D) Resource

Answer:

**正确答案是 C) Organization。**

在 Google Cloud Platform (GCP) 中，resource hierarchy 的结构如下（从上到下）：

- **Organization** → 根节点（仅在您关联了 Google Workspace 或 Cloud Identity 账户时存在）
- **Folders** → Organization 下的可选分组层
- **Projects** → 大多数 Resources 所在的主要层级
- **Resources** → 具体服务（VMs、buckets、databases 等）

**Organization** 层级的关键特性：

- 它是层级结构的**根节点 (root node)**。
- **Billing** 挂载在 Organization 层级（通过与 Organization 关联的 Billing Account）。
- **Organization Policies** (Org Policies) 通常最有效地在 Organization 层级强制执行，因为这会将制约因素应用于其下方的所有 folders、projects 和 resources（除非在下方被覆盖）。
- 大多数核心治理、security 和 compliance 控制都在此处应用。

为什么其他选项不正确：

- **A) Folder**: 可选的分组层；可以拥有 policies，但它不是根节点，且 billing 不挂载在这里。
- **B) Project**: 包含实际的 resources 并可以有自己的 billing（在旧版设置中），但在现代 organizations 中，billing 是在 Organization 层级中心化的。Projects 不是根节点。
- **D) Resource**: 最底层（单个服务）；billing 和 organization policies 都不会挂载在这里。

因此，挂载 billing 且通常强制执行 Organization Policies 的根节点是 **Organization**。

References:

- [Google Cloud Resource Hierarchy Documentation](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy)
- [Organization Policy Overview](https://cloud.google.com/resource-manager/docs/organization-policy/overview)
