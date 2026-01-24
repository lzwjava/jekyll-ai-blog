---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5.2
title: Google Kubernetes Engine 入门
translated: true
type: note
---

Question: Introduction to Google Kubernetes Engine (GKE) in Google Cloud

Answer:

## Introduction to Google Kubernetes Engine (GKE)

**Google Kubernetes Engine (GKE)** 是由 **Google Cloud Platform (GCP)** 提供的托管型 Kubernetes 服务。它允许你使用 **Kubernetes** 部署、管理和扩展容器化应用程序，而无需手动管理底层基础设施。

简单来说：

> GKE 让你能够大规模运行 Docker 容器，并由 Google 处理大部分操作复杂性。

---

## What is Kubernetes (Quick Context)

在了解 GKE 之前，先了解 Kubernetes 会有所帮助：

* **Kubernetes (K8s)** 是一个开源的容器编排系统
* 它的自动化功能包括：

  * 容器部署
  * Scaling（扩缩容）
  * Load balancing（负载均衡）
  * Self-healing（自愈，重启失败的容器）
* 最初由 Google 开发，现在由 CNCF 维护

GKE 是 Google 提供的 **托管和管理** 版本的 Kubernetes。

---

## Core Components of GKE

### 1. Cluster

**GKE cluster** 是主要资源。它由以下部分组成：

* **Control Plane**（由 Google 管理）
* **Worker Nodes**（运行容器的 VM）

---

### 2. Control Plane (Managed by Google)

包括：

* Kubernetes API Server
* Scheduler
* Controller Manager
* etcd (cluster 状态数据库)

✅ 你 **不需要管理** GKE 中的这些组件（这是一个巨大的优势）。

---

### 3. Nodes & Node Pools

* **Nodes** 是 Compute Engine VM
* **Node Pools** 将具有相同配置的 Node 分组
* 不同的 Pool 可以拥有：

  * 不同的 Machine types
  * 不同的 Autoscaling 规则
  * 不同的 Workloads

---

### 4. Pods

* Kubernetes 中最小的可部署单元
* 一个 Pod 包含：

  * 一个或多个容器
  * 共享的网络和存储

---

## Key Features of GKE

### 1. Fully Managed Kubernetes

* Google 负责处理：

  * Master 节点的升级
  * 安全补丁
  * High availability（高可用性）
* 显著减轻了运维负担

---

### 2. Auto Scaling

* **Horizontal Pod Autoscaling (HPA)**：根据 CPU/内存使用情况扩展 Pod
* **Cluster Autoscaler**：自动添加/移除 Node
* **Vertical Pod Autoscaling (VPA)**：调整资源请求

---

### 3. High Availability

* Multi-zone 和 Regional clusters
* 自动 Node 修复
* Workloads 自愈

---

### 4. Integrated Security

* IAM 集成
* Workload Identity
* Private clusters
* Shielded VMs
* Binary Authorization

---

### 5. Deep GCP Integration

GKE 与以下服务无缝集成：

* Cloud Load Balancing
* Cloud Monitoring & Logging
* Artifact Registry
* Cloud IAM
* Cloud Storage & Persistent Disks

---

## Deployment Workflow (Typical)

1. 构建容器镜像 (Docker)
2. 将镜像推送到 Artifact Registry
3. 创建一个 GKE cluster
4. 定义 Kubernetes manifests (YAML)

   * Deployment
   * Service
   * ConfigMap / Secret
5. 使用 `kubectl` 进行部署
6. 通过 LoadBalancer 或 Ingress 暴露服务

---

## GKE Cluster Modes

### 1. Standard Mode

* 你管理 Node 配置
* 更多的控制权，更多的责任
* 常用于生产环境的 Workloads

### 2. Autopilot Mode

* Google 管理 Node 和 Scaling
* 按 Pod 资源使用情况付费
* 强大的默认设置，灵活性较低
* 非常适合希望最小化运维工作的团队

---

## Common Use Cases

* Microservices（微服务）架构
* Web 应用程序和 API
* CI/CD 平台
* Machine learning 推理
* Hybrid 和 Multi-cloud 工作负载

---

## Advantages of GKE

* 生产级别的 Kubernetes
* 强大的可靠性和性能
* 一流的 Autoscaling 能力
* 减少运维开销
* 原生的 Kubernetes 体验

---

## Challenges / Considerations

* Kubernetes 有一定的学习曲线
* 如果没有适当的资源管理，成本可能会增加
* 需要理解容器和 Networking

---

## When to Use GKE

在以下情况使用 GKE：

* 你需要可扩展的容器编排
* 你想要托管的 Kubernetes
* 你正在构建 Cloud-native 或微服务系统
* 你已经在使用 Google Cloud 服务

---

## Summary

**GKE = Kubernetes + Google 的可靠性 + 托管运维**

它是最成熟、最强大的托管 Kubernetes 平台之一，适用于初创公司和大规模企业系统。

References:

* [https://cloud.google.com/kubernetes-engine](https://cloud.google.com/kubernetes-engine)
* [https://kubernetes.io/docs/home/](https://kubernetes.io/docs/home/)
* [https://cloud.google.com/architecture/kubernetes](https://cloud.google.com/architecture/kubernetes)