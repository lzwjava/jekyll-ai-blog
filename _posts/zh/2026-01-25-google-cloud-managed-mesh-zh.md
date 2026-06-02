---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud 全托管服务网格
translated: true
type: note
---

**Question:** 什么是 Google Cloud 中的 Cloud Service Mesh？

**Answer:**

Cloud Service Mesh 是 Google Cloud 的**全托管 service mesh** 解决方案。它有助于简化、安全化、观测和管理现代分布式应用程序中 microservices 之间的通信。

### 什么是常规意义上的 service mesh？

service mesh 是一个专用的基础设施层，用于处理 microservices 架构中的 service-to-service 通信。它提供流量路由（traffic routing）、负载均衡（load balancing）、重试（retries）、熔断（circuit breaking）、双向 TLS 加密（mutual TLS encryption）、可观测性（observability，包括 metrics、logs、traces）以及策略执行等功能，且这一切都无需修改应用程序代码。

### Cloud Service Mesh 的特性

Google Cloud Service Mesh（在许多语境下以前被称为 **Anthos Service Mesh**）基于开源项目 **Istio** 构建，但作为由 Google 运营的**托管式** control plane 提供，具有以下关键特征：

- **全托管 control plane** —— Google 负责 Istio control plane 的安装、升级、扩缩容和高可用性（无需亲自管理 istiod）。
- 支持 **GKE**（Google Kubernetes Engine —— 包括 Autopilot 和 Standard 模式）、**Google Compute Engine** VM、**on-premises** Kubernetes 集群以及 multi-cloud/hybrid 环境。
- 两种主要的部署模式：
  - **Managed** —— Google 完全运营 control plane（推荐大多数用户使用）
  - **In-cluster**（自托管） —— 你在集群内部运行 control plane（拥有更多控制权，但运维工作量更大）
- 与 Google Cloud 生态系统深度集成：
  - 用于可观测性的 Cloud Monitoring 和 Cloud Trace
  - Cloud Logging
  - 用于 mTLS 的托管证书和 CA
  - Traffic Director（用于 service discovery 和负载均衡）
  - Google Cloud Armor 和其他安全服务

### 提供核心能力

- **流量管理 (Traffic management)** —— 高级路由、canary/blue-green 部署、故障注入 (fault injection)、超时 (timeouts)、重试、熔断器
- **安全 (Security)** —— 自动双向 TLS (mTLS)、授权策略、请求身份验证、端到端加密
- **可观测性 (Observability)** —— 黄金指标（latency、traffic、errors、saturation）、分布式追踪 (distributed tracing)、服务级仪表板、访问日志
- **策略执行 (Policy enforcement)** —— 速率限制 (rate limiting)、配额和自定义策略

### 何时使用 Cloud Service Mesh

在以下情况（或计划构建时）使用它：

- 运行在 Kubernetes（特别是 GKE）上的 microservices
- 需要在 hybrid/multi-cloud 环境中实现一致的流量控制、强安全性 (mTLS) 和深度可观测性
- 希望避免自行运行 Istio 的运维负担

简而言之：Cloud Service Mesh 是 Google 提供的生产级、低维护成本的方式，旨在为您的 cloud-native 应用程序添加 Istio 风格的 service mesh 能力，并具备强大的 Google Cloud 集成和全球规模的可靠性。

**References:**

- [Cloud Service Mesh - Google Cloud](https://cloud.google.com/products/service-mesh)
- [Cloud Service Mesh overview - Google Cloud Documentation](https://docs.cloud.google.com/service-mesh/docs/overview)
- [Introducing Cloud Service Mesh | Google Cloud Blog (April 2024)](https://cloud.google.com/blog/products/networking/introducing-cloud-service-mesh)
- [Cloud Service Mesh documentation](https://docs.cloud.google.com/service-mesh/docs)
