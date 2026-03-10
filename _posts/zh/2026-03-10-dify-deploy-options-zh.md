---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Dify 部署选项详解
translated: true
type: note
---

**问题：** Dify 开源项目与 dify.ai 门户网站之间的关系是什么，它们是否提供企业部署？

---

**回答：**

## 概述：同一产品，多种交付模式

Dify 由 **LangGenius, Inc.** 创建，开源 GitHub 项目 ([github.com/langgenius/dify](https://github.com/langgenius/dify)) 和 [dify.ai](https://dify.ai) 门户网站是同一个平台——只是访问方式不同。云服务托管了自部署版本的所有功能。可以将其类比为 WordPress.com 与 WordPress.org：相同核心软件，不同托管方式。

---

## 三种部署选项

### 1. Dify Cloud (dify.ai — 托管 SaaS)
这是 dify.ai 门户网站。Dify.ai 提供云托管服务，采用分层订阅模式。您可以立即注册并使用，无需任何设置。定价层大致如下：

- **Sandbox (免费)：** 试用层，应用和存储数量有限。
- **Professional (~$59/月)：** 针对独立开发者和小型团队构建生产 AI 应用。
- **Team (~$159/月)：** 针对中型团队，支持最多 50 名团队成员在一个工作空间中协作。
- **Enterprise (自定义定价)：** 联系销售；无限配额加上高级功能（见下文）。

### 2. 自托管社区版 (开源)
Dify 的核心平台是开源的。您可以从 GitHub 下载并在自己的服务器或云实例上运行，无需支付许可费。软件免费；您只需承担托管基础设施成本。它通过 Docker Compose 或 Kubernetes Helm charts 部署。这适合对数据控制有严格要求或希望避免 recurring SaaS 费用的团队。

仓库采用 Dify 开源许可，该许可本质上是 Apache 2.0 加上一些额外限制。

### 3. 企业版 (本地部署 / 私有云)
是的，Dify 提供企业部署。Dify Enterprise 以安全、可定制且企业就绪的包形式提供 Dify 的全部功能。专为 Kubernetes 构建，此版本支持官方 Helm chart 部署，让组织能够灵活地在自己的云基础设施或本地环境中运行 Dify，满足严格的合规、数据驻留和监管要求。

企业功能包括：
- 多个工作空间、SSO (SAML 和 OIDC)、部署协助、广泛的白标定制、可协商 SLA、模型负载均衡、集中式工作空间和用户管理、自定义角色、专用 Slack 频道、电话和邮件支持，以及企业级使用洞察。
- 多租户管理、二步验证和 MFA 支持，以及付费商业许可，支持完整品牌定制。

---

## 关键关系总结

## Key Relationship Summary

| Aspect | Open Source (GitHub) | dify.ai Cloud | Enterprise |
|---|---|---|---|
| Cost | Free (infra costs only) | Tiered subscriptions | Custom (contact sales) |
| Hosting | You manage it | Dify manages it | You manage it (on-prem/VPC) |
| Data control | Full | Limited (Dify's cloud) | Full |
| SSO / Multi-tenant | Manual setup | Limited | Yes, built-in |
| Support | Community / GitHub | Email | Dedicated private channels |
| License | Apache 2.0 + conditions | SaaS ToS | Commercial license |

---

## 底线

该平台提供自托管和云部署选项，满足不同用户在控制、扩展性和易用性方面的偏好。开源项目和 dify.ai 在核心上是同一产品——门户网站只是开源代码的托管云版本。对于需要本地部署、合规、SSO 和 SLA 的企业，可以通过联系 Dify 销售团队获取专用企业许可。

---

**参考资料：**

- [Dify GitHub 仓库 (langgenius/dify)](https://github.com/langgenius/dify/)
- [Dify 官网](https://dify.ai/)
- [Dify 企业页面](https://dify.ai/enterprise)
- [Dify 定价页面](https://dify.ai/pricing)
- [Dify Enterprise 在 Microsoft Marketplace 上](https://marketplace.microsoft.com/en-us/product/saas/sosgrouplimited.sos-dify-enterprise)
- [Dify 战略概述与定价详解 (Baytech Consulting)](https://www.baytechconsulting.com/blog/what-is-dify-ai-2025)