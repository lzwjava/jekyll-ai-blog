---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Google Cloud API Gateway 基础知识
translated: true
type: note
---

Cloud Endpoints 是 Google Cloud 的 API 管理系统，可帮助您开发、部署、保护和监控 API。它作为一个分布式的 API gateway，部署在您的 backend 服务的各个前端。

## What Cloud Endpoints Does

Cloud Endpoints 提供了一套工具和服务，用于管理 API 的整个生命周期。当您使用 Endpoints 部署 API 时，无需编写基础架构代码即可获得 authentication、monitoring、logging 和 API key validation 功能。

该服务的工作方式是在您的 API 旁边部署一个 proxy（基于 Envoy 或 Extensible Service Proxy）。此 proxy 会拦截传入的请求，根据您的配置对其进行验证，并将合法请求转发到您的 backend。

## Key Features

**Authentication and Security**：Endpoints 支持多种 authentication 方法，包括 API keys、JSON Web Tokens (JWT)、Firebase Authentication、Auth0 和 Google authentication。您可以定义不同的 API 方法需要哪些 authentication 方式。

**API Management**：您可以使用 OpenAPI 规范（针对 REST APIs）或 gRPC 服务定义来定义 API 界面。Endpoints 利用这些规范来验证传入的请求，并生成 client libraries 和文档。

**Monitoring and Logging**：与 Cloud Monitoring 和 Cloud Logging 的集成让您可以深入了解 API 流量、latency、错误率和其他 metrics。您可以查看哪些方法被调用最频繁，跟踪一段时间内的性能，并设置 alerts。

**Rate Limiting and Quotas**：您可以针对每个用户、每个 API key 或全局设置 API 使用 quotas。这可以防止您的 backend 过载，并允许您实现分层服务级别。

**Developer Portal**：Endpoints 可以生成一个 developer portal，API 使用者可以在其中探索您的 API 文档、交互式地尝试各种方法并管理他们的 API keys。

## Supported Platforms

Cloud Endpoints 支持多个 Google Cloud 计算平台：

- **App Engine**：与 standard 和 flexible 环境紧密集成
- **Cloud Run**：部署具有 automatic scaling 功能的容器化 APIs
- **Google Kubernetes Engine (GKE)**：在 Kubernetes 集群中运行 APIs
- **Compute Engine**：在 virtual machines 上部署

您还可以使用 Endpoints OpenAPI 来管理运行在 Google Cloud 之外的 APIs，尽管存在一些限制。

## API Types

**Cloud Endpoints for OpenAPI**：管理使用 OpenAPI 规范（2.0 或 3.0 版本）定义的 REST APIs。这是最灵活的选项，且支持跨平台工作。

**Cloud Endpoints for gRPC**：专为 gRPC APIs 设计，使用 protocol buffers 进行服务定义。这为 service-to-service 通信提供了更好的性能。

**Cloud Endpoints Frameworks**：针对 App Engine 上 Python 和 Java APIs 的旧版选项，使用 annotations 而不是单独的配置文件。Google 建议新项目迁移到 OpenAPI 或 gRPC 选项。

## How It Works

典型的流程包括定义您的 API 规范，将其部署到 Endpoints，然后部署配置为与 Endpoints proxy 配合工作的 backend 服务。当 client 发起请求时，proxy 会验证 authentication、检查 quotas、记录请求日志，并在一切正常的情况下将其转发给您的 backend。backend 处理请求并通过 proxy 将 response 返回给 client。

配置是 versioned（版本化）的，因此您可以部署新版本的 API 配置，并在需要时回滚。API 配置与 backend 实现之间的解耦使您在管理和演进 API 时具有很大的灵活性。

## Pricing

Cloud Endpoints 本身不单独收费——您只需支付底层基础架构的费用（例如运行 API 和 proxy 的计算资源），并根据生成的日志和 metrics 数量支付 Cloud Logging 和 Cloud Monitoring 的标准费用。

这使得 Endpoints 与第三方 API 管理解决方案相比特别具有吸引力，因为您主要是在为您已经使用的资源付费，而不是在云账单中增加一项显著的新支出。