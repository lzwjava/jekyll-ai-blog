---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Armor DDoS 与 WAF 防护
translated: true
type: note
---

Question: What is an introduction to Google Cloud Armor?

Answer:

Google Cloud Armor 是 Google Cloud 的 **network security service**，旨在保护应用程序和基础设施免受各种基于互联网的威胁，特别是 **DDoS attacks** 和常见的 web application attacks。

### Main Purposes

- **DDoS protection** — 缓解容量型网络层（Layer 3/4）和应用层（Layer 7）攻击。
- **Web Application Firewall (WAF)** — 阻断常见的漏洞利用，如 SQL injection (SQLi)、cross-site scripting (XSS)、remote code execution 以及许多其他 OWASP Top 10 威胁。

### Key Features

- **Always-on Layer 3/4 DDoS protection** — 为 Google Cloud load balancers 自动提供（基础容量型防护无需额外配置）。
- **Layer 7 protection** — 通过附加到 HTTP(S) load balancers 的 security policies 进行配置。
- **Security Policies** — 核心机制：
  - 自定义规则（定义 match conditions → 触发 allow、deny、redirect、rate-limit 等操作）。
  - **Preconfigured WAF rules** — 开箱即用、符合 OWASP 标准的规则集，包含数十种签名。
  - **Preconfigured protection levels**（例如针对常见威胁的默认规则集）。
- **Adaptive Protection** (Enterprise tier) — 基于 ML 的自动威胁检测和规则调整。
- **Bot Management** (Enterprise) — 先进的 bot 检测与缓解。
- **Edge security** — 规则在 Google 的 edge 端（靠近流量源头）进行评估，从而减轻后端负载。

### Tiers / Editions (as of 2025–2026)

- **Cloud Armor Standard** — 基础 DDoS protection + 自定义规则 + 部分 preconfigured WAF rules（按需付费，主要根据处理的请求量计费）。
- **Cloud Armor Enterprise** — 全功能版本：
  - 高级 WAF 规则
  - Adaptive Protection
  - Bot Management
  - Managed Protection（始终运行的精选防御）
  - 通过订阅实现的预测性定价（月度/年度承诺选项）

### Where It Attaches

Cloud Armor policies 主要附加到：

- 全球外部 **Application Load Balancers** (HTTP/HTTPS)
- Classic Application Load Balancers
- 某些跨项目和 multi-cloud 场景（需正确配置）

它**不直接**保护 Compute Engine VMs 或非负载均衡流量，除非流量通过受支持的 load balancer 路由。

### Common Use Cases

- 保护公共 web applications 免受 DDoS 洪水攻击
- 无需编写自定义 regex 规则即可阻断常见 web 攻击
- 对可疑客户端（例如暴力破解登录尝试）进行 Rate limiting
- 基于地理位置或 IP 的访问控制
- 防御 APIs 和移动后端
- 为面向互联网的服务增加 defense-in-depth

简而言之：Cloud Armor 是 Google 的 **always-on DDoS scrubbing** + **managed WAF** + **edge policy enforcement** 的结合体，充分利用了 Google 庞大的全球网络和威胁情报。

References:

- [Google Cloud Armor Overview](https://docs.cloud.google.com/armor/docs/cloud-armor-overview)
- [Google Cloud Armor Product Page](https://cloud.google.com/security/products/armor)
- [Google Cloud Armor Documentation](https://docs.cloud.google.com/armor/docs)
