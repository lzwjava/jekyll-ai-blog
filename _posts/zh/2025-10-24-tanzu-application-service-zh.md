---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: VMware Tanzu应用服务概览
translated: true
type: note
---

## VMware Tanzu Application Service for VMs (TAS for VMs) 简介

VMware Tanzu Application Service for VMs（TAS for VMs）是基于开源项目 Cloud Foundry 构建的商业平台即服务（PaaS）。该平台旨在简化云原生应用的部署、扩展和管理，让开发人员能够专注于编写代码而无需处理基础设施问题。TAS for VMs 支持在多种环境中快速部署应用，包括本地环境（如 vSphere）或公有云（AWS、Azure、GCP、OpenStack），同时支持自管理部署和经认证的商业提供商。

### 核心特性

- **开源基础**：基于 Cloud Foundry 的可扩展架构，避免供应商锁定，支持多语言、多框架和多服务
- **自动化部署**：使用常用工具（如 CLI）直接推送应用无需代码修改；应用会被打包成"droplets"（预编译包）实现快速部署和运行
- **弹性伸缩与高可用**：通过 Diego 在虚拟机间智能分配负载，支持自动扩缩容和故障容错，有效应对流量高峰或系统故障
- **用户管理**：通过 UAA（用户账户与认证）服务器将团队组织为"组织"和"空间"，支持基于角色的权限管理（如管理员、开发者）
- **服务集成**：通过服务代理轻松将应用与数据库或 API 等服务绑定，无需修改应用代码
- **监控与日志**：通过 Loggregator 将日志和指标聚合到"Firehose"数据流，支持实时分析、告警和工具集成
- **轻量版选项**：仅需 4 台虚拟机即可运行的轻量版本（标准版需13+台），适合小团队或测试环境，但存在扩展限制
- **灵活基础设施**：通过 BOSH（自动化工具）进行部署，使用 Tanzu Operations Manager 统一管理配置

### 核心优势

TAS for VMs 能够实现分钟级应用上线，通过自动扩缩容和全球可达性加速产品上市周期。该平台降低基础设施管理成本，通过隔离的工作空间增强安全性，并确保应用跨环境运行的一致性。通过抽象虚拟机管理，有效削减成本与复杂度，同时 Cloud Foundry 社区持续提供创新功能和技术支持。

### 工作原理

TAS for VMs 本质上是一个多租户 PaaS 平台：

1. **部署阶段**：通过 Tanzu Operations Manager 在 BOSH 管理的虚拟机上配置和部署平台
2. **应用生命周期**：开发者通过 CLI 推送代码；Cloud Controller 使用 buildpacks（语言特定配置）将代码打包成 droplets，随后 Diego 通过竞拍机制在主机虚拟机间分配并运行实例
3. **路由与访问**：Gorouter 处理入站流量并实现外部负载均衡；UAA 负责用户认证
4. **运维管理**：内部组件通过 NATS 消息总线和 BOSH DNS 进行通信；资源文件与配置存储在 GitHub、对象存储或 MySQL 中

TAS for VMs 在开源 Cloud Foundry 基础上扩展了 VMware 的企业级功能、技术支持和认证保障，使其成为生产工作负载的稳健选择。

详细内容请参阅官方文档：[TAS for VMs 概述](https://techdocs.broadcom.com/us/en/vmware-tanzu/platform/tanzu-platform-for-cloud-foundry/6-0/tpcf/concepts-overview.html)
