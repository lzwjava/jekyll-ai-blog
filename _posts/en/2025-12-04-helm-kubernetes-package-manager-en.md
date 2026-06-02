---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Helm Kubernetes Package Manager
translated: false
type: note
---

Question: What is Helm in software?

Answer:

Helm is the package manager for Kubernetes, often described as the "Kubernetes equivalent of apt, yum, or Homebrew."

It simplifies the deployment, management, and upgrading of applications on Kubernetes clusters by packaging all related Kubernetes resources (Deployments, Services, ConfigMaps, etc.) into a single unit called a **chart**.

### Key Concepts

- **Chart**: A Helm package that contains:
  - YAML templates for Kubernetes manifests
  - Default configuration values (in `values.yaml`)
  - Helper files and scripts
- **Release**: A specific instance of a chart deployed to a cluster (you can have multiple releases of the same chart with different configurations).
- **Repository**: A storage location (usually HTTP/S) where charts are hosted and shared (e.g., Artifact Hub is the official public repo).

### Common Commands

```bash
helm search hub nginx          # Find charts
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-nginx bitnami/nginx   # Deploy a chart
helm upgrade my-nginx bitnami/nginx --set replicaCount=5
helm rollback my-nginx 1       # Roll back to previous release
helm uninstall my-nginx        # Remove the release
```

### Helm Versions

- **Helm 2** (older, now deprecated): Used a server-side component called Tiller.
- **Helm 3** (current, since 2019): Fully client-side, no Tiller, better security and RBAC support.

In short, Helm makes complex Kubernetes application deployments repeatable, versioned, and configurable — think of it as the tool that turns a messy pile of YAML files into manageable, shareable packages.

References:

- [Helm Official Documentation](https://helm.sh/docs/)
- [Artifact Hub](https://artifacthub.io/)
