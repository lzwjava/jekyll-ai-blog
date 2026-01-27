---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud 专业开发人员考试题库
translated: true
type: note
---

问题：提供 50 道 Google Cloud Professional Cloud Developer 认证考试的多选题（不显示答案）

回答：

以下是涵盖 Google Cloud Professional Cloud Developer 认证考试关键主题的 50 道原创多选题。每道题有四个选项 (A–D)。这些题目旨在反映真实考试的风格和范围（截至 2025–2026 年）。

1. 哪项服务最适合托管需要自动缩容至零实例并支持自定义 runtimes 的 stateless Web 应用程序？  
   - A. App Engine Standard  
   - B. Cloud Run  
   - C. Compute Engine  
   - D. Cloud Functions (1st gen)

2. 您需要存储具有 strong consistency 和 SQL 查询结构的结构化数据。您应该选择哪个数据库？  
   - A. Cloud Firestore (Datastore mode)  
   - B. Cloud SQL  
   - C. Bigtable  
   - D. Cloud Bigtable

3. 为运行在 Cloud Run 上的服务进行身份验证以调用 Cloud Storage JSON API 的推荐方式是什么？  
   - A. 使用存储在 Secret Manager 中的 service account key 文件  
   - B. 将 service account 关联到 Cloud Run 服务  
   - C. 使用无需配置的 Application Default Credentials  
   - D. 启用 Compute Engine 默认 service account

4. 在更新 Cloud Run 服务时，哪种部署策略可以最大限度地减少停机时间？  
   - A. Blue-green deployment  
   - B. Traffic splitting with revisions  
   - C. Rolling update with managed instance groups  
   - D. 使用 Compute Engine 的 Canary deployment

5. 您正在设计一个处理上传到 Cloud Storage 的图像的应用程序。哪个事件源应触发 Cloud Function？  
   - A. Pub/Sub message  
   - B. Cloud Storage object finalize event  
   - C. Cloud Audit Logs 条目  
   - D. HTTP request

6. 与手动执行 gcloud 命令相比，通过 cloudbuild.yaml 文件使用 Cloud Build 的主要好处是什么？  
   - A. 更快的构建时间  
   - B. 内置 caching 和 parallel steps  
   - C. 自动 secret rotation  
   - D. 免费无限次的构建时长

7. 哪个 IAM role 允许应用程序读写特定的 Cloud Storage bucket，而无需授予更广泛的项目权限？  
   - A. roles/storage.objectAdmin  
   - B. roles/storage.legacyBucketReader  
   - C. roles/storage.objectViewer + roles/storage.objectCreator  
   - D. roles/storage.admin

8. 您需要为运行在 Cloud Run 上的 microservices 应用程序实现 distributed tracing。您应该集成哪项 Google Cloud 服务？  
   - A. Cloud Trace  
   - B. Cloud Profiler  
   - C. Cloud Monitoring  
   - D. Cloud Logging

9. 在不影响当前流量的情况下，为 App Engine Standard 应用程序部署新版本的正确方法是什么？  
   - A. 使用 gcloud app deploy --promote  
   - B. 部署到新版本并使用 traffic splitting  
   - C. 直接更新默认版本  
   - D. 重新部署相同的版本号

10. 对于访问频率较低但仍需要毫秒级访问延迟的备份文件，Cloud Storage 中的哪种 storage class 最合适？  
    - A. Standard  
    - B. Nearline  
    - C. Coldline  
    - D. Archive

11. 您正在将 monolithic 应用程序迁移到 microservices。哪项服务最适合在服务之间安全地暴露 internal APIs？  
    - A. Cloud Endpoints  
    - B. Cloud Load Balancing internal HTTP(S)  
    - C. VPC Service Controls  
    - D. BeyondCorp Enterprise

12. 如何确保 Cloud Function 每次只处理来自 Pub/Sub subscription 的一条消息？  
    - A. 设置 --max-instances=1  
    - B. 在函数配置中设置 concurrency=1  
    - C. 在 Pub/Sub 中使用 ordered delivery  
    - D. 将 --trigger-topic 与 --ack-deadline 结合使用

13. 在 Cloud Run 应用程序中，读取更改频率较低的小型配置值的最快方法是什么？  
    - A. Cloud Firestore document  
    - B. Secret Manager + environment variable  
    - C. 启动时的 Cloud SQL 查询  
    - D. Cloud Storage JSON 文件

14. 当代码推送到 Cloud Source Repositories 时，应使用什么来自动构建 container images 并将其部署到 Artifact Registry？  
    - A. Cloud Scheduler + Cloud Build  
    - B. 连接到代码库的 Cloud Build trigger  
    - C. Artifact Registry webhook  
    - D. 在 CI/CD 流水中执行 gcloud builds submit

15. 对于在具有 multi-region clusters 的 GKE 上运行的全球 HTTP(S) 应用程序，您应该使用哪种负载均衡器类型？  
    - A. Internal HTTP(S) Load Balancer  
    - B. External Application Load Balancer  
    - C. Network Load Balancer  
    - D. Classic VPN Gateway

16. 您需要运行一个每天处理 1 TB 数据然后终止的批处理作业。哪项服务成本最低？  
    - A. Compute Engine preemptible VMs  
    - B. Cloud Run jobs  
    - C. Dataflow batch pipeline  
    - D. Dataproc Serverless

17. 在运行于 Cloud Run 的容器化应用程序中，管理 secrets 的最佳实践是什么？  
    - A. 将 secrets 固化（Bake）到 Docker image 中  
    - B. 将 Secret Manager 中的 secrets 挂载为 volumes  
    - C. 通过 Cloud Build 的 environment variables 传递 secrets  
    - D. 直接在应用程序代码中使用 Cloud KMS

18. 哪项服务可以自动处理 event-driven 工作负载的重试、dead-letter queues 和 exactly-once 处理语义？  
    - A. Cloud Tasks  
    - B. Eventarc  
    - C. 带有 ordering keys 的 Pub/Sub  
    - D. Workflows

19. 您想监控来自应用程序的自定义延迟指标。您应该使用哪项服务来创建这些 custom metrics？  
    - A. Cloud Monitoring custom service metrics  
    - B. Cloud Trace spans  
    - C. Cloud Profiler  
    - D. Cloud Logging structured logs

20. 为公开的 Cloud Run API 实现 rate limiting 的推荐方法是什么？  
    - A. 使用带有 quotas 的 API Gateway  
    - B. 在应用程序代码中使用 Redis 实现  
    - C. 使用 Cloud Armor  
    - D. 启用带有 OAuth 的 IAP

21. 哪个数据库支持全球分布式应用程序的 multi-region strong consistency？  
    - A. Cloud Spanner  
    - B. Firestore multi-region  
    - C. 带有 cross-region read replicas 的 Cloud SQL  
    - D. Bigtable multi-cluster routing

22. 如何在不创建密钥的情况下，授予第三方 service account 访问您的 Cloud Storage bucket 的权限？  
    - A. 使用 workload identity federation  
    - B. 生成 signed URL  
    - C. 将 service account 添加到 bucket IAM policy 中  
    - D. 使用 gsutil acl ch

23. 哪种工具有助于分析在 Cloud Run 上运行的 Go 应用程序的内存使用情况并检测泄漏？  
    - A. Cloud Profiler  
    - B. Cloud Debugger  
    - C. 通过 Cloud Trace 使用 pprof  
    - D. Memorystore for Redis

24. 您正在使用 Terraform 管理 GCP 资源。您应该在哪里存储 service account keys 等敏感值？  
    - A. 在 Terraform state 文件中  
    - B. 在带有 Terraform provider 的 Google Cloud Secret Manager 中  
    - C. 硬编码在 .tf 文件中  
    - D. 在加密的 Git 存储库中

25. Cloud Functions (2nd gen) 的默认扩缩容行为是什么？  
    - A. 自动缩容至零  
    - B. 始终运行至少 1 个实例  
    - C. 固定实例数量  
    - D. 仅支持手动扩缩容

26. 哪种选项为存储在 Cloud Storage 中的对象提供最强的 durability（持久性）？  
    - A. Dual-region  
    - B. Multi-region  
    - C. 带有 object versioning 的 Regional  
    - D. 启用 Turbo replication

27. 您需要运行从 Pub/Sub 拉取消息的容器化 background workers。哪项服务最合适？  
    - A. 带有 --cpu-throttling 的 Cloud Run services  
    - B. 带有 Pub/Sub pull subscriber 的 Compute Engine VM  
    - C. 由 Pub/Sub 触发的 Cloud Run jobs  
    - D. 带有 Deployment 和 pull subscription 的 GKE

28. 您应该使用什么来编排包含条件分支的多步骤 serverless workflow？  
    - A. Cloud Composer  
    - B. Cloud Workflows  
    - C. 通过 Pub/Sub 链接的 Cloud Functions  
    - D. Dataflow Flex templates

29. 哪项服务原生集成了 Cloud Build，用于扫描 container images 漏洞？  
    - A. Artifact Registry vulnerability scanning  
    - B. Container Analysis  
    - C. Security Command Center  
    - D. Binary Authorization

30. 您想为新的 Cloud Run revision 进行 canary testing。这该如何实现？  
    - A. 使用 traffic tags 和渐进式流量切换  
    - B. 部署到独立的服务  
    - C. 使用 --no-traffic 标志并手动切换  
    - D. 创建一个新项目

31. 处理上传到 Cloud Run 服务的大文件（>100 MB）的最佳方式是什么？  
    - A. 直接上传到 Cloud Run  
    - B. 直接上传到 Cloud Storage signed URL  
    - C. 使用增加超时的 multipart/form-data  
    - D. 通过 Pub/Sub 进行流式传输

32. 哪个功能允许您根据 cookie 或 header 值将流量路由到不同的 App Engine 版本？  
    - A. Traffic splitting  
    - B. 带有 routing 的自定义域名映射  
    - C. Dispatch.yaml  
    - D. 带有 tags 的 Versions

33. 您需要跨多个 Firestore documents 实现 transactional consistency。您应该使用哪个 API？  
    - A. Batch write  
    - B. Transaction  
    - C. Run in transaction  
    - D. Distributed counter pattern

34. 调用 Cloud APIs 的内部 GKE 工作负载实现身份验证的推荐方式是什么？  
    - A. Workload Identity  
    - B. Service account key JSON  
    - C. 默认 Compute Engine SA  
    - D. OAuth 2.0 client credentials

35. 哪项服务提供具有自动扩缩容功能的托管 Redis 兼容缓存？  
    - A. Memorystore for Redis Cluster  
    - B. Cloud Memorystore  
    - C. ElastiCache (AWS)  
    - D. GKE 上的 Redis Enterprise

36. 您正在排查 Cloud Run 服务的生产问题。哪种工具允许您拍摄运行中实例的 snapshots？  
    - A. Cloud Debugger  
    - B. Cloud Logging real-time tail  
    - C. Cloud Trace  
    - D. gcloud beta run services proxy

37. 在 CI/CD 流水中，Binary Authorization 的主要目的是什么？  
    - A. 签署 container images  
    - B. 扫描恶意软件  
    - C. 执行 admission policies（准入政策）  
    - D. 轮换 service account keys

38. 哪项 Pub/Sub 功能可确保特定实体的消息按发布顺序进行处理？  
    - A. Ordering keys  
    - B. Exactly-once delivery guarantee  
    - C. Flow control  
    - D. Dead-letter topic

39. 您需要以低延迟运行机器学习推理。哪种部署选项最适合 TensorFlow 模型？  
    - A. 带有 GPU 的 Cloud Run  
    - B. Vertex AI Endpoints  
    - C. 挂载了 GPU 的 Compute Engine  
    - D. 带有 GPU 节点的 GKE

40. 您应该使用什么来自动轮换外部 CI/CD 系统使用的 service account keys？  
    - A. Workload Identity Federation  
    - B. 通过 OAuth 的短时凭据  
    - C. Cloud KMS asymmetric keys  
    - D. Service account impersonation

41. 哪项监控指标表示 Cloud Run 服务由于高 CPU 使用率而正在扩容？  
    - A. container/cpu/utilization  
    - B. run.googleapis.com/request_count  
    - C. run.googleapis.com/container/startup_latency  
    - D. run.googleapis.com/active_instance_count

42. 您正在设计一个必须每秒处理 100 万个事件的系统。哪种消息服务最合适？  
    - A. Pub/Sub  
    - B. Cloud Tasks  
    - C. Eventarc  
    - D. Cloud Pub/Sub Lite

43. 在 GCP 上的分布式系统中进行日志记录的最佳实践是什么？  
    - A. 使用带有 structured JSON 的 stdout/stderr  
    - B. 直接写入 Cloud Logging API  
    - C. 使用旧版 App Engine logging  
    - D. 将日志存储在 Cloud Storage 中

44. 哪种选项允许在不重新部署代码的情况下逐步推出配置更改？  
    - A. App Engine config versions  
    - B. 每个 revision 的 Cloud Run environment variables  
    - C. 存储在 Firestore 中的 Feature flags  
    - D. Secret Manager versions

45. 您需要针对不同团队授予对 BigQuery datasets 的细粒度访问权限。推荐哪种方法？  
    - A. Authorized views  
    - B. Dataset-level IAM roles  
    - C. Column-level security  
    - D. BigQuery Omni

46. 容器化应用的典型 Cloud Build 流水线中操作的正确顺序是什么？  
    - A. Build → Scan → Push → Deploy  
    - B. Push → Build → Deploy → Scan  
    - C. Deploy → Build → Scan → Push  
    - D. Scan → Deploy → Build → Push

47. 哪项服务可以帮助您在 GKE 中实施 chaos engineering 实验？  
    - A. Chaos Mesh (开源)  
    - B. Cloud Service Mesh  
    - C. Fault Injection (Cloud Load Testing)  
    - D. 不存在原生的 GCP 服务

48. 您想减少 Cloud Functions (2nd gen) 的冷启动延迟。哪种选项最有帮助？  
    - A. 使用 minimum instances  
    - B. 增加分配的 CPU  
    - C. 改用 Cloud Run  
    - D. 使用 Cloud Scheduler 进行预热（Pre-warm）

49. 在 event-driven 支付处理系统中实现幂等性（idempotency）的推荐方法是什么？  
    - A. 使用 transaction ID 作为 idempotency key  
    - B. 启用 Pub/Sub exactly-once  
    - C. 使用 Cloud Tasks lease duration  
    - D. 在 Firestore 中存储已处理的 IDs

50. 哪种组合能够以最低的运维开销为公共 APIs 提供身份验证（authentication）和授权（authorization）？  
    - A. API Gateway + Identity-Aware Proxy  
    - B. Cloud Endpoints + ESPv2  
    - C. Cloud Run + Firebase Authentication  
    - D. Apigee + Service accounts

参考文献：

- [Google Cloud Professional Cloud Developer Exam Guide](https://cloud.google.com/learn/certification/cloud-developer)
- [Google Cloud sample questions for Professional Cloud Developer](https://cloud.google.com/learn/certification/cloud-developer#sample-questions)