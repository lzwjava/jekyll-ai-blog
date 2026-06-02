---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: 专业云开发者考试指南摘要
translated: true
type: note
---

Question: Professional Cloud Developer 考试指南的内容是什么？

Answer: **Professional Cloud Developer** 考试指南概述了在 Google Cloud 上构建、部署和管理可扩展、安全且高可用应用程序所需的技能和知识。该认证的候选人应具备云原生应用程序、Google Cloud APIs 以及各种托管服务的经验。

该考试分为四个主要部分：

*
**第 1 部分：设计高度可扩展、可用且可靠的云原生应用程序 (~36%)**


* 侧重于选择合适的平台（例如 Cloud Run, GKE）和设计高性能的 APIs (REST, gRPC)。


* 包括通过 Identity-Aware Proxy (IAP), Secret Manager 和 IAM roles 来确保应用程序的安全。


* 涵盖数据存储选择（例如 Spanner, Bigtable）和复制策略。




*
**第 2 部分：构建和测试应用程序 (~23%)**


* 涵盖使用 Cloud Shell, Cloud Code 和 Gemini Code Assist 等工具设置开发环境。


* 侧重于使用 Cloud Build 构建容器并将其存储在 Artifact Registry 中。


* 包括编写单元测试和执行自动化集成测试。




*
**第 3 部分：部署应用程序 (~20%)**


* 详细说明 Cloud Run 的部署策略，包括使用 Eventarc 和 Pub/Sub 触发器。


* 涵盖将容器部署到 GKE，定义资源需求并实施健康检查。




*
**第 4 部分：将应用程序与 Google Cloud 服务集成 (~21%)**


* 侧重于管理连接以及对 Cloud SQL 和 Firestore 等数据存储进行数据读写。


* 涵盖通过 Client Libraries 或 REST 调用 Google Cloud APIs，使用 exponential backoff 处理错误，以及对结果进行分页处理。


* 包括可观测性任务，如为指标 (metrics)、日志 (logs) 和追踪 (traces) 检测代码，以及使用 Gemini Cloud Assist 进行故障排除。





References:

* [Professional Cloud Developer Exam Guide](https://services.google.com/fh/files/misc/professional_cloud_developer_exam_guide_english.pdf)
