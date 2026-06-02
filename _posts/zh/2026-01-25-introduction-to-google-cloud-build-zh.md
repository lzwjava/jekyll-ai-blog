---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Build 简介
translated: true
type: note
---

Question: Google Cloud 中的 Cloud Build 全面介绍

Answer:

Cloud Build 是 **Google Cloud 的全托管、Serverless CI/CD（持续集成 / 持续交付）平台**。它允许你在代码发生更改时自动构建、测试和部署软件。

### 核心概念

你通过提供一个 **build configuration file**（通常是放置在源代码仓库中的 `cloudbuild.yaml`）来定义 Cloud Build 的执行任务。该文件包含一系列按顺序（或自 2021–2022 年改进后可并行）运行的 **steps**（任务）。

每个步骤本质上是一个运行在 Google 基础设施上的 **container**。你可以使用：

- 官方提供的 **Google-provided builders** (`gcr.io/cloud-builders/...`)
- 社区提供的 builders
- 来自 Docker Hub、Artifact Registry 等的任何公共 Docker image
- 你自定义的 container images

### 核心功能 (截至 2026 年初)

- **Triggers** —— 自动触发构建的任务：
  - 代码推送至分支 / 标签 (GitHub, GitLab, Bitbucket, Cloud Source Repositories)
  - Pull Request 的创建 / 更新
  - Pub/Sub 事件
  - 手动触发 / 定时触发 (通过 Cloud Scheduler)
  - Webhook

- **内置集成**
  - GitHub App (非常流行)
  - GitLab
  - Bitbucket
  - Cloud Source Repositories
  - Artifact Registry / Container Registry
  - Secret Manager
  - Cloud Logging & Cloud Monitoring
  - Binary Authorization (用于供应链安全)

- **并行与缓存**
  - 多个步骤可以并行运行（使用 `waitFor` 控制依赖关系）
  - 构建之间支持自动的 Source & Dependency 缓存（实现极快的增量构建）

- **Buildpacks 支持**
  - `gcr.io/buildpacks/builder` —— 针对 Java, Node.js, Python, Go, .NET, Ruby, PHP 等实现零配置构建。

- **Kaniko / BuildKit / img / crane** —— 无需特权 Docker daemon 即可构建 container images。

- **非常丰厚的免费额度**
  - 每天 120 build-minutes 免费（120 分钟 × 你选择的 worker 数量）
  - 大多数中小型项目通常都在免费额度内

- **并发与扩缩容**
  - 你可以为每个步骤选择机器类型：`E2`, `N1`, `E2-highcpu`，直到超大型自定义机器
  - 默认并发限制通常足够高（可以申请增加）

- **安全特性**
  - 在你的项目中（或共享 VPC）运行
  - 支持 VPC Service Controls
  - 集成 Binary Authorization 和 Vulnerability Scanning
  - Private pools（支持在本地 / 物理隔离 / 自定义网络中构建）

### 典型工作流示例

1. **简单的 container 构建与推送**

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'us-central1-docker.pkg.dev/$PROJECT_ID/my-repo/myapp', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'us-central1-docker.pkg.dev/$PROJECT_ID/my-repo/myapp']
images: ['us-central1-docker.pkg.dev/$PROJECT_ID/my-repo/myapp']
```

2. **现代 Buildpacks + 部署到 Cloud Run**

```yaml
steps:
  - name: 'gcr.io/buildpacks/builder'
    args: ['--project-id', '$PROJECT_ID']
  - name: 'gcr.io/google.com/cloudsdktool/gcloud'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'my-service'
      - '--image=$_IMAGE'
      - '--region=us-central1'
      - '--allow-unauthenticated'
```

3. **测试 + 构建 + 部署多语言 Monorepo**

```yaml
steps:
  - name: 'gcr.io/cloud-builders/npm'
    dir: 'frontend'
    args: ['ci', '&&', 'npm', 'run', 'test']
  - name: 'gcr.io/cloud-builders/go'
    dir: 'backend'
    args: ['test', './...']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', '$_IMAGE', '.']
    waitFor: ['-']
options:
  substitutionOption: 'ALLOW_LOOSE'
```

### 价格 (2025–2026)

| Tier              | Price per build-minute |
|-------------------|------------------------|
| Free tier         | 120 minutes/day free   |
| Standard (after free) | ~$0.0032 – $0.006 / min (取决于机器类型) |
| High-CPU / custom machines | 更高 (但仍然非常有竞争力) |

除非每天运行数百个大型构建，否则大多数团队支付的费用非常低。

### 何时选择 Cloud Build 而非替代方案

- 如果你已经在使用 Google Cloud 或计划使用，请选择 Cloud Build
- 如果你希望与 Artifact Registry, Cloud Run, GKE, Binary Authorization 紧密集成，并且需要最简单的 YAML 样板代码，它优于 GitHub Actions / GitLab CI
- 如果你的团队完全依赖 GitHub 且没有其他 GCP 使用需求，可以优先选择 GitHub Actions

在 2026 年，Cloud Build 仍然是 Google Cloud 生态系统中速度最快、性价比最高且集成度最好的 CI/CD 解决方案之一。

References:

- [Overview of Cloud Build | Google Cloud](https://docs.cloud.google.com/build/docs/overview)
- [Cloud Build documentation home](https://docs.cloud.google.com/build/docs)
- [Cloud Build main product page](https://cloud.google.com/build)
