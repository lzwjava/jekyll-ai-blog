---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Google Cloud 技能总结
translated: true
type: note
---

根据我阅读的所有笔记，以下是您Google Cloud知识的全面总结：

---

## ☁️ Google Cloud — 您已掌握并使用的知识

### 🛠️ 实际构建与部署（动手实践）

| 模块/功能 | 使用方式 |
| --- | --- |
| **Speech-to-Text v2 API** | 集成到您的 `ww` CLI 工具中 — `ww gcp-speech transcribe <audio>` — 将音频上传到 GCS，运行 Chirp/长/短模型，将转录保存为 `.md` 文件。您深入了解 Chirp、Chirp_2、Chirp_3、长模型和短模型。 |
| **Cloud Storage (GCS)** | 用于音频上传的 `test2x` 存储桶。GCS 生命周期规则（删除旧文件，迁移到 Nearline/Coldline/Archive）。使用 `gsutil` CLI。 |
| **Cloud Run** | 部署了一个 Java/Spring Boot 的 `blog-server` 容器。您了解 `gcloud run deploy --source .`、Artifact Registry、Cloud Build、`.gcloudignore`、以及调试挂起问题的 `--verbosity=debug`。部署在 `asia-northeast1` 区域。 |
| **YouTube Data API v3** | 构建了 `ww gen-video upload` — OAuth 2.0 桌面流，使用可续传的 MediaFileUpload 进行视频上传。将 `client_secret.json` 存储在 `~/.google/` 目录。 |
| **OAuth 2.0** | 修复了 redirect_uri 问题，运行了 `flow.run_local_server(port=8080)`，在 `~/.google/youtube_token.json` 中处理令牌缓存。 |
| **Compute Engine** | 在台北区域（`asia-east1`）创建了一个 E2 micro 虚拟机作为 VPN 服务器（约每月 13 美元）。了解共享核心、抢占式/Spot 虚拟机、自定义机器类型。 |
| **gcloud CLI** | 从 507.0.0 更新到 532.0.0。使用 `gcloud auth login`、`gcloud config set project`、`gcloud services enable`、`gcloud components update`。 |
| **Google AdSense** | 添加到您的 Jekyll 博客 — `ads.txt`、自动广告脚本、手动文章内广告单元。提交了审批申请，处理了拒绝和修复。了解广告收入动态。 |

### 📚 学习并深入了解（考试/认证级别）

| 模块 | 您了解的内容 |
| --- | --- |
| **BigQuery** | 无服务器列式数据仓库。Dremel/Colossus/Borg 架构。用于成本优化的分区与聚类。`bq` CLI、Python 客户端 (`google.cloud.bigquery`)、`--dry_run`。BigQuery ML、向量搜索、JSON 嵌入存储用于 RAG。 |
| **IAM 与安全** | Identity-Aware Proxy (IAP) — Zero Trust、上下文感知访问。`roles/compute.instanceAdmin` 与 `roles/editor` 与 `roles/owner` 的区别。服务账号与用户账号。 |
| **GKE (Kubernetes Engine)** | 了解 GKE 集群创建、HPA/VPA 扩缩容、Nginx Ingress、安全访问模式。 |
| **Cloud SQL / Spanner / Firestore** | Spanner — 全球分布式、强一致性、ACID。Firestore — NoSQL 文档数据库、实时同步、离线支持、安全规则。Cloud SQL — 传统关系型数据库。 |
| **Vertex AI** | Vertex AI 上的 Imagen 4 图像生成、安全过滤器、`google-gen-ai-image-config`。Google AI Studio 与 Vertex AI 的指标对比。 |
| **Cloud Load Balancing** | GCP Cloud Load Balancing 简介、Cloud NAT、Cloud Armor (WAF)。 |
| **网络** | Cloud NAT 与家庭路由器对比、多区域设计、VPC、Private Service Connect。 |
| **认证** | 学习了 GCP ACE (Associate Cloud Engineer)、Professional Cloud Developer、Cloud Digital Leader、Professional ML Engineer。做过练习题。 |

### 💰 定价与成本知识

| 主题 | 详情 |
| --- | --- |
| **Compute Engine 定价** | 台北区域 E2 micro = $0.0084/小时。持续使用折扣、承诺使用折扣（30-70% 折扣）。Spot 虚拟机（60-91% 折扣）。 |
| **网络出站流量** | 亚洲区域首 1TB 为 $0.12/GiB。入站流量免费。 |
| **GCS 存储类别** | Standard → Nearline → Coldline → Archive。生命周期规则。 |
| **BigQuery 定价** | $6.25/TB 扫描数据量（按需模式）。通过分区/聚类降低成本。 |
| **GPU 成本** | GCP 上 8× H100 约每月 $57k。遇到过 GCP GPU 配额被拒的情况。 |
| **Cloud Run** | 免费层：每月 200 万次请求。按请求付费。 |

### ⚡ 您的 GCP 概况总结

您不仅仅是学习理论 — 您已经构建了**实际集成**：

- **`ww gcp-speech transcribe`** — 使用 GCS + Chirp 模型的语音转文本管道
- **`ww gen-video upload`** — 使用 OAuth 的 YouTube Data API
- **Jekyll 博客上的 AdSense 变现**
- **Java 后端的 Cloud Run 部署**
- **台北区域的 Compute Engine VPN**

您对 GCP 的**开发者/平台**方面非常熟悉（Cloud Run、GCS、Speech API、YouTube API、gcloud CLI、BigQuery），同时还具备跨多个服务的**认证级别知识**。根据笔记数量，您最薄弱的领域似乎是 **GKE**（理论多于实践）和 **Vertex AI**（学习了 Imagen 但实践较少），而您最擅长的领域是 **GCP Speech-to-Text** + **Cloud Run** + **GCS** + **OAuth/YouTube 集成**。
