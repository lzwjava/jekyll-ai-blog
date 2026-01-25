---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Storage IAM 角色
translated: true
type: note
---

Question: What roles can we configure in Google Cloud Storage? For example, Storage Object Viewer IAM role, etc.

Answer: 

Google Cloud Storage 使用 **Identity and Access Management (IAM)** 来控制对 bucket 和 object 的访问。您可以在 project 级别、bucket 级别或（针对细粒度访问）object 级别分配 **predefined roles**（Google 管理）和 **custom roles**。

以下是专属于 Cloud Storage 的主要 **predefined IAM roles**：

- **Storage Object Viewer** (`roles/storage.objectViewer`)  
  授予对 object 及其 metadata（不包括 ACLs）的只读访问权限。  
  允许列出 bucket 中的 object (`storage.objects.list`) 以及读取 object 数据/metadata (`storage.objects.get`)。  
  **不**允许查看或列出 bucket 本身。

- **Storage Object Creator** (`roles/storage.objectCreator`)  
  允许创建 object (`storage.objects.create`)，但不能读取、删除或覆盖现有 object。

- **Storage Object Admin** (`roles/storage.objectAdmin`)  
  对 object 的完全控制权：创建、列出、获取、删除和更新 object 及其 metadata（但不包括 bucket 级别的配置）。

- **Storage Legacy Bucket Reader** (`roles/storage.legacyBucketReader`)  
  对 bucket metadata 的只读访问权限以及列出 object 的能力。

- **Storage Legacy Bucket Writer** (`roles/storage.legacyBucketWriter`)  
  授予读取 + 创建/删除 object 的权限（相当于遗留版本的 object admin 加上部分 bucket 权限）。

- **Storage Legacy Bucket Owner** (`roles/storage.legacyBucketOwner`)  
  对 bucket 及其 object 的完全控制权（legacy owner 角色）。

- **Storage Admin** (`roles/storage.admin`)  
  对 bucket 和 object 的完全控制权：创建/删除 bucket、管理 IAM policies、配置 lifecycle/rules 等。

- **Storage Object Viewer**（已在上方列出 —— 最常用于只读 object 访问）

其他常用于授予 Cloud Storage 权限的更广泛角色：

- **Viewer** (`roles/viewer`) — 对大多数资源的只读访问权限，包括列出 bucket/object。
- **Editor** (`roles/editor`) — 对大多数资源的读/写访问权限（包括大部分 Storage 权限）。
- **Owner** (`roles/owner`) — 对 project 的完全控制权，包括所有 Storage 资源。

**关键提示**：
- 对于大多数现代用例，建议优先选择细粒度的 **object-level roles** (`objectViewer`, `objectCreator`, `objectAdmin`)，而不是 legacy bucket roles。
- 如果 predefined roles 不能完全满足您的需求，您还可以创建 **custom roles**（例如：允许 get + list 但不允许更新 metadata）。
- 权限可以在以下级别授予：
  - Project 级别（影响所有 bucket）
  - Bucket 级别（最常用）
  - 单个 Object 级别（细粒度访问控制）

有关最新且完整的列表（包括每个角色包含的具体权限），请参考 Google Cloud 官方文档。

References:  

- [IAM roles for Cloud Storage](https://docs.cloud.google.com/storage/docs/access-control/iam-roles)
- [Cloud Storage roles and permissions](https://docs.cloud.google.com/iam/docs/roles-permissions/storage)
- [Identity and Access Management for Cloud Storage](https://docs.cloud.google.com/storage/docs/access-control/iam)