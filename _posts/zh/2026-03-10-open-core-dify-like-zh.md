---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 类似 Dify 的开放核心公司
translated: true
type: note
---

**问题：** 哪些其他公司遵循与 Dify 类似的模式（开源项目 + 云门户 + 企业部署）？例如 Elasticsearch 和 GreptimeDB？

---

**回答：**

这种模式被称为 **"Open-Core"** 商业模式，是现代开发者工具公司中最主流的策略之一。该模式为：

> **Free open-source core → Managed cloud SaaS → Enterprise on-prem/private deployment**

如今我们看到的公共 OSS 企业，如 MongoDB、Confluent 和 HashiCorp，都采用了混合 open-core / 云托管模式，并附加专业服务。

---

## 1. Elasticsearch (Elastic)

Elasticsearch 和 Kibana 的核心在 AGPL 许可下开源，代码托管在公共仓库中 — 您可以开始使用，甚至构建完整的解决方案，而无需运行您看不到的代码。

三个层级：

- **Open Source / Self-hosted：** 在您自己的服务器上免费自运行。
- **Elastic Cloud (SaaS)：** Elastic Cloud 使工程团队能够利用 Elasticsearch 的功能和优势，而无需相关专业知识和维护。它采用订阅、按使用付费模式，允许团队在 AWS、Azure 或 Google Cloud 上部署和管理 Elasticsearch 集群。
- **Enterprise (on-prem)：** 高级功能锁定在企业订阅后面 — Standard、Gold、Platinum 和 Enterprise 层级 — 在开源核心基础上添加高级安全（SAML/OIDC、字段级安全）、机器学习、跨集群复制和告警。

值得注意的争议：AWS 开始提供托管 Elasticsearch 服务，这与 Elastic 的商业模式冲突。Elastic 更改了其许可，以防止云提供商将 Elasticsearch 打包为服务，AWS 则回应通过 fork 该项目创建了 OpenSearch。

---

## 2. GreptimeDB (Greptime)

GreptimeDB 是一个开源的可观测性数据库，在一个引擎中处理 metrics、logs 和 traces。它可以用作单一 OpenTelemetry 后端，取代 Prometheus、Loki 和 Elasticsearch，基于对象存储构建。

三个层级完全遵循与 Dify 相同的模式：

- **GreptimeDB OSS** — 开源数据库，适用于中小规模的可观测性和 IoT 用例，理想用于个人项目或开发/测试环境。
- **GreptimeDB Enterprise** — 功能强大的可观测性数据库，增强了安全、高可用性和企业级支持。
- **GreptimeCloud** — 完全托管的无服务器 DBaaS，具有弹性扩展和零运维开销，专为需要开箱即用速度、灵活性和易用性的团队构建。

---

## 3. HashiCorp (Terraform, Vault, Consul)

HashiCorp 的开源模式随着时间演变为免费、企业版和管理服务版本。Terraform、Vault、Consul 和 Nomad 等产品通过 source-available 许可访问，许多还提供企业版和管理服务版，包含免费和付费层级。

- **Open Source：** Terraform (IaC)、Vault (secrets)、Consul (networking) — 免费自托管。
- **Enterprise：** 添加 RBAC、审计日志、集中管理和治理功能。
- **HCP (HashiCorp Cloud Platform)：** 所有工具的完全托管 SaaS 版本。

HashiCorp 于 2021 年上市，并于 2025 年 2 月被 IBM 以 64 亿美元收购 — 这有力验证了 open-core 商业模式。

---

## 4. GitLab

GitLab CE (Community Edition) 采用 MIT 风格的开源许可，而 GitLab EE (Enterprise Edition) 采用专有许可。

GitLab 采用 open-core 模式，构建了一个完整的单一应用 DevOps 平台 — 覆盖从项目规划、CI/CD 到安全扫描和监控的整个软件开发生命周期。

- **GitLab CE：** 免费、自托管、开源。
- **GitLab.com (SaaS)：** 在其云门户上的免费和付费层级。
- **GitLab EE：** 企业自托管版，带有高级功能（合规、SAML、审计事件）。

---

## 5. MongoDB

- **MongoDB Community Server：** 开源、自托管。
- **MongoDB Atlas：** MongoDB 推出其云托管版本 Atlas，此后已成为巨额业务 — 约占总收入的 60%。
- **MongoDB Enterprise Advanced：** 用于本地或私有云的企业部署，包含安全、管理和支持。

---

## 6. Confluent (Apache Kafka)

Apache Kafka 是开源核心。Confluent 由 Kafka 原始创建者创立，在其基础上添加：

- **Confluent Platform：** 自托管企业版。
- **Confluent Cloud：** 完全托管的 Kafka-as-a-Service。
- Confluent Cloud 年同比增长超过 200%，展示了这种扩展模式对受益于运维简化的复杂技术公司的有效性。

---

## 7. Neo4j

Neo4j CE (Community Edition) 采用 GPL version 3 许可，而 Neo4j EE (Enterprise Edition) 采用专有许可，提供包括集群和热备份在内的额外功能。

相同模式：开源社区版 → 托管 AuraDB 云 → 企业本地版。

---

## 8. Other Notable Examples

| Company / Project | Open Source Core | Cloud SaaS | Enterprise |
|---|---|---|---|
| **Supabase** | GitHub (Apache 2.0) | supabase.com | Self-hosted Enterprise |
| **Minio** | GitHub (AGPL) | Hosted object storage | AGPL / Commercial enterprise |
| **Airbyte** | GitHub (MIT/ELv2) | Airbyte Cloud | Self-Managed Enterprise |
| **Metabase** | GitHub (AGPL) | Metabase Cloud | Enterprise (SAML, SSO) |
| **n8n** | GitHub (Source-available) | n8n Cloud | Enterprise self-hosted |
| **DataStax** (Cassandra) | Apache Cassandra (open) | Astra DB Cloud | DataStax Enterprise |

---

## The Common Pattern Summarized

第二代 OSS 公司，即 open-core 公司，为其软件提供两个版本："core" 版本保持开源，企业版利用核心代码但提供订阅制的优质功能，如安全和集成。在过去几年，OSS 企业还通过云托管服务引入额外收入流，允许用户通过云托管模式访问开源二进制文件，而无需自行设置和管理产品。

企业层级的关键差异化功能几乎总是相同：SSO/SAML、RBAC、审计日志、高可用性、专用支持 SLA 和合规工具。

---

**参考文献：**

- [Open-core model - Wikipedia](https://en.m.wikipedia.org/wiki/Open-core_model)
- [Elastic Open Source Philosophy](https://www.elastic.co/about/open-source)
- [GreptimeDB GitHub](https://github.com/GreptimeTeam/greptimedb)
- [Greptime Products Overview](https://www.greptime.com/product/db)
- [HashiCorp Open Source](https://www.hashicorp.com/en/about/open-source)
- [How companies make millions on Open Source (Palark)](https://palark.com/blog/open-source-business-models/)
- [Redpoint Open-source Top 25 Analysis](https://www.redpoint.com/content-hub/written/introducing-the-redpoint-open-source-top-25/)