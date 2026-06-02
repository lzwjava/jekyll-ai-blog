---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: GCP 云负载均衡简介
translated: true
type: note
---

Question: Google Cloud Platform (GCP) 中的 Cloud Load Balancing 是什么？

Answer:

**Google Cloud Platform (GCP)** 中的 Cloud Load Balancing 是一种全托管、分布式、软件定义的 Load Balancing 服务。它将传入流量分配到多个 Backend 实例（例如 Compute Engine VM、Google Kubernetes Engine 集群、Cloud Run 服务或 VM Instance Groups），以确保高可用性、Scalability 和性能。

### 核心特性

- **完全分布式**：使用 Google 的全球 **Anycast IP** 基础设施——同一个 Frontend IP 可以从全球多个 PoP 点发布。
- **无需 Pre-warming**：它可以随流量自动扩展。
- **集成 Health Checking**：自动移除状态异常的 Backend。
- **零停机配置更改**：在大多数情况下生效。
- **Premium Tier**（全球，使用 Google 骨干网）与 **Standard Tier**（区域级，成本较低，但在某些路径上使用公共互联网）。

### 主要 Load Balancers 类型

Google Cloud 提供多种 Load Balancer 类型。两大主要类别是：

1. **Application Load Balancers** (Layer 7 – 内容感知)
   - 理解 HTTP/HTTPS/gRPC/HTTP/2/QUIC 协议
   - 支持 URL maps、基于 Host/Path 的路由、Traffic splitting、基于 Header 的路由等。
   - 子类型：
     - **External Application Load Balancer** (全球) → 面向互联网的 Web/App 的经典选择
     - **Internal Application Load Balancer** (区域) → 用于 VPC 内部的私有流量
     - **Cross-region Internal Application Load Balancer** (更新的，多区域内部 HTTP(S))

2. **Network Load Balancers** (Layer 4 – 基于协议/端口)
   - 以极少的检查透传流量
   - 子类型：
     - **External passthrough Network Load Balancer** (区域) → TCP/UDP/SSL Proxy
     - **Internal passthrough Network Load Balancer** (区域) → VPC 内部的 TCP/UDP
     - **TCP/SSL Proxy Load Balancer** (全球) → 终止 SSL，保留 Client IP

### 快速对比表

| Load Balancer 类型 | 范围 | 层级 | 协议 | 典型用例 | 保留 Client IP |
|---------------------------------|-----------|-------|----------------------------|-------------------------------------------|---------------------|
| External Application            | Global    | L7    | HTTP(S), HTTP/2, gRPC, QUIC| 公共网站, APIs                     | 是 (通过 XFF)      |
| Internal Application            | Regional  | L7    | HTTP(S)                    | 内部微服务                    | 是                 |
| TCP/SSL Proxy                   | Global    | L4    | TCP, SSL                   | 非 HTTP 的全球 TCP/SSL 服务          | 是                 |
| External Passthrough Network    | Regional  | L4    | TCP, UDP                   | 游戏, VoIP, 传统协议            | 是 (直接)        |
| Internal Passthrough Network    | Regional  | L4    | TCP, UDP                   | 内部 TCP/UDP 流量                  | 是 (直接)        |

### 核心组件

- **Frontend** — IP 地址 + 端口 + 协议（入口点）
- **Backend service** — 定义流量如何路由到 Backend + Health checks + Session affinity
- **Backend** — Instance groups, NEGs (Network Endpoint Groups), Cloud Run 等
- **URL map** (仅限 L7) — Host/Path 路由规则
- **Health checks** — 确定 Backend 是否健康
- **Autoscaling** — 与 MIGs (Managed Instance Groups) 无缝协作

### 常见用例

- 将全球用户流量分配到最近的健康实例（低延迟）
- 通过流量拆分进行蓝绿部署和金丝雀发布
- 在 VPC 内安全地暴露内部服务
- 处理突发流量高峰（黑五、产品发布）
- 通过全球外部 Load Balancing 支持混合云/多云设置

Cloud Load Balancing 是主流云提供商中功能最强大且对开发者最友好的 Load Balancing 产品之一，尤其适用于全球化应用。

参考资料：

- [Cloud Load Balancing overview](https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview)
- [Choose a load balancer](https://docs.cloud.google.com/load-balancing/docs/choosing-load-balancer)
- [Load balancer feature comparison](https://docs.cloud.google.com/load-balancing/docs/features)
- [Cloud Load Balancing product page](https://cloud.google.com/load-balancing)
