---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: NGINX Ingress Controller on GKE
translated: false
type: note
---

Question: Introduction to NGINX Ingress Controller in GCP

Answer:

The **NGINX Ingress Controller** is one of the most popular ways to expose HTTP/HTTPS services in Kubernetes clusters, including those running on **Google Kubernetes Engine (GKE)** in Google Cloud Platform (GCP).

### What is an Ingress in Kubernetes?

An **Ingress** is a Kubernetes API object that manages external access (mainly HTTP and HTTPS) to services inside the cluster. It provides:

- Load balancing
- SSL/TLS termination
- Name-based virtual hosting
- Path-based routing

However, Kubernetes itself does **not** include a built-in Ingress controller implementation — it only defines the API. You need to install a controller that actually implements this API.

### NGINX Ingress Controller vs GKE's built-in Ingress

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

Most teams choose **NGINX Ingress** when they need more powerful routing capabilities than what the native GKE Ingress offers.

### How NGINX Ingress Works on GKE (High-level)

1. You deploy the **NGINX Ingress Controller** as a Deployment + Service (type LoadBalancer) in your GKE cluster.
2. GKE automatically provisions a Google Cloud **HTTP(S) Load Balancer** in front of it.
3. The controller watches for Ingress objects in the cluster.
4. When you create an Ingress resource, NGINX gets configured dynamically to route traffic accordingly.

### Quick Comparison of Installation Methods on GKE (2025/2026)

- **Official manifests** (most common)
  `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.x/deploy/static/provider/cloud/deploy.yaml`

- **Helm** (very popular)

  ```bash
  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
  helm repo update
  helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace
  ```

- **F5 NGINX Ingress Controller** (commercial version with extra enterprise features)

### Minimal Example Usage

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"           # important on GKE
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx                         # recommended way in newer versions
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

### Typical Reasons People Choose NGINX Ingress on GKE

- Very powerful annotation set (auth, rate-limit, circuit-breaker, canary deployments, blue-green, regex paths, …)
- Better support for gRPC, WebSocket long-lived connections
- More fine-grained control over redirects / rewrites
- Easier to run multiple Ingress controllers side-by-side (blue vs green, public vs internal)
- Consistent behavior across clouds (GKE + EKS + AKS + on-prem)

### Summary Recommendation (2026)

- Need simple setup + deep Google integration → use **GKE native Ingress**
- Need advanced routing / annotations / canaries / auth / regex → use **NGINX Ingress Controller**

References:

- [Kubernetes Ingress-NGINX Official Documentation](https://kubernetes.github.io/ingress-nginx/)
- [ExternalDNS with NGINX on GKE](https://kubernetes-sigs.github.io/external-dns/latest/docs/tutorials/gke-nginx)
- [Google Cloud - Ingress Configuration Overview](https://cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration)
