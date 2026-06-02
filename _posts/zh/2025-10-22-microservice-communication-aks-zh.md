---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在AKS中配置微服务通信
translated: true
type: note
---

### 在 Azure Kubernetes 服务 (AKS) 中配置微服务间通信

在 Azure Kubernetes 服务 (AKS) 中，微服务通常作为由 **Deployment** 管理的 **Pod** 进行部署。为使它们能够相互通信（例如服务 A 调用服务 B），需要使用 **Kubernetes Service** 来抽象 Pod 的动态 IP 并提供稳定端点。这是通过内部网络利用 Kubernetes 内置的 DNS 解析实现的。以下是一步步的配置和实施指南。

#### 1. **将微服务部署为 Deployments**
   每个微服务运行在一个 Pod（或一组用于扩展的 Pod）中。使用 Deployment 来管理它们。

   简单微服务 Deployment 的 YAML 示例 (`service-a-deployment.yaml`)：
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: service-a
     namespace: default  # 或您的自定义命名空间
   spec:
     replicas: 3  # 按需扩展
     selector:
       matchLabels:
         app: service-a
     template:
       metadata:
         labels:
           app: service-a
       spec:
         containers:
         - name: service-a
           image: your-registry/service-a:latest  # 例如，ACR 或 Docker Hub 镜像
           ports:
           - containerPort: 8080  # 您的应用监听的端口
   ```

   应用它：
   ```
   kubectl apply -f service-a-deployment.yaml
   ```

   为其他服务（例如 `service-b`）重复此步骤。

#### 2. **使用 Services 暴露微服务**
   为每个微服务创建一个 **ClusterIP Service**。此类型仅用于内部通信（不暴露到集群外部）。它对流量进行负载均衡到 Pod，并提供 DNS 名称。

   服务 A 的 YAML 示例 (`service-a-service.yaml`)：
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: service-a
     namespace: default
   spec:
     selector:
       app: service-a  # 匹配 Deployment 标签
     ports:
     - protocol: TCP
       port: 80  # Service 端口（调用者使用的端口）
       targetPort: 8080  # Pod 的容器端口
     type: ClusterIP  # 仅内部
   ```

   应用它：
   ```
   kubectl apply -f service-a-service.yaml
   ```

   对服务 B 执行相同操作。现在，Pod 可以通过 Service 的 DNS 名称相互访问。

#### 3. **微服务如何相互调用**
   - **基于 DNS 的发现**：Kubernetes DNS 自动解析 Service 名称。从服务 A 中的 Pod 调用服务 B 时使用：
     - `<service-name>.<namespace>.svc.cluster.local`（完全限定名称，例如 `service-b.default.svc.cluster.local`）。
     - 如果在同一命名空间中，只需 `<service-name>`（例如 `service-b`）。
   - **HTTP/gRPC 调用**：在您的应用代码中，向 `http://service-b:80/endpoint` 发出请求。Kubernetes 处理负载均衡和故障转移。
     - Python 示例（使用 requests）：
       ```python
       import requests
       response = requests.get("http://service-b:80/api/data")
       ```
     - 对于 gRPC，使用相同的主机名和 gRPC 端口。
   - **端口映射**：Service 端口（例如 80）映射到 Pod 的目标端口（例如 8080）。无需硬编码 Pod IP——它们在重启时会更改。

   从 Pod 测试连通性：
   ```
   kubectl exec -it <pod-name-in-service-a> -- curl http://service-b:80/health
   ```

#### 4. **高级配置选项**
   - **命名空间**：将服务部署在不同的命名空间中以实现隔离。使用完全限定 DNS（例如 `service-b.other-ns.svc.cluster.local`）。
   - **网络策略**：使用 Calico 或 Azure CNI 策略保护通信，以允许/拒绝服务之间的流量。
     允许服务 A 调用服务 B 的策略示例：
     ```yaml
     apiVersion: networking.k8s.io/v1
     kind: NetworkPolicy
     metadata:
       name: allow-service-a-to-b
     spec:
       podSelector:
         matchLabels:
           app: service-b
       policyTypes:
       - Ingress
       ingress:
       - from:
         - podSelector:
             matchLabels:
               app: service-a
         ports:
         - protocol: TCP
           port: 80
     ```
   - **服务网格（例如 Istio 或 Linkerd）**：对于生产环境，添加网格以实现可观测性、mTLS 和流量管理。通过 Helm 在 AKS 上安装，然后将 sidecar 代理注入到 Pod 中。
   - **外部访问（如果需要）**：使用 **LoadBalancer** 或 **Ingress** Services 进行出站调用，但对于内部通信坚持使用 ClusterIP。

#### 5. **最佳实践**
   - 使用 **环境变量** 或 **ConfigMaps** 将 Service DNS 名称动态注入到应用中。
   - 使用 Azure Monitor for AKS 监控服务间流量。
   - 基于 CPU/内存使用情况，使用 Horizontal Pod Autoscaler (HPA) 进行水平扩展。
   - 对于 Azure 特定的集成，使用 Azure Container Registry (ACR) 存储镜像，使用 Azure AD 进行身份验证。

此设置确保了可靠、可扩展的通信，而无需紧密耦合。从基本的 Services 开始，然后根据需要添加安全/网格层。

[AKS 网络概述](https://learn.microsoft.com/en-us/azure/aks/concepts-network)
[Kubernetes Services 文档](https://kubernetes.io/docs/concepts/services-networking/service/)
[AKS 微服务教程](https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-deploy-cluster)
