---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 机密管理中的 Vaults 崛起
translated: true
type: note
---

HashiCorp Vault 已成为现代 secrets management 和安全基础设施中最重要的工具之一。让我带您了解它的起源、演变及其重要性。

## The Genesis (2015)

HashiCorp Vault 由 Armon Dadgar 和 Mitchell Hashimoto 创建，并于 2015 年 4 月正式发布。其背后的公司 HashiCorp 当时已凭借 Vagrant、Packer、Terraform 和 Consul 等工具闻名。创始人发现基础设施工具领域存在一个关键空白：在现代分布式系统中，没有一个全面的开源解决方案用于管理 secrets 和保护敏感数据。

他们当时要解决的问题日益迫切。随着企业向云基础设施、microservices 和 DevOps 实践转型，secrets 正在疯狂激增。API keys、database credentials、TLS certificates 和 encryption keys 散落在配置文件、环境变量和安全性较差的存储中。将 secrets 植入应用程序或将其存储在纯文本配置文件中的传统方法，在动态的 cloud-native 环境下已彻底失效。

## Initial Vision

Vault 在设计之初就遵循了几个核心原则：

**Centralized secrets management** —— 为组织内的所有 secrets 提供单一事实来源，而不是将 secrets 分散在各种系统和配置文件中。

**Dynamic secrets generation** —— Vault 不存储长效的静态凭证，而是可以为 databases、cloud providers 和其他服务生成短效的、按需分配的凭证。这极大地减少了攻击面。

**Encryption as a service** —— Vault 可以处理加密和解密操作，使应用程序能够受益于强大的 cryptography，而无需自行实现。

**Detailed audit logging** —— 与 Vault 的每一次交互都会被记录，提供完整的 audit trail，记录谁在何时访问了哪些 secrets。

**Tight access control** —— 基于复杂的 policy 的访问控制，确保只有经过授权的实体才能访问特定的 secrets。

## 早期开发与应用 (2015-2017)

Vault 0.1.0 发布时具备了基础但强大的功能，包括存储通用 secrets 的能力、针对 AWS 和 PostgreSQL 的 dynamic secret 生成、灵活的 policy 系统以及多种 authentication backends。初始版本刻意保持聚焦，以便 HashiCorp 收集反馈并进行迭代。

这个时机非常完美。随着组织采用 containers、Kubernetes 和 microservices 架构，他们正深陷 secrets sprawl（密钥蔓延）的困扰。DevOps 团队需要一种能够整合进自动化流水线的程序化管理 secrets 的方式。Vault 以 API-first 的设计和对多个 secret backends 的支持，成为了理想的选择。

在此期间，HashiCorp 迅速扩展了 Vault 的功能，增加了对 MySQL、Cassandra 和 MongoDB 等更多 secret backends 的支持，引入了包括 GitHub、LDAP 和 AppRole 在内的更多 authentication 方法，并为企业级部署实现了 high availability 和 replication 功能。

## 企业级时代 (2017-2019)

2017 年，HashiCorp 推出了 Vault Enterprise，增加了大型组织在大规模生产部署中所需的功能。这包括用于跨多个集群扩展读取操作的 performance replication、用于业务连续性的灾难恢复复制（disaster recovery replication）、用于增强安全性的 HSM (Hardware Security Module) 支持、用于多租户部署的 namespaces，以及像 Sentinel 这种 policy-as-code 集成的治理功能。

这是一个关键时刻。Vault 不再仅仅是初创公司和科技公司的工具，开始被银行、医疗机构、政府部门和其他受高度监管的行业所采用。企业级功能解决了合规性、可审计性和运营韧性等阻碍这些组织使用的核心关切。

## 成熟与 Cloud Native 集成 (2019-2021)

随着 Kubernetes 成为主流的容器编排平台，Vault 与 cloud-native 生态系统的集成显著加深。HashiCorp 推出了用于简化容器化环境下 secret 提取的 Vault Agent，一种原生的 Kubernetes authentication 方法，用于将 secrets 挂载进 pods 的 Vault CSI Provider，以及用于 Kubernetes 原生 secret 管理的 Vault Secrets Operator。

在此期间，Vault 还扩展了其云集成，增加了对 AWS、Azure 和 GCP 等所有主要 cloud providers 在 authentication 和 dynamic secret 生成方面的原生支持。该工具在处理多云（multi-cloud）和混合云环境的复杂性方面变得越来越成熟。

## 近期发展 (2021 至今)

最近，Vault 继续在几个重要方向上演进：

**Vault Secrets Operator** —— 于 2023 年发布，提供了一种真正的 Kubernetes 原生方式将 Vault secrets 同步到 Kubernetes secrets 中，使已经投入 Kubernetes 的团队更容易采用。

**HCP Vault** —— HashiCorp Cloud Platform Vault 以完全托管服务的形式提供 Vault，消除了运行 Vault 基础设施的运营负担。这使得没有运营复杂性处理能力的、但又想获得 Vault 收益的小型团队和组织能够使用它。

**增强的 DevOps 集成** —— 与 CI/CD 平台、GitOps 工作流和 infrastructure-as-code 工具的深度集成，使 Vault 成为现代开发流水线的自然组成部分。

**Secrets Sprawl 解决方案** —— 意识到 secrets 存在于许多地方（源代码、CI/CD、容器、云服务），Vault 引入了相应功能和合作伙伴集成，用于发现并将 secrets 迁移到 Vault 中。

**Zero Trust Security** —— 随着零信任架构受到重视，Vault 基于身份的访问控制和短效凭证使其成为 zero trust 实现中的核心组件。

## 技术创新

几项技术创新使 Vault 变得格外强大：

**Barrier 和 Seal 机制** —— Vault 的架构使用一个加密屏障（cryptographic barrier）来保护所有静态数据。seal/unseal 机制确保即使有人获得了 Vault 存储后端的访问权限，如果没有 unseal keys，数据仍处于加密状态且不可用。

**Shamir's Secret Sharing** —— Vault 实现了 Shamir's Secret Sharing 算法，将 unseal keys 分发给多人，确保任何人都无法独自解封 Vault。这解决了密钥管理中一个关键的安全关切。

**Lease 系统** —— Vault 中的每个 secret 都有一个关联的 lease（租约）并且可以被撤销。这使得 secret rotation（密钥轮换）变得切实可行，并能够自动清理未使用的凭证。

**Plugin 架构** —— Vault 的插件系统允许第三方通过自定义的 secret engines、auth methods 和数据库连接来扩展 Vault，而无需修改核心代码库。

## 对行业的影响

Vault 的影响远远超出了它的直接用户群。它普及了几个重要概念，包括：作为静态凭证优选替代方案的 dynamic secrets；将 secrets management 视为需要专用工具的独立基础设施关注点；针对应用程序开发者的 encryption-as-a-service 的重要性；以及适合自动化工作流的 API 驱动的 secrets 管理。

该工具还影响了竞争对手和替代方案。在 Vault 取得成功后，许多 cloud providers 增强了其原生的 secrets 管理产品，如 AWS Secrets Manager 和 Azure Key Vault，该领域也涌现了其他开源项目，但 Vault 仍然是功能最全面、应用最广泛的解决方案。

## 当前现状与未来

如今，全球有数千家组织在使用 Vault，从初创公司到财富 500 强企业。它已成为运行现代 cloud-native 应用程序的组织安全基础设施的标准组件。该项目保持活跃开发，定期发布版本以增加新功能并改进现有能力。

展望未来，Vault 将继续演进，以应对日益复杂的分布式系统中关于 secrets 管理的新挑战：受监管行业对 secrets 治理和合规性的需求、与新兴技术和平台的集成，以及如何让开发团队更轻松、便捷地践行强大的安全实践。

HashiCorp Vault 的历史实际上是一部基础设施安全随云计算和 DevOps 实践共同演进的史诗。它发现了一个组织管理敏感数据的根本性问题，并提供了一个已成为现代安全架构基石的解决方案。