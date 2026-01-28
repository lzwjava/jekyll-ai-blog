---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Istio 安全层详解
translated: true
type: note
---

这些是 Kubernetes 环境中使用的三种不同但互补的安全机制，尤其是在涉及 Istio 时。以下是清晰的分解：

### 1. **Kubernetes NetworkPolicy** (L3/L4 网络级访问控制)

- **Layer**：在 OSI Layer 3 (IP) 和 Layer 4 (TCP/UDP 端口) 上运行。
- **Scope**：在网络级别控制 pod 到 pod 的流量。
- **Enforced by**：Kubernetes CNI 插件（例如 Calico、Cilium、Weave 等）。Istio **不会**强制执行或替换 NetworkPolicy。
- **What it can do**：
  - 基于 pod 标签、命名空间、IP 块 (CIDR) 允许/拒绝流量。
  - 在端口和协议级别控制 ingress/egress。
  - 示例：“仅允许命名空间 prod 中标签为 app=frontend 的 pod 连接到标签为 app=backend 的 pod 的端口 8080”。
- **Limitation**： 
  - 无身份感知（不知道 HTTP、gRPC 或用户身份）。
  - 无应用层 (L7) 策略，如基于 HTTP 路径/方法的路由。
  - 无法强制加密 (mTLS)。

### 2. **Istio AuthorizationPolicy** (L7/应用级授权 + 身份感知)

- **Layer**：OSI Layer 7 (HTTP、gRPC 等)。
- **Scope**：控制 Istio service mesh 内部的访问（通过 Envoy sidecar proxy 的流量）。
- **Enforced by**：Istio 的 Envoy sidecar proxy。
- **What it can do**：
  - 基于 JWT claims、源身份 (SPIFFE)、headers、paths、methods 等进行授权。
  - 非常细粒度的规则：
    ```yaml
    apiVersion: security.istio.io/v1beta1
    kind: AuthorizationPolicy
    metadata:
      name: httpbin-allow-get
      namespace: foo
    spec:
      selector:
        matchLabels:
          app: httpbin
      action: ALLOW
      rules:
      - when:
        - key: request.auth.principal
          values: ["cluster.local/ns/default/sa/admin"]
        to:
        - operation:
            methods: ["GET"]
            paths: ["/public/*"]
      - when:
        - key: request.headers[authorization]
          values: ["Bearer valid-token-*"]
    ```
- **Key advantage**：基于身份（使用 mTLS 提供的身份），支持 JWT，支持 DENY 策略，基于条件的规则。
- 仅适用于通过 Istio proxy 的流量（即 mesh 内部）。

### 3. **mTLS (mutual TLS) in Istio**

- **Purpose**：提供加密 + 强大的服务身份。
- **How it works in Istio**：
  - Istio 通过 istiod 自动为每个 workload 提供 X.509 证书。
  - 默认情况下（设置为 STRICT 时），sidecar 之间的所有 mesh 内部流量使用 mTLS 加密。
  - 每个服务获得强大的身份：`cluster.local/ns/{namespace}/sa/{service-account}` (SPIFFE 格式)。
- **Modes in Istio** (`PeerAuthentication`)：
  - `STRICT`：强制 mTLS（生产环境推荐）。
  - `PERMISSIVE`：允许 mTLS 和明文（迁移期间有用）。
- **Critical role**：没有 mTLS，Istio AuthorizationPolicy 将**没有可靠的源身份** → 依赖 `request.auth.principal` 或 `source.principal` 的策略将变得薄弱或无效。

### Relationship and Best Practice Summary

| 特性                          | Kubernetes NetworkPolicy | Istio AuthorizationPolicy | Istio mTLS            |
|-------------------------------|---------------------------|---------------------------|-----------------------|
| Layer                         | L3/L4                    | L7                        | L4 (transport) + identity |
| Enforced by                   | CNI (Calico, Cilium, etc.) | Envoy sidecar            | Envoy sidecar         |
| Identity aware                | No                       | Yes (via mTLS or JWT)     | Provides the identity |
| Encryption                    | No                       | No (relies on mTLS)       | Yes                   |
| HTTP path/method control      | No                       | Yes                       | No                    |
| Works outside mesh            | Yes                      | No                        | No                    |
| Recommended in Istio clusters  | Yes (defense in depth)   | Yes (primary L7 control)  | Yes (STRICT mode)     |

### Recommended Secure Setup in Istio + Kubernetes

1. 全局启用 **Istio mTLS 在 STRICT 模式**（通过 `PeerAuthentication` 或 `DestinationRule`）。
2. 使用 **Istio AuthorizationPolicy** 作为细粒度访问控制的主要机制（谁可以调用哪个 API）。
3. 保留 **Kubernetes NetworkPolicy** 用于：
   - 防御纵深。
   - 阻止绕过 mesh 的流量（例如 init containers、host networking pod、外部 ingress）。
   - 到外部服务的 egress 控制。

简而言之：  
**mTLS** 提供加密 + 强大身份 → **Istio AuthorizationPolicy** 使用这些身份进行 L7 授权 → **Kubernetes NetworkPolicy** 添加额外的 L3/L4 安全网。

它们并不相互排斥 — 在生产 Istio 设置中，应一起使用所有三个。