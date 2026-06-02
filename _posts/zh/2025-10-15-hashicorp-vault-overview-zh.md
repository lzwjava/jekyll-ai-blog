---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: HashiCorp Vault概览
translated: true
type: note
---

### 什么是 HashiCorp Vault？

HashiCorp Vault 是一款开源工具，专为安全管理、存储和访问敏感数据（通常称为“机密信息”）而设计。这些信息包括 API 密钥、密码、证书、令牌和加密密钥。它作为一个基于身份的集中式机密管理系统，提供加密即服务和特权访问控制功能，帮助企业在动态、多云或混合环境中保护敏感信息。

#### 核心特性

- **机密信息管理**：Vault 既能处理静态机密（如长期有效的密码），也能管理动态机密（按需生成的短期凭证，例如会自动过期的数据库用户）。
- **加密与审计**：所有数据在存储和传输过程中均经过加密，并提供完整的日志记录和审计功能以追踪访问和变更。
- **基于身份的访问**：可与身份提供商（如 LDAP、OIDC）集成，对用户和系统进行身份验证，并执行精细化的访问控制策略。
- **动态凭证与租期机制**：机密信息设有有效期限，从而降低长期暴露的风险。
- **云无关与自托管**：适用于任何基础设施环境，支持本地部署或托管服务。

#### 工作原理

Vault 采用客户端-服务器架构。客户端（应用程序或用户）向 Vault 服务器进行身份验证，服务器根据策略对请求进行授权。一旦获得批准，Vault 可以检索存储的机密信息、生成新的机密或撤销访问权限。例如，一个应用程序可以请求临时数据库凭证，使用后让其自动过期。其架构包含用于持久化存储的后端（如 Consul、PostgreSQL），并支持通过集群实现高可用性。

该工具广泛应用于 DevOps、安全与合规场景，用以替代人工处理机密信息的方式，在低信任环境中降低泄露风险。

#### 参考资料

- [什么是 Vault？ | Vault - HashiCorp Developer](https://developer.hashicorp.com/vault/docs/about-vault/what-is-vault)
- [HashiCorp Vault | 基于身份的机密信息管理](https://www.hashicorp.com/en/products/vault)
- [hashicorp/vault：用于机密信息管理、加密...的工具 - GitHub](https://github.com/hashicorp/vault)
- [什么是 HashiCorp Vault 及其工作原理？ - KodeKloud](https://kodekloud.com/blog/what-is-hashicorp-vault/)
