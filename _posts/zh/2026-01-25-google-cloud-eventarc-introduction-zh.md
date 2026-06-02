---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Eventarc 简介
translated: true
type: note
---

**Question:** 什么是 Google Cloud 中的 Eventarc？

**Answer:**

Eventarc 是 Google Cloud 的全托管服务，用于构建 **event-driven architectures**（事件驱动架构）。它简化了将事件源（event sources）连接到事件消费者（event consumers，如 Cloud Run 服务、Cloud Functions、Workflows 或自定义应用程序）的过程，无需您管理底层基础设施、消息队列或复杂的路由逻辑。

### 核心用途

Eventarc 在 Google Cloud 中提供 **unified eventing experience**（统一的事件体验）。Eventarc 不再需要为每个服务（如 Pub/Sub、Audit Logs、Storage 通知等）使用不同的机制，而是使用开放的 **CloudEvents** 规范对事件传递进行标准化。

### 主要组件

- **Triggers** —— 您创建的核心资源。一个 trigger 定义了：
  - 接收哪些事件（根据事件类型、来源、属性等进行过滤）
  - 发送到哪里（目的地：Cloud Run、Cloud Functions 2nd gen、Workflows、App Engine、GKE 服务、Pub/Sub topic 等）
- **Sources** —— 任何产生事件的对象。Eventarc 支持两大类：
  - **Google events**（由 Google 管理）：Audit Logs、Pub/Sub topics、Cloud Storage 对象更改、Firebase、IoT Core 等 —— 涵盖 60 多个 Google Cloud 服务。
  - **Custom / third-party events**（通过 Publish API）：您可以发送自己符合 CloudEvents 格式的事件（在 **Eventarc Advanced** 中受支持）。
- **Destinations** —— 常见的接收目标包括：
  - Cloud Run 服务（最常见的用例）
  - 2nd generation Cloud Functions
  - Workflows
  - Pub/Sub topics
  - GKE 服务（通过直接传递）
  - 自定义 HTTP 端点（带身份验证）

### 关键特性（截至 2025 年底 / 2026 年初）

- 完全 serverless —— 无需管理服务器或集群
- 具有重试和 dead-letter handling（死信处理）机制的 At-least-once delivery（至少一次传递）
- 在 trigger 级别进行过滤（按事件类型、服务名称、资源名称等）
- 支持 CloudEvents 1.0 格式
- **Eventarc Advanced**（高级版）增加了：
  - 用于摄取自定义/第三方事件的 Publish API
  - 更高级的路由和丰富（enrichment）功能
  - 对复杂 microservices 编排的更好支持
- 基于 IAM 的 trigger 和 destination 安全控制
- 全球可用性（在某些配置中支持多区域 trigger）

### 常见用例

- 在以下情况触发 Cloud Run 服务：
  - 文件上传到 Cloud Storage
  - 收到 Pub/Sub 消息
  - Compute Engine VM 状态更改（通过 Audit Logs）
  - 新用户在 Firebase Authentication 中注册
- 构建事件驱动的工作流（例如：图像处理 → 缩放 → 分析 → 存储元数据）
- 使用更灵活的路由取代传统的 Pub/Sub push subscriptions
- 实时响应 Google Cloud 操作（审核日志事件、资源更改）

### 简单流程示例

1. 文件上传到 Cloud Storage bucket → 生成事件
2. Eventarc trigger 过滤 `google.cloud.storage.object.v1.finalized` 事件
3. Eventarc 将 CloudEvent (HTTP POST) 传递给您的 Cloud Run 服务
4. 您的服务处理该事件（例如：创建缩略图）

Eventarc 已成为 Google Cloud 中处理大多数事件驱动模式（特别是针对 Cloud Run 或现代 serverless 工作负载）的推荐方式，取代了许多旧的点对点集成。

如需最新详情，请查看官方文档。

**References:**

- [Eventarc overview](https://docs.cloud.google.com/eventarc/docs/overview)
- [Eventarc documentation](https://docs.cloud.google.com/eventarc/docs)
- [Eventarc Advanced announcement (2025)](https://cloud.google.com/blog/products/application-modernization/eventarc-advanced-orchestrates-complex-microservices-environments)
- [Eventarc: A unified eventing experience (original 2021 announcement)](https://cloud.google.com/blog/topics/developers-practitioners/eventarc-unified-eventing-experience-google-cloud)
