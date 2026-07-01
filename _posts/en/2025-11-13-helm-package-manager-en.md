---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: "Helm: Kubernetes Package Manager"
translated: false
type: note
---

Helm is the package manager for Kubernetes, often called "the yum or apt for Kubernetes." It simplifies deploying, managing, and upgrading complex applications on Kubernetes clusters by bundling related resources (Deployments, Services, ConfigMaps, etc.) into reusable, versioned **charts**.

Think of a Helm chart like a Docker image for Kubernetes manifests: it packages YAML files, templates, defaults, and logic into a single unit that can be installed with one command.

In CI/CD pipelines like **Jenkins**, Helm is commonly used to:

- Build and test charts.
- Push charts to repositories (e.g., ChartMuseum, Harbor, Nexus).
- Deploy applications to staging/production clusters securely.

---

## Why Use Helm?

| Problem | Helm Solution |
| -------- | --------------- |
| Managing 50+ YAML files manually | Bundle into one chart |
| Deploying same app to dev/stage/prod | Use `values.yaml` overrides |
| Rolling back failed deployments | `helm rollback` |
| Sharing apps across teams | Publish charts to repo |
| Versioning infrastructure | Semantic versioning of charts |

---

## Core Concepts

### 1. **Chart**

- Directory structure containing Kubernetes manifests and metadata.
- Example: `my-app-chart/`

```
my-app-chart/
├── Chart.yaml          # Metadata (name, version, etc.)
├── values.yaml         # Default configuration values
├── templates/          # Kubernetes YAML templates
│   ├── deployment.yaml
│   ├── service.yaml
│   └── _helpers.tpl    # Reusable template snippets
└── charts/             # Sub-charts (dependencies)
```

### 2. **Release**

- An instance of a chart running in a cluster.
- One chart → multiple releases (e.g., `myapp-dev`, `myapp-prod`).

### 3. **Repository**

- HTTP server hosting indexed charts (like npm registry).
- Common: ChartMuseum, Harbor, Nexus, GitHub Pages, S3.

### 4. **Tiller** (Deprecated)

- Helm v2 used a server-side component called Tiller.
- **Helm v3+ removes Tiller** → client-only, more secure.

---

## Helm Commands Cheat Sheet

| Command | Purpose |
| ------- | -------- |
| `helm create mychart` | Scaffold new chart |
| `helm lint mychart/` | Validate chart |
| `helm package mychart/` | Create `.tgz` archive |
| `helm repo add stable https://charts.helm.sh/stable` | Add repo |
| `helm repo update` | Update local cache |
| `helm search repo nginx` | Find charts |
| `helm install myapp ./mychart` | Deploy release |
| `helm upgrade myapp ./mychart -f prod-values.yaml` | Upgrade with new values |
| `helm rollback myapp 3` | Roll back to revision 3 |
| `helm uninstall myapp` | Delete release |
| `helm list` | List releases |
| `helm status myapp` | Show release status |
| `helm template ./mychart -f values.yaml` | Render templates locally |

---

## Chart Structure Deep Dive

### `Chart.yaml` (Required)

```yaml
apiVersion: v2
kind: Chart
name: my-app
version: 1.2.3
appVersion: "2.5.0"
description: A sample web app
type: application
keywords:
  - web
  - http
home: https://example.com
sources:
  - https://github.com/user/my-app
maintainers:
  - name: Dev Team
    email: dev@example.com
icon: https://example.com/logo.png
```

### `values.yaml` (Defaults)

```yaml
replicaCount: 2
image:
  repository: nginx
  tag: "1.21"
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
resources:
  limits:
    cpu: 500m
    memory: 512Mi
```

### `templates/deployment.yaml`

{% raw %}

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: 80
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

{% endraw %}

### `_helpers.tpl` (Best Practice)

{% raw %}

```tpl
{{/* Generate basic labels */}}
{{- define "my-app.labels" -}}
helm.sh/chart: {{ include "my-app.chart" . }}
app.kubernetes.io/name: {{ include "my-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

{% endraw %}

---

## Helm in Jenkins CI/CD Pipeline

Here’s a typical **Jenkins Pipeline** using Helm:

```groovy
pipeline {
    agent any
    environment {
        CHART_DIR = "helm/my-app"
        IMAGE_NAME = "myregistry/my-app"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        HELM_REPO = "https://charts.mycompany.com"
    }
    stages {
        stage('Build & Push Docker') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                docker push ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Package Helm Chart') {
            steps {
                sh """
                cd ${CHART_DIR}
                yq eval '.image.tag = "${IMAGE_TAG}"' values.yaml -i
                helm dependency update
                helm package .
                """
            }
        }

        stage('Deploy to Staging') {
            when { branch 'main' }
            steps {
                withCredentials([kubeconfigFile(credentialsId: 'kubeconfig-staging')]) {
                    sh """
                    helm upgrade --install myapp-staging ./helm/my-app*.tgz \
                      --namespace staging \
                      --values values-staging.yaml \
                      --wait --timeout 5m
                    """
                }
            }
        }

        stage('Deploy to Production') {
            when { tag "v*" }
            input { message "Deploy to production?" }
            steps {
                withCredentials([kubeconfigFile(credentialsId: 'kubeconfig-prod')]) {
                    sh """
                    helm upgrade --install myapp-prod ./helm/my-app*.tgz \
                      --namespace production \
                      --values values-prod.yaml \
                      --atomic
                    """
                }
            }
        }
    }
}
```

### Key Jenkins Plugins

- **Kubernetes CLI** (`kubectl`)
- **Helm** (via `helm` binary in agent)
- **Pipeline Utility Steps** (`readYaml`, `writeYaml`)
- **Credentials Binding** (for kubeconfig, registry)

---

## Best Practices

| Practice | Why |
| -------- | ----- |
| Use `helm lint` + `helm template` in CI | Catch errors early |
| Version charts semantically | `1.0.0` → `1.0.1` for config, `1.1.0` for new features |
| Use `appVersion` for app, `version` for chart | Decouple app and packaging |
| Split environments with `-f values-env.yaml` | Avoid duplicating charts |
| Use `helm secrets` or SOPS for secrets | Never commit plaintext |
| Pin dependency versions | `helm dependency update --version X` |
| Use `{{ include "chart.labels" . }}` helpers | Consistent labeling |
| Enable `--atomic` in prod upgrades | Auto-rollback on failure |

---

## Common Tools & Integrations

| Tool | Use with Helm |
| ------ | --------------- |
| **ChartMuseum** | Lightweight chart repo |
| **Harbor / Nexus** | Enterprise registry + Helm repo |
| **ArgoCD** | GitOps + Helm |
| **Flux** | GitOps with Helm Operator |
| **helmfile** | Manage multiple releases declaratively |
| **k3s / kind** | Local testing |

---

## Troubleshooting Tips

| Issue | Fix |
| ------ | ----- |
| `Error: UPGRADE FAILED: another operation is in progress` | Wait or use `--force` (dangerous) |
| Templates not rendering | Use `helm template .` locally |
| ImagePullBackOff | Check tag, registry auth |
| Release not found | `helm ls --all --all-namespaces` |
| CRDs not applied | Add `crds/` folder and apply separately |

---

## Example: Deploy NGINX with Helm

```bash
# Add repo
helm repo add bitnami https://charts.bitnami.com/bitnami

# Install
helm install web-server bitnami/nginx \
  --set replicaCount=3 \
  --set service.type=LoadBalancer

# Upgrade
helm upgrade web-server bitnami/nginx --set replicaCount=5

# Rollback
helm rollback web-server 1
```

---

## Resources

- [Official Helm Docs](https://helm.sh/docs/)
- [Helm Hub (Chart Repository)](https://hub.helm.sh/)
- [Artifact Hub (Modern Chart Search)](https://artifacthub.io/)
- [Helm Best Practices](https://helm.sh/docs/topics/charts/#chart-best-practices)

[Helm Official Site](https://helm.sh)
[Bitnami Charts](https://github.com/bitnami/charts)
[Helm in Jenkins X](https://www.jenkins-x.io/docs/)
