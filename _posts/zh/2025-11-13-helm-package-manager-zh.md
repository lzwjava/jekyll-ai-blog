---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Helm：Kubernetes包管理器
translated: true
type: note
---

Helm 是 Kubernetes 的包管理器，常被称为“Kubernetes 的 yum 或 apt”。它通过将相关资源（Deployment、Service、ConfigMap 等）打包成可复用的版本化 **Chart**，简化了在 Kubernetes 集群上部署、管理和升级复杂应用的过程。

可以将 Helm Chart 视为 Kubernetes 清单文件的 Docker 镜像：它将 YAML 文件、模板、默认值和逻辑打包成一个单元，只需一条命令即可安装。

在 **Jenkins** 等 CI/CD 流水线中，Helm 通常用于：

- 构建和测试 Chart
- 将 Chart 推送到仓库（如 ChartMuseum、Harbor、Nexus）
- 安全地将应用部署到预发布/生产集群

---

## 为什么使用 Helm？

| 问题 | Helm 解决方案 |
|--------|---------------|
| 手动管理 50 多个 YAML 文件 | 打包成一个 Chart |
| 将同一应用部署到开发/预发布/生产环境 | 使用 `values.yaml` 覆盖配置 |
| 回滚失败的部署 | `helm rollback` |
| 跨团队共享应用 | 将 Chart 发布到仓库 |
| 基础设施版本管理 | Chart 语义化版本控制 |

---

## 核心概念

### 1. **Chart**

- 包含 Kubernetes 清单和元数据的目录结构
- 示例：`my-app-chart/`

```
my-app-chart/
├── Chart.yaml          # 元数据（名称、版本等）
├── values.yaml         # 默认配置值
├── templates/          # Kubernetes YAML 模板
│   ├── deployment.yaml
│   ├── service.yaml
│   └── _helpers.tpl    # 可复用模板片段
└── charts/             # 子 Chart（依赖项）
```

### 2. **Release**

- 在集群中运行的 Chart 实例
- 一个 Chart → 多个 Release（如 `myapp-dev`、`myapp-prod`）

### 3. **Repository**

- 托管已索引 Chart 的 HTTP 服务器（类似 npm 注册表）
- 常见仓库：ChartMuseum、Harbor、Nexus、GitHub Pages、S3

### 4. **Tiller**（已弃用）

- Helm v2 使用名为 Tiller 的服务端组件
- **Helm v3+ 移除了 Tiller** → 仅客户端，更安全

---

## Helm 命令速查表

| 命令 | 用途 |
|-------|--------|
| `helm create mychart` | 创建新 Chart 脚手架 |
| `helm lint mychart/` | 验证 Chart |
| `helm package mychart/` | 创建 `.tgz` 归档 |
| `helm repo add stable https://charts.helm.sh/stable` | 添加仓库 |
| `helm repo update` | 更新本地缓存 |
| `helm search repo nginx` | 查找 Chart |
| `helm install myapp ./mychart` | 部署 Release |
| `helm upgrade myapp ./mychart -f prod-values.yaml` | 使用新值升级 |
| `helm rollback myapp 3` | 回滚到版本 3 |
| `helm uninstall myapp` | 删除 Release |
| `helm list` | 列出 Release |
| `helm status myapp` | 显示 Release 状态 |
| `helm template ./mychart -f values.yaml` | 本地渲染模板 |

---

## Chart 结构详解

### `Chart.yaml`（必需）

```yaml
apiVersion: v2
kind: Chart
name: my-app
version: 1.2.3
appVersion: "2.5.0"
description: 示例 Web 应用
type: application
keywords:
  - web
  - http
home: https://example.com
sources:
  - https://github.com/user/my-app
maintainers:
  - name: 开发团队
    email: dev@example.com
icon: https://example.com/logo.png
```

### `values.yaml`（默认值）

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

### `_helpers.tpl`（最佳实践）

{% raw %}

```tpl
{{/* 生成基础标签 */}}
{{- define "my-app.labels" -}}
helm.sh/chart: {{ include "my-app.chart" . }}
app.kubernetes.io/name: {{ include "my-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

{% endraw %}

---

## Helm 在 Jenkins CI/CD 流水线中的应用

典型的 **Jenkins Pipeline** 使用 Helm 示例：

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
        stage('构建并推送 Docker') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                docker push ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('打包 Helm Chart') {
            steps {
                sh """
                cd ${CHART_DIR}
                yq eval '.image.tag = "${IMAGE_TAG}"' values.yaml -i
                helm dependency update
                helm package .
                """
            }
        }

        stage('部署到预发布环境') {
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

        stage('部署到生产环境') {
            when { tag "v*" }
            input { message "确认部署到生产环境？" }
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

### 关键 Jenkins 插件

- **Kubernetes CLI** (`kubectl`)
- **Helm**（通过代理中的 `helm` 二进制文件）
- **Pipeline Utility Steps** (`readYaml`、`writeYaml`)
- **Credentials Binding**（用于 kubeconfig、注册表）

---

## 最佳实践

| 实践 | 原因 |
|--------|-----|
| 在 CI 中使用 `helm lint` + `helm template` | 及早发现错误 |
| Chart 语义化版本控制 | 配置更新用 `1.0.0` → `1.0.1`，新功能用 `1.1.0` |
| 使用 `appVersion` 表示应用版本，`version` 表示 Chart 版本 | 解耦应用与打包 |
| 使用 `-f values-env.yaml` 分离环境配置 | 避免重复 Chart |
| 使用 `helm secrets` 或 SOPS 管理密钥 | 绝不提交明文密钥 |
| 固定依赖版本 | `helm dependency update --version X` |
| 使用 `{{ include "chart.labels" . }}` 辅助函数 | 保持标签一致性 |
| 在生产环境升级中启用 `--atomic` | 失败时自动回滚 |

---

## 常用工具与集成

| 工具 | 与 Helm 的配合使用 |
|------|---------------|
| **ChartMuseum** | 轻量级 Chart 仓库 |
| **Harbor / Nexus** | 企业级注册表 + Helm 仓库 |
| **ArgoCD** | GitOps + Helm |
| **Flux** | 使用 Helm Operator 的 GitOps |
| **helmfile** | 声明式管理多个 Release |
| **k3s / kind** | 本地测试 |

---

## 故障排除技巧

| 问题 | 解决方法 |
|------|-----|
| `Error: UPGRADE FAILED: another operation is in progress` | 等待或使用 `--force`（危险） |
| 模板未渲染 | 本地使用 `helm template .` |
| ImagePullBackOff | 检查标签、注册表认证 |
| 找不到 Release | `helm ls --all --all-namespaces` |
| CRD 未应用 | 添加 `crds/` 文件夹并单独应用 |

---

## 示例：使用 Helm 部署 NGINX

```bash
# 添加仓库
helm repo add bitnami https://charts.bitnami.com/bitnami

# 安装
helm install web-server bitnami/nginx \
  --set replicaCount=3 \
  --set service.type=LoadBalancer

# 升级
helm upgrade web-server bitnami/nginx --set replicaCount=5

# 回滚
helm rollback web-server 1
```

---

## 资源

- [官方 Helm 文档](https://helm.sh/docs/)
- [Helm Hub（Chart 仓库）](https://hub.helm.sh/)
- [Artifact Hub（现代 Chart 搜索）](https://artifacthub.io/)
- [Helm 最佳实践](https://helm.sh/docs/topics/charts/#chart-best-practices)

[Helm 官网](https://helm.sh)
[Bitnami Charts](https://github.com/bitnami/charts)
[Jenkins X 中的 Helm](https://www.jenkins-x.io/docs/)
