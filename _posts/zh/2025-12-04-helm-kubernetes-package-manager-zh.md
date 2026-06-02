---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Helm Kubernetes 包管理器
translated: true
type: note
---

Question: What is Helm in software?

Answer:

Helm 是 Kubernetes 的包管理器，通常被称为“Kubernetes 版的 apt、yum 或 Homebrew”。

它通过将所有相关的 Kubernetes 资源（Deployments、Services、ConfigMaps 等）打包成一个称为 **chart** 的单一单元，简化了 Kubernetes 集群上应用程序的部署、管理和升级。

### 核心概念
- **Chart**：一个 Helm 包，包含：
  - 用于 Kubernetes manifests 的 YAML 模板
  - 默认配置值（在 `values.yaml` 中）
  - 辅助文件和脚本
- **Release**：部署到集群的 chart 的特定实例（您可以拥有同一个 chart 的多个具有不同配置的 release）。
- **Repository**：Charts 托管和共享的存储位置（通常是 HTTP/S）（例如，Artifact Hub 是官方公共 repo）。

### 常用命令
```bash
helm search hub nginx          # 查找 chart
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-nginx bitnami/nginx   # 部署 chart
helm upgrade my-nginx bitnami/nginx --set replicaCount=5
helm rollback my-nginx 1       # 回滚到上一个 release
helm uninstall my-nginx        # 删除 release
```

### Helm 版本
- **Helm 2**（较旧，现已弃用）：使用一个名为 Tiller 的服务端组件。
- **Helm 3**（当前版本，自 2019 年起）：完全是客户端，没有 Tiller，具有更好的安全性和 RBAC 支持。

简而言之，Helm 使复杂的 Kubernetes 应用程序部署变得可重复、有版本控制和可配置——将其视为将杂乱的 YAML 文件堆转变为可管理、可共享的软件包的工具。

参考资料：
- [Helm Official Documentation](https://helm.sh/docs/)
- [Artifact Hub](https://artifacthub.io/)
