---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Cloud Run 被忽视的缺点
translated: true
type: note
---

以下是一些关于 **Google Cloud Run** 的**非主流或反直觉观点** / 热门争议 / 较少被提及的批评，这些观点经常出现在开发者讨论中（尤其是 Reddit、Hacker News、博客和论坛）。这些观点与将 Cloud Run 誉为“最佳 Serverless 容器平台”的主流赞美相左。

**问题：关于 Google Cloud Platform (GCP) 中的 Cloud Run，有哪些非主流观点？**

**回答：**

Cloud Run 因其简单性、基于容器的 Serverless 模型、按请求付费的价格体系以及出色的 Developer Experience 而广受赞誉。然而，在长期运行生产负载的用户中，持续出现了一些较少见或属于“非主流观点”式的批评：

- **针对某些 Networking / Enterprise 用例，Cloud Run 的设计实际上是有缺陷的**  
  它对 Google 的 Serverless VPC Access 和 Load Balancer 的依赖引入了各种怪异问题（URL 损坏、受限的 Outbound Networking、文档中标记为“不推荐”的有限自定义域名行为、以及在某些 Region 从零扩容时缓慢且不可靠的 Cold Starts）。一些开发者认为这些不是小 Bug，而是基础架构上的权衡，使得它在处理非平凡应用时，无法完全替代 GKE 或 Compute Engine。

- **一旦需要 Reliability，它并不总是像宣传的那么便宜**  
  为了避免痛苦的 Cold-start 延迟或丢弃请求，许多团队将 `min-instances` 设置为 1（或更高）并启用 `always-allocated CPU`。这使得“仅在处理时付费”的承诺变成了一张更接近于廉价 Always-on VM 的账单。对于中等流量的服务，实际成本可能会超过一个小型的 GKE Autopilot 集群，甚至超过调优后的 Cloud Functions 配置。

- **对许多工作负载而言，Cloud Run 相比 Cloud Functions 被过度吹捧了**  
  少数派声音（包括一些 Google 员工撰写的反向观点文章）认为，“Cloud Run 绝对优于 Cloud Functions”的论调是市场驱动的。对于简单的 Event-driven 或 HTTP-triggered 逻辑，Cloud Functions（或最新的 Cloud Run Functions）的开发速度更快，在极低流量下成本更低，拥有更好的 Native Trigger 生态系统，并避免了 Container Build 的复杂性。“万事皆用 Cloud Run”的建议会导致团队对简单的任务过度工程化（Over-engineer）。

- **到 2025 年，从零开始的 Cold-start 可靠性依然不尽如人意**  
  尽管有所改进，许多团队仍报告称，当 `min-instances = 0` 时，会出现偶发性的长尾延迟（数秒）甚至唤醒失败事件——特别是在非热门 Region 或使用较大 Container Images 时。这使得对于延迟敏感的用户侧 API 来说，如果不开启 `min-instances`（从而导致更高成本），使用 Cloud Run 会面临风险。

- **与 AWS ECS Fargate 或 Azure Container Apps 相比，Egress / Networking / VPC 的体验依然痛苦**  
  Serverless VPC Access connector 的限制、Private Services 较高的延迟、在许多场景下缺乏 Native Outbound Static IPs，以及偶尔怪异的 Load-balancer 行为，导致一些多云或企业级团队认为 Cloud Run 是“一个非常棒的 Serverless 容器选项……但它依然强迫你困在 Google 的网络城堡里”。

- **伪装在简单性下的 Lock-in 太容易形成**  
  虽然容器在理论上是可移植的，但与 Cloud Logging、Cloud SQL Proxy Sidecars、IAM、Artifact Registry、域名映射怪癖以及通过 Eventarc 实现的事件机制的深度集成，制造了隐形锁定。有人认为，相比起步于纯粹的 Kubernetes 或 VMs，后期从 Cloud Run 迁移出来的难度大得令人惊讶。

这些观点属于少数派看法——大多数开发者在处理其核心场景（HTTP APIs、Background workers、中小规模 Microservices）时，依然给予 Cloud Run 极高的评价。而当团队面临更大规模、更低延迟要求、复杂网络环境或极度波动/极度安静的流量模式时，这些批评声音会变得更加强烈。

**参考资料：**

- [Cloud Run: broken by design (Reddit thread)](https://www.reddit.com/r/googlecloud/comments/117dd9i/cloud_run_broken_by_design)
- [No, Cloud Run is not better than Google Cloud Functions (Medium article)](https://medium.com/google-cloud/no-cloud-run-is-not-better-than-google-cloud-functions-f34f46bd3545)
- [Shouldn't cloud run instance reliably scale from zero instances? (Reddit)](https://www.reddit.com/r/googlecloud/comments/yp9yjg/shouldnt_cloud_run_instance_reliably_scale_from)
- [Coming from Azure, Cloud Run is amazing — but mentions URL mangling bug (Reddit)](https://www.reddit.com/r/googlecloud/comments/1d7iv86/coming_from_azure_cloud_run_is_amazing)
- 探讨 `min-instances` 成本和 Cold-start 行为的各类 Hacker News 和 Reddit 贴文 (2023–2025)