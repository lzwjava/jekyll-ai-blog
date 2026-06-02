---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Platform 历史
translated: true
type: note
---

Question: Introduction to the history of Google Cloud Platform

Answer:

Google Cloud Platform (GCP)，现在通常被称为 **Google Cloud**，是 Google 的一套云计算服务套件。它主要与 **AWS** 和 **Microsoft Azure** 竞争。其发展历史与支撑 Google Search、YouTube、Gmail 和 Maps 的内部基础架构密切相关。

### 早期起步与关键里程碑

- **2008 – 正式进入云计算领域**
  在 **2008 年 4 月**，Google 发布了 **Google App Engine** (GAE) 预览版。这是一款 **PaaS** (Platform as a Service) 产品，允许开发者使用 Python（后来扩展到 Java、Go、PHP、Node.js 等）在托管、自动扩展的环境中部署 Web 应用程序。
  App Engine 被广泛认为是后来演变为 Google Cloud Platform 的真正起点。

- **2010 – 首批 IaaS 基础组件**
  在 **2010 年 5 月**，Google 推出了：
  - **Google Cloud Storage** — 对象存储服务（Amazon S3 的直接竞争对手）
  - **BigQuery**（内部最初称为 Dremel）— 发布预览版，这是一款用于大规模分析的革命性 Serverless 数据仓库
  - **Prediction API** — 早期的 Machine Learning 服务（后被弃用）

- **2011–2012 – 正式的平台品牌化**
  - 2011 年左右，各项独立服务开始被整合到一个更统一的产品组合下。
  - 在 **2012 年 7 月**，Google 正式创立了 **Google Cloud Platform** 品牌，并开始将其作为凝聚力强的产品系列进行推广。

- **2013–2015 – 核心服务的快速扩张**
  - **2013**: **Google Compute Engine** (GCE) 正式版发布 → 完整的 IaaS 虚拟机服务（虽早前已发布，但在 2013 年达到 GA 阶段）。这是 Google 对 AWS EC2 的直接回应。
  - **2014**: **Kubernetes** 开源（诞生于 Google 内部的 Borg 系统）。
  - **2015**: **Kubernetes 1.0** 发布 → 成为 Google Kubernetes Engine (GKE) 的基石，目前是 GCP 最强大的服务之一。

- **2016–2018 – 成为严肃的企业级参与者**
  - **2016**: Diane Greene（VMware 联合创始人）加入 Google 领导云业务 → 开启了重大的企业级推进。
  - 品牌重塑力度加强；“Google Cloud” 身份得到强化。
  - **Cloud Spanner**（全球分布式关系型数据库）于 2017 年发布 — 这是其独特的竞争优势。
  - **Anthos**（多云/混合云平台）于 2019 年发布，但其根源可追溯到这一时期。

- **2019–2021 – 品牌重塑与 AI 重心**
  - **2019–2020**: 营销重点从 “Google Cloud Platform” 转向 **Google Cloud**。
  - 大力投资于 **AI/ML**（Vertex AI、BigQuery ML、TPUs）、**Anthos** 以及 **Security** 产品。

- **2022–2025 – 成熟与增长**
  - Google Cloud 的市场份额稳居第三（截至 2024–2025 年全球约占 10–11%），仅次于 AWS 和 Azure。
  - 在 **AI**、**Data Analytics**、**Kubernetes** 和 **Sovereign Cloud**（主权云）解决方案方面增长强劲。
  - 持续扩展区域（目前已有 40 多个 Region，120 多个 Zone）。

### 简要里程碑时间表

| 年份       | 里程碑                                  | 类别         |
|------------|----------------------------------------|--------------|
| 2008       | Google App Engine (预览版)             | PaaS         |
| 2010       | Cloud Storage + BigQuery (预览版)      | Storage + Analytics |
| 2013       | Compute Engine GA                      | IaaS         |
| 2014       | Kubernetes 开源                         | Containers   |
| 2017       | Cloud Spanner GA                       | Database     |
| 2019–2020  | 品牌重塑 → Google Cloud                | Branding     |
| 2020+      | Vertex AI, 生成式 AI 推进               | AI/ML        |

Google Cloud 虽然起步晚于 AWS (2006) 和 Azure (2010)，但它利用了 Google 世界级的内部基础设施，特别是在 **Data Processing**、**AI** 和 **Container Orchestration** 领域。如今，它在 **Data & Analytics**、**Kubernetes** 和 **AI/ML Workloads** 方面表现尤为强劲。

参考文献：

- [Google Cloud Platform - Wikipedia](https://en.wikipedia.org/wiki/Google_Cloud_Platform)
- [An Annotated History of Google's Cloud Platform](https://medium.com/@retomeier/an-annotated-history-of-googles-cloud-platform-90b90f948920)
- [Timeline of Google Cloud Platform](https://timelines.issarice.com/wiki/Timeline_of_Google_Cloud_Platform)
- [The History of Google Cloud Platform - Pluralsight](https://www.pluralsight.com/resources/blog/cloud/history-google-cloud-platform)
