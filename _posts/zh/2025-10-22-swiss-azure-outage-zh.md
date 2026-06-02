---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 瑞士北部Azure服务重大中断
translated: true
type: note
---

### 瑞士北部区域 Azure 服务中断事件：2025年9月26-27日

本次事件是瑞士北部区域一次影响多个可用区的大范围平台级中断，持续约22小时，从UTC时间9月26日23:54开始，至UTC时间9月27日21:59全面恢复。虽然大部分服务在UTC时间9月27日04:00左右恢复，但部分遗留问题仍需在当日进行人工干预。

#### 根本原因

中断源于对软件负载均衡基础设施中用于授权通信的证书进行的计划配置变更。其中一张新证书存在**格式错误的值**，且未在验证过程中被发现。该变更通过加急部署通道执行，意外地跨多个区域部署而未触发健康保障机制，导致：

- 负载均衡器与存储资源及节点断开连接
- 受影响的虚拟机检测到磁盘长时间断开后自动关闭以防数据损坏
- 影响蔓延至依赖服务，形成级联效应

#### 受影响服务

此次中断波及瑞士北部区域托管的大量Azure服务，包括：

- **核心基础设施**：Azure 存储、Azure 虚拟机、Azure 虚拟机规模集
- **数据库服务**：Azure Cosmos DB、Azure SQL 数据库、Azure SQL 托管实例、Azure Database for PostgreSQL
- **计算与应用**：Azure 应用服务、Azure API 管理、Azure Kubernetes 服务、Azure Databricks
- **网络与安全**：Azure 应用程序网关、Azure 防火墙、Azure Cache for Redis
- **分析与监控**：Azure Synapse Analytics、Azure 数据工厂、Azure 流分析、Azure 数据资源管理器、Azure Log Analytics、Microsoft Sentinel
- **其他服务**：Azure 备份、Azure Batch、Azure Site Recovery、Azure Application Insights

依赖这些服务的应用（如自定义应用程序）同样受到影响，导致大范围服务不可用或性能降级。

#### 时间线与缓解措施

- **9月26日 23:54 UTC**：配置变更部署后开始产生影响
- **9月27日 00:08 UTC**：自动化监控系统检测到异常
- **9月27日 00:12 UTC**：Azure 存储和网络团队启动调查
- **9月27日 02:33 UTC**：执行配置变更回滚
- **9月27日 03:40 UTC**：证书回滚完成
- **9月27日 04:00 UTC**：大部分服务自动恢复；识别出遗留问题（如因竞争条件或错误关机信号导致部分虚拟机处于停止/异常状态）
- **9月27日 06:19–14:15 UTC**：开发并验证恢复脚本；对SQL托管实例虚拟机、可信启动虚拟机及Service Fabric集群等受影响资源执行定向重启
- **9月27日 16:15 UTC**：遗留问题实现部分恢复
- **9月27日 21:59 UTC**：最终验证后确认全面恢复

连接恢复后大多数资源可自动恢复，但部分资源（如使用自定义扩展的虚拟机）需手动重启以解决启动顺序问题。

#### 经验总结与改进措施

微软初步事件报告强调已实施的改进：

- 已完成部署系统审计并移除高风险加急部署通道
- 已完成自动回滚等安全增强措施
- 计划于2025年11月前实现：增强资源健康状态监控，优化弹性恢复流程以减少人工干预

此次事件凸显了共享基础设施中配置变更的风险，但Azure的响应机制有效控制了数据丢失范围并实现了快速大规模恢复。

[Azure 状态历史记录](https://azure.status.microsoft/en-us/status/history/)
