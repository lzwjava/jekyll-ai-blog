---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: GKE 上的 NGINX Ingress 控制器
translated: true
type: note
---

Question: Introduction to NGINX Ingress Controller in GCP

Answer:

**NGINX Ingress Controller** 是在 Kubernetes 集群（包括 Google Cloud Platform (GCP) 中的 **Google Kubernetes Engine (GKE)**）中公开 HTTP/HTTPS 服务最流行的方式之一。

### 什么是 Kubernetes 中的 Ingress？

**Ingress** 是一个 Kubernetes API 对象，用于管理集群内服务的外部访问（主要是 HTTP 和 HTTPS）。它提供：
- Load balancing
- SSL/TLS termination
- 基于名称的 Virtual hosting
- 基于路径的 Routing

然而，Kubernetes 本身并**不**包含内置的 Ingress controller 实现——它仅定义了 API。你需要安装一个实际执行该 API 的 controller。

### NGINX Ingress Controller vs GKE 内置 Ingress

| Feature                          | GKE Built-in Google Cloud Load Balancer Ingress | NGINX Ingress Controller                     |
|----------------------------------|--------------------------------------------------|----------------------------------------------|
| Controller type                  | Google-managed (GCLB)                            | Community / F5 NGINX open-source             |
| Load balancer provisioned        | External HTTP(S) Load Balancer                   | Also External HTTP(S) Load Balancer          |
| Setup complexity                 | Very simple (`type: Ingress`)                    | Requires installing controller first         |
| Features                         | Good integration with Google Cloud features      | Much richer annotations & configuration      |
| Advanced routing                 | Basic                                            | Excellent (regex, rewrites, rate limiting, auth, canary, mirroring, …) |
| TLS termination                  | At Google Cloud Load Balancer                    | At NGINX or at Google LB (both possible)     |
| Cost                             | Google LB charges apply                          | Same LB charges + node costs                 |
| Best for                         | Simple setups, Google ecosystem preference       | Complex routing, advanced features, multi-cloud |

当团队需要比原生 GKE Ingress 提供更强大的 Routing 能力时，大多数会选择 **NGINX Ingress**。

### NGINX Ingress 在 GKE 上如何工作（高层架构）

1. 你在 GKE 集群中将 **NGINX Ingress Controller** 部署为 Deployment + Service (type LoadBalancer)。
2. GKE 会自动在其前面配置一个 Google Cloud **HTTP(S) Load Balancer**。
3. Controller 会监听集群中的 Ingress 对象。
4. 当你创建一个 Ingress 资源时，NGINX 会动态配置以按需路由流量。

### GKE 安装方法快速对比 (2025/2026)

- **Official manifests** (最常见)  
  `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.x/deploy/static/provider/cloud/deploy.yaml`

- **Helm** (非常流行)  
  ```bash
  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
  helm repo update
  helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace
  ```

- **F5 NGINX Ingress Controller** (具有额外企业级功能的商业版本)

### 最小使用示例

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"           # 在 GKE 上非常重要
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx                         # 在新版本中推荐的方式
  rules:
  - host: api.yourdomain.com
    http:
      paths:
      - path: /api(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
```

### 人们在 GKE 上选择 NGINX Ingress 的典型原因

- 非常强大的 Annotation 集合（auth, rate-limit, circuit-breaker, canary deployments, blue-green, regex paths, …）
- 对 gRPC, WebSocket 长连接有更好的支持
- 对 Redirects / Rewrites 有更精细的控制
- 易于并行运行多个 Ingress controller（例如 blue vs green, public vs internal）
- 跨云的一致行为（GKE + EKS + AKS + on-prem）

### 总结建议 (2026)

- 需要简单设置 + 深度 Google 集成 → 使用 **GKE native Ingress**
- 需要高级 Routing / Annotations / Canaries / Auth / Regex → 使用 **NGINX Ingress Controller**

References:  

- [Kubernetes Ingress-NGINX Official Documentation](https://kubernetes.github.io/ingress-nginx/)
- [ExternalDNS with NGINX on GKE](https://kubernetes-sigs.github.io/external-dns/latest/docs/tutorials/gke-nginx)
- [Google Cloud - Ingress Configuration Overview](https://cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration)