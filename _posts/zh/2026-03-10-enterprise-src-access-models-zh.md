---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 企业源代码访问模型
translated: true
type: note
---

**问题：** 在 open-core 公司中，对于企业级 on-premises/私有部署，是否向客户提供源代码？企业级功能（SSO/SAML、RBAC、audit logging、HA 等）是否闭源？

---

**回答：**

## 简短回答

**是的，企业级功能几乎总是闭源（专有）的。** 但客户对源代码*访问*的情况更为微妙——并非非黑即白。

---

## 源代码访问的范围

实际上有三种不同的场景，而非仅“开源”或“闭源”：

### 1. 完全闭源 / 仅二进制文件（经典企业模式）

企业级附加组件是编译后的二进制文件或插件。客户完全得不到源代码。他们部署预构建的工件。公司基于免费软件代码库创建闭源 fork，或将额外专有功能作为模块提供，以避免违反免费软件许可。例如：较旧的 Elastic plugins、某些 Confluent connectors。

### 2. 源代码可用（现代趋势）

企业级代码*对付费客户可见*——他们可以阅读甚至修改它——但**不能重新分发或在没有商业协议的情况下使用它**。对于企业软件，提供源代码如今已成为基本要求。源代码托管的时代已结束。客户期望获得访问权限。如果你不提供，他们会找到提供者。这正迅速成为主流模式，因为企业买家——尤其在受监管行业——要求代码可审计性以进行安全审查。

### 3. 完全开源（企业级功能罕见）

一切均为开源，包括企业级功能。收入来源于支持、SLA 和托管服务。Red Hat/RHEL 是这种方法的典型示例。

---

## 企业级功能本身是否闭源？

是的。基础产品是开源的，但重要功能是专有的，需要付费许可。“核心”部分是开源的。其余一切均需付费。

企业所需的功能——SSO、audit logs、高级 alerting、基于角色的访问——均为企业专属。这些并非小众功能；对于在受监管环境或大规模运营的团队而言，它们是基本要求。

这是 deliberate 的产品策略：最吸引管理层或高管的特性是专有的，需要订阅。焦点不再是“该功能技术上在哪里？”——而是面向最终用户。

---

## 各公司实际处理方式的真实示例

| Company | Enterprise Code Access | License Model |
|---|---|---|
| **Elastic** | Source-available to customers | Elastic License 2.0 (ELv2) — can read, cannot redistribute or offer as SaaS |
| **GitLab EE** | Source code visible on GitLab.com | Proprietary — can inspect but not use without a license |
| **HashiCorp (Vault/Terraform EE)** | Source-available | BSL (Business Source License) — reverts to open after 4 years |
| **Neo4j EE** | Binary only | Proprietary |
| **Grafana Enterprise** | Source-available to paying customers | Grafana Enterprise License |
| **MongoDB** | SSPL (partially open, highly restrictive) | SSPL — effectively source-available for most uses |

---

## 这种拆分是故意的（非偶然）

公司开发企业版，将专有增值通常集中在开源项目不足的领域——通常针对企业客户需求，如垂直可扩展性、第三方集成、改进的安全性和更高速度。

开源社区的批评是真实的：许多所谓的“企业级”功能最终成为基本安全特性，如 TLS 支持——免费版中你希望有的简单改进——但这些从未进入社区版，因为公司意图仅让个人使用该版本。

---

## 锁定风险

Open core 会产生一种微妙的锁定形式。你不会被开源部分锁定——你可以随时 fork 它。你被你依赖的专有功能锁定。Open core 供应商可以随时更改许可。Elastic 这么做了。HashiCorp 这么做了。Redis Labs 这么做了。MongoDB 这么做了（SSPL）。当商业模式不起作用时，许可会变得更严格。

---

## 总结

- 企业级功能（SSO、RBAC、audit logs、HA clustering）→ **总是闭源 / 专有**
- 客户源代码访问→ **取决于公司，但趋势是“source-available”（你可以阅读，但不能复制/重新分发）**
- 完全开源的企业级功能→ **罕见，主要为 Red Hat 模式**
- On-prem 企业部署 = 你在自家基础设施上运行他们的专有二进制文件/插件，通常无权修改

---

**参考资料：**

- [Open-core model - Wikipedia](https://en.wikipedia.org/wiki/Open-core_model)
- [Open Source vs Open Core: What It Actually Means (OneUptime)](https://oneuptime.com/blog/post/2026-02-14-open-source-vs-open-core/view)
- [OCV Source Available License](https://www.opencoreventures.com/blog/ocvs-new-source-available-license-is-a-simple-alternative-to-closed-source-licenses)
- [Open Core is a Misunderstood Business Model](https://opencoreventures.com/blog/open-core-is-a-misunderstood-business-model)
- [Some Thoughts on Open Core - Linux Journal](https://www.linuxjournal.com/content/some-thoughts-open-core)
