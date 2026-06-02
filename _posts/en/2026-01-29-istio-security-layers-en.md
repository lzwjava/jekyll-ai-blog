---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Istio Security Layers Explained Clearly
translated: false
type: note
---

Question: What are Istio AuthorizationPolicy, Kubernetes NetworkPolicy, and mTLS? Please explain their purposes, differences, and how they relate to each other.

Answer:

These are three different but complementary security mechanisms used in Kubernetes environments, especially when Istio is involved. Here's a clear breakdown:

### 1. **Kubernetes NetworkPolicy** (L3/L4 network-level access control)

- **Layer**: Operates at OSI Layer 3 (IP) and Layer 4 (TCP/UDP ports).
- **Scope**: Controls pod-to-pod traffic at the network level.
- **Enforced by**: Kubernetes CNI plugins (e.g., Calico, Cilium, Weave, etc.). Istio does **not** enforce or replace NetworkPolicy.
- **What it can do**:
  - Allow/deny traffic based on pod labels, namespaces, IP blocks (CIDR).
  - Control ingress/egress at the port & protocol level.
  - Example: "Only allow pods with label app=frontend in namespace prod to connect to port 8080 of pods with app=backend".
- **Limitation**:
  - No identity awareness (doesn't know HTTP, gRPC, or user identity).
  - No application-layer (L7) policies like HTTP path/method-based routing.
  - Cannot enforce encryption (mTLS).

### 2. **Istio AuthorizationPolicy** (L7/application-level authorization + identity-aware)

- **Layer**: OSI Layer 7 (HTTP, gRPC, etc.).
- **Scope**: Controls access inside the Istio service mesh (traffic that goes through Envoy sidecar proxies).
- **Enforced by**: Istio's Envoy sidecar proxies.
- **What it can do**:
  - Authorization based on JWT claims, source identity (SPIFFE), headers, paths, methods, etc.
  - Very fine-grained rules:

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

- **Key advantage**: Identity-based (uses mTLS-provided identities), works with JWT, supports DENY policies, condition-based rules.
- Works **only** on traffic that passes through Istio proxies (i.e., inside the mesh).

### 3. **mTLS (mutual TLS) in Istio**

- **Purpose**: Provides encryption + strong service identity.
- **How it works in Istio**:
  - Istio automatically provisions X.509 certificates to every workload via istiod.
  - All mesh-internal traffic between sidecars is encrypted with mTLS by default (when set to STRICT).
  - Each service gets a strong identity: `cluster.local/ns/{namespace}/sa/{service-account}` (SPIFFE format).
- **Modes in Istio** (`PeerAuthentication`):
  - `STRICT`: Enforces mTLS (recommended in production).
  - `PERMISSIVE`: Allows both mTLS and plaintext (useful during migration).
- **Critical role**: Without mTLS, Istio AuthorizationPolicy has **no reliable source identity** → policies that depend on `request.auth.principal` or `source.principal` become weak or ineffective.

### Relationship and Best Practice Summary

| Feature                        | Kubernetes NetworkPolicy | Istio AuthorizationPolicy | Istio mTLS            |
|-------------------------------|---------------------------|---------------------------|-----------------------|
| Layer                         | L3/L4                    | L7                        | L4 (transport) + identity |
| Enforced by                   | CNI (Calico, Cilium, etc.) | Envoy sidecar            | Envoy sidecar         |
| Identity aware                | No                       | Yes (via mTLS or JWT)     | Provides the identity |
| Encryption                    | No                       | No (relies on mTLS)       | Yes                   |
| HTTP path/method control      | No                       | Yes                       | No                    |
| Works outside mesh            | Yes                      | No                        | No                    |
| Recommended in Istio clusters  | Yes (defense in depth)   | Yes (primary L7 control)  | Yes (STRICT mode)     |

### Recommended Secure Setup in Istio + Kubernetes

1. Enable **Istio mTLS in STRICT mode** globally (via `PeerAuthentication` or `DestinationRule`).
2. Use **Istio AuthorizationPolicy** as your primary mechanism for fine-grained access control (who can call what API).
3. Keep **Kubernetes NetworkPolicy** for:
   - Defense in depth.
   - Blocking traffic that bypasses the mesh (e.g., init containers, host networking pods, ingress from outside).
   - Egress control to external services.

In short:
**mTLS** gives you encryption + strong identities → **Istio AuthorizationPolicy** uses those identities for L7 authorization → **Kubernetes NetworkPolicy** adds an extra L3/L4 safety net.

They are not mutually exclusive — in a production Istio setup, you should use all three together.
