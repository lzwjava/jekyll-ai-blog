---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 了解 GCP 的身份识别代理
translated: true
type: note
---

Question: What is an introduction to Identity-Aware Proxy (IAP) in Google Cloud Platform (GCP)?

Answer: 

**Identity-Aware Proxy (IAP)** 是 Google Cloud 提供的一种 **managed security service**，作为应用程序和资源的中央授权层。它基于 **user identity** 和请求上下文实现 context-aware 访问控制，无需传统的 VPNs、bastion hosts 或暴露公共 IP。

### Core Purpose

IAP 通过确保以下几点来帮助实现 **Zero Trust** 原则：
- 只有经过身份验证和授权的用户才能访问您的应用程序
- 访问决策在 **application level**（而非仅在网络层）做出
- 资源保持 **private** 状态（无需打开公共防火墙端口）

### How IAP Works (High-Level Flow)

1. 用户尝试访问受保护的应用（通过浏览器或 API 调用）。
2. IAP 在请求到达应用程序 **之前** 对其进行拦截。
3. IAP 将用户重定向至 **Google login**（如果尚未登录）。
4. 身份验证成功后，IAP 检查 **IAM policies** 以验证用户是否拥有所需角色（例如 `roles/iap.httpsResourceAccessor`）。
5. 如果允许，IAP 将请求转发到后端应用程序，并包含 identity headers（例如 `X-Goog-Authenticated-User-Email`）。
6. 如果拒绝 → 用户收到 **403 Forbidden** 响应。

### Supported Resources (2026 status)

IAP 保护：
- **Cloud Run** 服务
- **App Engine** 应用程序
- **Compute Engine** VMs (HTTP(S) load balancers)
- **Google Kubernetes Engine (GKE)** (通过 HTTPS load balancer)
- **Internal HTTP(S) Load Balancers** (用于私有应用)
- **On-premises / hybrid** Web 应用程序 (通过 IAP for on-prem / BeyondCorp Enterprise)

### Key Benefits

- **无需 VPN** — 用户只需浏览器即可从任何地方访问应用
- 通过 Google Cloud IAM 实现 **集中式访问控制**（支持个人、Google Groups、Workspace 账号）
- **Context-aware**（在使用 Chrome Enterprise Premium 或 BeyondCorp Enterprise 时，可以结合设备安全状态等 BeyondCorp 属性）
- **内置 DDoS 保护** 和全球负载均衡
- **易于启用** — 通常只需点击几下 + IAM 绑定
- 同时支持 **Google accounts** 和 **external identities** (通过 Identity Platform / Workforce Identity Federation)

### Common Use Cases

- 内部工具和管理仪表板（无公共暴露）
- 仅限员工访问的 Staging / Dev 环境
- 希望在不迁移到云端的情况下进行加固的传统本地 Web 应用
- 保护 machine-to-machine 和 user-to-machine 场景下的 API 端点
- 使用 Google 发行的短期 Token 替换客户端证书或长效 API keys

### Quick Comparison: IAP vs Alternatives

| Feature                  | IAP (Google Cloud)      | Traditional VPN         | Cloud IAM alone       |
|--------------------------|--------------------------|--------------------------|------------------------|
| Granularity              | Per-app / per-resource   | Network-level            | Service account level  |
| External user support    | Yes (federation)         | Usually limited          | Limited                |
| Public IP needed?        | No                       | No                       | Often yes              |
| Device posture checking  | Yes (with BeyondCorp)    | Sometimes                | No                     |
| Setup complexity         | Low–medium               | High                     | Low                    |

IAP 是在 Google Cloud 中转向 **Zero Trust architecture** 并显著减少攻击面的最简便方法之一。

References:  

- [Identity-Aware Proxy overview](https://docs.cloud.google.com/iap/docs/concepts-overview)
- [Identity-Aware Proxy (IAP) product page](https://cloud.google.com/security/products/iap)
- [IAP documentation home](https://docs.cloud.google.com/iap/docs)