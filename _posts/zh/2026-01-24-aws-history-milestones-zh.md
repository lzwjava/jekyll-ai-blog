---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AWS 历史与里程碑
translated: true
type: note
---

Question: Provide an introduction to the history of AWS (Amazon Web Services)

Answer: 

以下是 **Amazon Web Services (AWS)** 的简要发展史：

### 早期起源 (2000–2006)

- Amazon 开始构建大规模的内部 Infrastructure，以应对其电子商务业务的巨大增长。
- 到 2000 年代初期，Amazon 已经创建了非常复杂的内部系统，涵盖 Storage、Computing、Databases 和 Distribution。
- 2002 年，Jeff Bezos 发布了一项著名的指令：**所有团队必须仅通过服务接口（Service Interfaces）相互通信**（即面向服务架构 Service-oriented architecture），严禁直接链接——这一架构决策后来成为了 AWS 的基石。
- 关键洞察：Amazon 意识到，自己在运行互联网规模的 Infrastructure 方面变得非常擅长——远超大多数公司。

### AWS 的诞生 – 公共服务 (2006)

- **2006 年 3 月**：Amazon S3 (Simple Storage Service) 发布 —— 这是第一个公开可用的 AWS 服务
  → 提供具有 99.999999999% ("11 9s") 持久性承诺的 Object storage
- **2006 年 8 月**：Amazon EC2 (Elastic Compute Cloud) 发布 Beta 版
  → 按小时租用 Virtual Machines —— 在当时是革命性的
- 这两项服务被广泛认为是**现代云计算的诞生**。

### 快速扩张 (2007–2012)

- 2007–2008：推出了 RDS (托管关系型数据库)、Elastic MapReduce、CloudFront (CDN)、SimpleDB、Elastic Load Balancing
- 2009：引入了 **Availability Zones**（可用区）概念和 **VPC (Virtual Private Cloud)**
- 2010：正式结束 Beta 阶段，AWS 成为一项真正的业务
- 2011：推出 **DynamoDB**、Route 53 (DNS)、IAM (细粒度权限管理)
- 2012：推出 **Redshift** (数据仓库)、**Glacier** (低成本归档存储)

### 确立统治地位 (2013–2018)

- 2013–2014：推出 Lambda (Serverless)、ECS (容器服务)、Aurora (兼容 MySQL/PostgreSQL 的数据库)
- 2015：**AWS re:Invent** 成为全球最大的云计算会议
- 2016–2017：推出 SageMaker (Machine Learning)、Fargate (Serverless 容器)、AWS Snowball / Snowmobile
- 到 2017–2018 年，AWS 占据了约 33–35% 的市场份额 —— 超过了 Microsoft Azure + Google Cloud 的总和

### 成熟与 AI 时代 (2019–2025)

- 2019：推出 AWS Outposts (混合云硬件)、AWS Local Zones
- 2020–2021：推出 Graviton 处理器 (基于 ARM 架构，具有更好的性价比)
- 2022–2023：大力推进 Generative AI 基础设施 (Trainium、Inferentia 芯片、Bedrock、SageMaker 增强功能)
- 2024–2025：在 AI 基础设施、大规模 GPU 集群和主权云区域方面持续保持领导地位

### 关键里程碑总结

| 年份 | 里程碑 | 影响 |
| :--- | :--- | :--- |
| 2006 | S3 + EC2 发布 | 发明了现代公共云 |
| 2009 | VPC & Availability Zones | 提供企业级 Networking 与可靠性 |
| 2012 | re:Invent 大会开始举办 | 成为云计算行业的风向标事件 |
| 2014 | Lambda (Serverless) | 开启了 Serverless 革命 |
| 2017 | 约 180 亿美元年营收，市场领导者 | 证明了云计算是一项庞大的商业业务 |
| 2020+ | Graviton + Trainium/Inferentia 芯片 | 为 AI 与成本控制实现垂直整合 |

AWS 并没有发明云计算概念 —— 但它将其**商业化**，让数百万开发者能够使用，并开创了这个 Microsoft Azure、Google Cloud、Alibaba Cloud 等随后纷纷加入的行业类别。

References:  

- https://aws.amazon.com/about-aws/global-infrastructure/history/
- https://en.wikipedia.org/wiki/Amazon_Web_Services
- https://www.allthingsdistributed.com/2006/08/amazon_s3.html (Werner Vogels 博客 – 最初的发布公告之一)