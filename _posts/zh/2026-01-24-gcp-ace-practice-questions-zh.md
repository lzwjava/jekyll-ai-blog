---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: GCP Associate Cloud Engineer 模拟试题
translated: true
type: note
---

问题：请提供 50 道 GCP Google Associate Cloud Engineer (ACE) 认证考试的选择题，不显示答案。

回答：

这里有 50 道涵盖 Associate Cloud Engineer 考试关键主题的选择题（包括设置环境、规划/实施解决方案、配置访问权限、部署/管理基础架构以及运营/监控）。每道题有四个选项（A-D）。

1. 哪个 Google Cloud 资源层次结构级别是附加结算且通常强制执行 Organization Policies 的根节点？  
   A) Folder  
   B) Project  
   C) Organization  
   D) Resource

2. 在不授予更广泛权限的情况下，授予用户在特定项目中创建 Compute Engine 实例能力的推荐方法是什么？  
   A) roles/compute.instanceAdmin  
   B) roles/compute.instanceAdmin.v1  
   C) roles/editor  
   D) roles/owner

3. 哪个命令可以使用 gcloud 创建一个新的 Google Cloud 项目？  
   A) gcloud projects create PROJECT_ID  
   B) gcloud init project PROJECT_ID  
   C) gcloud projects new PROJECT_ID  
   D) gcloud create project PROJECT_ID

4. 您需要授予 service account 从 Cloud Storage bucket 中读取对象的能力。您应该使用哪个预定义角色？  
   A) roles/storage.objectViewer  
   B) roles/storage.admin  
   C) roles/storage.objectCreator  
   D) roles/storage.legacyBucketReader

5. Cloud Storage 中的哪种存储类别最适合访问频率较低但仍需要毫秒级访问延迟的数据？  
   A) Standard  
   B) Nearline  
   C) Coldline  
   D) Archive

6. 如果没有另外设置生命周期规则，Nearline 存储类别 bucket 中的对象自动移至 Coldline 的默认天数是多少？  
   A) 30 days  
   B) 90 days  
   C) 180 days  
   D) Never

7. 哪个命令可以使用 gcloud 列出特定 zone 中的所有实例？  
   A) gcloud compute instances list --zone=ZONE  
   B) gcloud instances list --zone=ZONE  
   C) gcloud compute list instances --zone=ZONE  
   D) gcloud list compute instances --zone=ZONE

8. 您想根据 CPU 使用率创建一个具有 autoscaling 功能的 managed instance group。您需要配置哪个资源？  
   A) Autoscaler  
   B) Load Balancer  
   C) Health Check  
   D) Firewall rule

9. 对于需要全球分发和 SSL 终止的 HTTP(S) 流量，您应该使用哪种类型的负载均衡器？  
   A) TCP/SSL Proxy Load Balancer  
   B) HTTP(S) Load Balancer  
   C) Internal Load Balancer  
   D) Network Load Balancer

10. 哪项服务是 serverless 的，且最适合由 HTTP 请求触发的容器化工作负载？  
    A) Cloud Functions  
    B) Cloud Run  
    C) App Engine Standard  
    D) Compute Engine

11. 在 Cloud Run 中，CPU 和内存使用的计费单位是什么？  
    A) Per request  
    B) vCPU-second and GiB-second  
    C) Per container instance  
    D) Per deployment

12. 哪种 IAM 成员类型代表 Google Workspace group？  
    A) user:  
    B) serviceAccount:  
    C) group:  
    D) domain:

13. 您需要允许运行在 Compute Engine 上的应用程序调用 Cloud Storage API 而无需嵌入凭据。您应该使用什么？  
    A) 附加到 VM 的 Service account  
    B) API key  
    C) OAuth 2.0 client ID  
    D) Access key

14. 哪种 VPC 网络类型允许您使用自定义子网和手动 IP 范围？  
    A) Auto mode  
    B) Custom mode  
    C) Legacy mode  
    D) Shared VPC

15. Google Cloud 中 Cloud NAT 的目的是什么？  
    A) 为出站流量将私有 IP 转换为公有 IP  
    B) 对内部流量进行负载均衡  
    C) 为私有 VM 提供入站连接  
    D) 加密区域之间的流量

16. 哪个命令用于部署 App Engine 应用程序的新版本？  
    A) gcloud app deploy  
    B) gcloud app create version  
    C) gcloud deploy app  
    D) gcloud app versions deploy

17. 在 Kubernetes Engine 中，哪个组件负责将 pod 调度到节点上？  
    A) kubelet  
    B) kube-scheduler  
    C) kube-controller-manager  
    D) etcd

18. 哪种 GKE 模式提供完全托管的 control plane 并减少了操作开销？  
    A) Standard mode  
    B) Autopilot mode  
    C) Enterprise mode  
    D) Classic mode

19. 您需要在 Kubernetes 中存储可以挂载为卷或环境变量的敏感配置数据。您应该使用哪个资源？  
    A) ConfigMap  
    B) Secret  
    C) PersistentVolumeClaim  
    D) ServiceAccount

20. Google Cloud 资源的主要监控工具是什么？  
    A) Cloud Trace  
    B) Cloud Monitoring  
    C) Cloud Logging  
    D) Cloud Debugger

21. 在 Google Cloud 中，哪项服务用于收集、索引和存储日志数据？  
    A) Cloud Monitoring  
    B) Cloud Logging  
    C) Cloud Trace  
    D) Operations Suite

22. Cloud Monitoring 中 uptime check 的目的是什么？  
    A) 监控 CPU 使用率  
    B) 检查公共端点的可用性  
    C) 跟踪请求延迟  
    D) 磁盘空间警报

23. 哪个命令可以将日志从 Cloud Logging 导出到 BigQuery？  
    A) 创建一个以 BigQuery 为目的地的 log sink  
    B) gcloud logging export  
    C) gcloud logging sinks create  
    D) A 和 C 都是

24. 您需要授予开发人员临时的提升权限以排查生产问题。最佳实践是什么？  
    A) 临时给予他们 roles/owner  
    B) 使用带有基于时间的访问权限的 IAM Conditions  
    C) 共享 service account 密钥  
    D) 将他们作为 editor 添加到项目中

25. 哪项功能允许多个项目共享同一个 VPC 网络？  
    A) VPC Peering  
    B) Shared VPC  
    C) Cloud Interconnect  
    D) Cloud VPN

26. 默认情况下，每个项目的自定义 VPC 网络最大数量是多少？  
    A) 1  
    B) 5  
    C) 10  
    D) 无限制

27. 哪种磁盘类型每 GB 成本最低，但不属于 SSD？  
    A) Balanced Persistent Disk  
    B) Standard Persistent Disk  
    C) SSD Persistent Disk  
    D) Extreme Persistent Disk

28. 您需要备份 Compute Engine 磁盘。您应该使用哪项服务？  
    A) Cloud Scheduler  
    B) Snapshot  
    C) Cloud Backup  
    D) Persistent Disk clone

29. Cloud Storage 生命周期规则的目的是什么？  
    A) 根据条件自动删除或转换对象  
    B) 加密对象  
    C) 设置保留策略  
    D) A 和 C 都是

30. 哪个命令将文件从本地复制到 Cloud Storage bucket？  
    A) gsutil cp  
    B) gcloud storage cp  
    C) gsutil rsync  
    D) A 和 B 都是

31. 在 IAM 中，最小权限原则（principle of least privilege）建议是什么？  
    A) 向所有用户授予 owner 角色  
    B) 仅授予执行任务所需的权限  
    C) 仅使用基本角色  
    D) 避免使用自定义角色

32. 哪项服务最适合运行需要扩展到数千个实例的无状态批处理作业？  
    A) Cloud Run jobs  
    B) Compute Engine VMs  
    C) App Engine Flexible  
    D) Cloud Functions

33. 创建资源时未指定位置的默认区域（region）是什么？  
    A) us-central1  
    B) 无默认值 - 必须指定  
    C) global  
    D) europe-west1

34. 哪项 Google Cloud 服务提供托管的 PostgreSQL 兼容数据库？  
    A) Cloud SQL  
    B) Firestore  
    C) Bigtable  
    D) AlloyDB

35. 您需要允许在没有公共 IP 的情况下对 Compute Engine VM 进行 SSH 访问。您应该使用什么？  
    A) 用于 TCP 转发的 Cloud IAP  
    B) Bastion host  
    C) Cloud VPN  
    D) 以上所有

36. gcloud auth application-default login 命令的作用是什么？  
    A) 在本地工具中进行用户凭据身份验证  
    B) 创建 service account 密钥  
    C) 登录 gcloud SDK  
    D) 在 VM 上启用 ADC

37. 默认情况下，哪种负载均衡器会保留源客户端 IP？  
    A) HTTP(S) Load Balancer  
    B) SSL Proxy Load Balancer  
    C) Internal TCP/UDP Load Balancer  
    D) TCP Proxy Load Balancer

38. 在 GKE Autopilot 中，谁负责管理节点？  
    A) 客户  
    B) Google  
    C) 双方共同  
    D) 不存在节点

39. 哪个命令可以扩展 managed instance group？  
    A) gcloud compute instance-groups managed resize  
    B) gcloud compute mig scale  
    C) gcloud compute instances resize-group  
    D) gcloud resize mig

40. 推荐的 Terraform 与 Google Cloud 身份验证方式是什么？  
    A) Service account 密钥文件  
    B) Application Default Credentials  
    C) gcloud auth application-default login  
    D) B 和 C 都是

41. 哪项服务是流数据实时分析的理想选择？  
    A) BigQuery  
    B) Dataflow  
    C) Pub/Sub + Dataflow  
    D) Dataproc

42. 防火墙规则优先级（priority）的目的是什么？  
    A) 数字越低 = 优先级越高  
    B) 数字越高 = 优先级越高  
    C) 没有优先级 - 第一个匹配的生效  
    D) 仅针对出站流量设置优先级

43. 哪个角色允许查看（但不修改）项目中的大多数资源？  
    A) roles/viewer  
    B) roles/browser  
    C) roles/reader  
    D) roles/monitoring.viewer

44. 您正在将本地 MySQL 数据库迁移到 Google Cloud。哪项服务提供了最简单的 lift-and-shift 方案？  
    A) Cloud SQL  
    B) Bare Metal Solution  
    C) Datastream  
    D) Database Migration Service

45. Cloud Billing 导出到 BigQuery 的功能可以实现什么？  
    A) 详细的成本分析和报告  
    B) 自动预算警报  
    C) 实时结算仪表板  
    D) 仅 A

46. 哪个选项不是 Compute Engine 中有效的机器系列（machine family）？  
    A) E2  
    B) N2  
    C) T2  
    D) C2

47. 在 Cloud Functions 中，第 2 代函数的最大超时时间是多少？  
    A) 9 minutes  
    B) 60 minutes  
    C) 540 seconds  
    D) 3600 seconds

48. 哪项服务提供托管的 Redis 兼容内存缓存？  
    A) Memorystore for Redis  
    B) Cloud SQL  
    C) Firestore in Datastore mode  
    D) Bigtable

49. 在 Cloud Storage 中使用客户管理的加密密钥 (CMEK) 需要什么？  
    A) Cloud KMS 密钥  
    B) 默认的 Google 管理密钥  
    C) A 和 B 均需要  
    D) 仅 A

50. 哪个 gcloud 命令显示当前的活动配置（active configuration）？  
    A) gcloud config list  
    B) gcloud config current  
    C) gcloud configuration active  
    D) gcloud config show

参考资料：

- https://cloud.google.com/learn/certification/cloud-engineer
- https://cloud.google.com/learn/certification/guides/cloud-engineer