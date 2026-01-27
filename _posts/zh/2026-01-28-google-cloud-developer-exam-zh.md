---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5.2
title: Google Cloud 开发者考试试题
translated: true
type: note
---

问题：请编写 50 道关于 Google Professional Cloud Developer 认证的选择题，不显示答案，使用 “-” 或 “*” 表示选项。

回答：

以下是 50 道与 **Google Professional Cloud Developer** 认证目标保持一致的**原创多选题**。
每道题目提供**四个选项**，使用 `-` 或 `*` 标记。**不提供答案**，适用于自测或模拟考试。

---

### 1.

哪种 Google Cloud 服务最适合运行无需服务器管理且具有自动扩缩功能的无状态 HTTP 应用程序？

* Compute Engine
* Cloud Run
* Cloud Functions
* Google Kubernetes Engine

---

### 2.

Cloud Run 服务需要安全地访问 Cloud SQL 实例。推荐的方法是什么？

* 使用公网 IP 并将所有 Google IP 范围加入白名单
* 使用 Cloud SQL Auth Proxy
* 在源代码中存储数据库凭据
* 在不进行身份验证的情况下使用 VPC peering

---

### 3.

哪种 Google Cloud 产品专为服务之间的异步事件驱动消息传递而设计？

* Cloud Tasks
* Pub/Sub
* Cloud Scheduler
* Cloud Load Balancing

---

### 4.

Google Cloud service account 的主要目的是什么？

* 代表人类用户
* 管理结算账户
* 为应用程序和服务提供身份验证 (Authenticate)
* 存储应用程序 Secret

---

### 5.

哪种存储选项为 Google Cloud 中的对象存储提供强一致性 (strong consistency)？

* Persistent Disk
* Cloud Storage
* Filestore
* Bigtable

---

### 6.

单次调用 Cloud Functions (2nd gen) 的最大执行时间是多少？

* 1 分钟
* 9 分钟
* 15 分钟
* 60 分钟

---

### 7.

推荐使用哪种工具在 Google Cloud 上管理 infrastructure as code？

* Cloud Deployment Manager
* Cloud Shell Editor
* Terraform
* Cloud Build

---

### 8.

哪种 HTTP 负载均衡功能允许根据 URL 路径转发流量？

* Network Load Balancer
* Internal TCP Load Balancer
* HTTP(S) Load Balancer
* VPN Gateway

---

### 9.

Google Kubernetes Engine 中的默认部署单元是什么？

* Pod
* Service
* Deployment
* Node

---

### 10.

哪个命令用于将服务部署到 Cloud Run？

* gcloud run deploy
* gcloud app deploy
* gcloud functions deploy
* kubectl apply

---

### 11.

哪种 Google Cloud 数据库最适合全球分布且强一致性的关系型工作负载？

* Cloud SQL
* Firestore
* BigQuery
* Spanner

---

### 12.

Cloud Build 的主要目的是什么？

* 托管应用程序
* 运行 CI/CD 流水线
* 监控日志
* 管理 API

---

### 13.

哪种 Google Cloud 服务针对使用 SQL 进行大规模分析查询进行了优化？

* Cloud SQL
* Bigtable
* BigQuery
* Firestore

---

### 14.

如何安全地存储敏感配置数据并供应用程序访问？

* 代码中的环境变量
* Cloud Storage bucket
* Secret Manager
* Source repository

---

### 15.

哪种 GKE 功能可确保零停机时间部署？

* Node auto-repair
* Rolling updates
* Preemptible VM
* Static IP

---

### 16.

使用 managed instance groups 的主要好处是什么？

* 手动扩展 VM
* 自动扩缩 (Automatic scaling) 和自愈 (self-healing)
* 更便宜的存储
* 更快的网络

---

### 17.

哪种服务为 Google Cloud 资源提供集中式日志记录？

* Cloud Trace
* Cloud Monitoring
* Cloud Logging
* Error Reporting

---

### 18.

对于在 GKE 上运行的应用程序，访问 Google Cloud API 的推荐身份验证方法是什么？

* 将 service account key 存储为文件
* 手动生成的 OAuth token
* Workload Identity
* 嵌入代码中的 API key

---

### 19.

Kubernetes 中的 readiness probe 表示什么？

* 容器是否已启动
* 容器是否准备好接收流量
* 节点是否健康
* Pod 是否可以被调度

---

### 20.

哪种 Cloud Run 功能允许仅限内部服务进行私有访问？

* IAM 角色
* Ingress settings
* VPC Service Controls
* 防火墙规则

---

### 21.

哪种 Google Cloud 服务用于调度 cron 任务？

* Cloud Tasks
* Pub/Sub
* Cloud Scheduler
* Cloud Functions

---

### 22.

将 GKE 应用程序暴露给互联网的推荐方式是什么？

* NodePort service
* LoadBalancer service
* 结合 HTTP(S) Load Balancer 的 Ingress
* 直接访问 VM IP

---

### 23.

哪种工具有助于识别分布式应用程序中的性能瓶颈？

* Cloud Logging
* Cloud Trace
* Cloud Profiler
* Error Reporting

---

### 24.

哪种 Google Cloud 服务最适合键值 (key-value) 和宽列 (wide-column) NoSQL 工作负载？

* Firestore
* Bigtable
* Cloud SQL
* Memorystore

---

### 25.

当 Cloud Run 服务缩容至零 (scale to zero) 时会发生什么？

* 容器被暂停
* 容器被删除
* 没有实例运行，新请求将触发新实例
* 服务变得不可用

---

### 26.

哪种 GKE 网络模式会为每个 Pod 分配一个 VPC IP 地址？

* Routes-based
* NAT-based
* VPC-native
* Overlay networking

---

### 27.

Cloud Endpoints 的主要目的是什么？

* 数据库迁移
* API 管理和安全
* 负载均衡
* 日志记录和监控

---

### 28.

哪种 IAM 角色最适合对 Cloud Storage 对象进行只读访问？

* Storage Admin
* Storage Object Admin
* Storage Object Viewer
* Storage Viewer

---

### 29.

哪种 Google Cloud 服务提供内存数据存储以实现低延迟访问？

* Bigtable
* Firestore
* Memorystore
* Cloud SQL

---

### 30.

Cloud Build 使用哪种构建配置文件？

* Dockerfile
* cloudbuild.yaml
* build.gradle
* app.yaml

---

### 31.

哪个选项允许在 GKE 中进行蓝绿部署 (blue-green deployments)？

* Node pools
* 使用 Service 进行流量分割 (Traffic splitting)
* 滚动节点升级
* Preemptible node

---

### 32.

Cloud Tasks 的主要用例是什么？

* 批量数据处理
* 延迟和异步任务执行
* 实时流式分析
* 应用程序托管

---

### 33.

哪种 Google Cloud 服务会自动收集应用程序错误报告？

* Cloud Logging
* Cloud Monitoring
* Error Reporting
* Cloud Trace

---

### 34.

Cloud Storage 的哪项功能有助于降低不常用数据的成本？

* Multi-region bucket
* Object versioning
* Lifecycle management
* Strong consistency

---

### 35.

将本地系统安全连接到 Google Cloud 的推荐方式是什么？

* 配合防火墙规则的公网 IP
* Cloud VPN 或 Cloud Interconnect
* 仅使用 NAT Gateway
* 带有 SSL 的负载均衡器

---

### 36.

哪个部署平台使用 `app.yaml` 进行配置？

* Cloud Run
* Cloud Functions
* App Engine
* GKE

---

### 37.

哪种 Google Cloud 服务支持实时数据摄取和流处理？

* Dataflow
* Dataproc
* BigQuery
* Composer

---

### 38.

哪个 Kubernetes 对象为一组 Pod 提供稳定的网络？

* Pod
* Deployment
* Service
* ConfigMap

---

### 39.

哪项监控功能允许定义阈值并发送通知？

* Logs Explorer
* Metrics Explorer
* Alerting policies
* Trace Viewer

---

### 40.

哪种 Cloud SQL 功能可以提高读取可扩展性 (read scalability)？

* 垂直扩展 (Vertical scaling)
* Read replicas
* 高可用性故障转移 (High availability failover)
* 自动备份

---

### 41.

存储用于 Cloud Run 部署的 Docker 镜像的推荐方式是什么？

* Docker Hub
* Cloud Storage
* Artifact Registry
* Git repository

---

### 42.

哪种 Google Cloud 服务负责编排服务之间的工作流？

* Cloud Tasks
* Cloud Workflows
* Pub/Sub
* Cloud Scheduler

---

### 43.

哪个 Kubernetes 功能限制了容器的 CPU 和内存使用量？

* Node selector
* Resource requests and limits
* Taints and tolerations
* Pod affinity

---

### 44.

哪种 Google Cloud 产品最适合批量 Spark 工作负载？

* Dataflow
* Dataproc
* Bigtable
* Composer

---

### 45.

哪个 Cloud Run 设置控制每个容器的最大并发请求数？

* Instance limit
* CPU allocation
* Concurrency
* Timeout

---

### 46.

哪种 Google Cloud 服务提供分布式配置存储？

* Secret Manager
* Config Connector
* Firestore
* Cloud Storage

---

### 47.

零停机时间架构迁移的推荐方法是什么？

* 迁移期间停止流量
* 向后兼容的架构更改 (Backward-compatible schema changes)
* 手动数据库更新
* 禁用应用程序写入

---

### 48.

哪项 Google Cloud 功能会自动重启不健康的 VM？

* Live migration
* Autohealing policies
* Preemptible instances
* Shielded VMs

---

### 49.

哪种服务最适合处理 HTTP 流量的突然激增？

* 单个 Compute Engine VM
* 带有 autoscaling 的 managed instance group
* Cloud Storage
* Filestore

---

### 50.

哪种 Google Cloud 工具有助于分析一段时间内的应用程序 CPU 和内存使用情况？

* Cloud Logging
* Cloud Trace
* Cloud Profiler
* Error Reporting

---

如果你需要，我还可以：

* **单独生成答案**
* 将此转化为**限时模拟考试**
* 创建**基于场景的题目**
* 严格按照**官方考试大纲**调整题目