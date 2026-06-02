---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将 Java 博客部署到 Cloud Run
translated: true
type: note
---

Question: 如何在 Google Cloud 中使用 Docker 容器部署 blog-server 应用？

Answer:

以下是 2026 年将 **Dockerized Java/Spring Boot** 应用程序（从包含 `Dockerfile` 和 `pom.xml` 的目录）部署到 **Google Cloud** 最常用且推荐的方法。目前最简单且最流行的方案是 **Cloud Run**（serverless containers）。

### 推荐选项：部署到 Cloud Run (serverless, 按请求付费)

#### 方案 A – 最简单：直接从源码自动构建并部署（推荐大多数开发者使用）

你甚至不需要在本地构建 Docker image。

1. 确保已安装 Google Cloud SDK 并完成身份验证：

   ```bash
   gcloud auth login
   gcloud config set project YOUR-PROJECT-ID
   ```

2. 启用必要的 API（只需运行一次）：

   ```bash
   gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
   ```

3. 在项目根目录（`pom.xml` 和 `Dockerfile` 所在位置）运行：

   ```bash
   gcloud run deploy blog-server \
     --source . \
     --region asia-northeast1 \          # 或 us-central1, europe-west1 等
     --allow-unauthenticated \          # 如果需要私有服务请移除此项
     --port 8080 \                      # 如果应用监听其他端口请修改
     --memory 1Gi                       # 可选 – 根据需求调整
   ```

   - Cloud Run 会自动识别这是一个 Maven/Spring Boot 项目，使用 Cloud Build 构建容器并进行部署。
   - 首次部署大约需要 3–5 分钟；后续部署速度会快得多。

#### 方案 B – 手动构建 Docker image 并推送

当你需要更多控制权或已有 CI/CD 流程时，此方案非常有用。

1. 在本地构建并打标签（tag）image：

   ```bash
   docker build -t gcr.io/YOUR-PROJECT-ID/blog-server:latest .
   # 或者使用 Artifact Registry (更新且推荐的方式):
   # docker build -t asia-northeast1-docker.pkg.dev/YOUR-PROJECT-ID/my-repo/blog-server:latest .
   ```

2. 推送 image：

   ```bash
   gcloud auth configure-docker
   docker push gcr.io/YOUR-PROJECT-ID/blog-server:latest
   # 如果使用 Artifact Registry:
   # gcloud auth configure-docker asia-northeast1-docker.pkg.dev
   # docker push asia-northeast1-docker.pkg.dev/YOUR-PROJECT-ID/my-repo/blog-server:latest
   ```

3. 部署到 Cloud Run：

   ```bash
   gcloud run deploy blog-server \
     --image gcr.io/YOUR-PROJECT-ID/blog-server:latest \
     --region asia-northeast1 \
     --allow-unauthenticated \
     --port 8080
   ```

   或者使用 Artifact Registry 里的 image：

   ```bash
   --image asia-northeast1-docker.pkg.dev/YOUR-PROJECT-ID/my-repo/blog-server:latest
   ```

#### 部署前的快速检查清单

- 你的 **Dockerfile** 应该暴露正确的端口（通常是 `EXPOSE 8080`）
- 应用应该监听 `0.0.0.0`（而不是 `localhost`）
- 对于生产环境，建议添加参数：

  ```bash
  --cpu 1 --memory 512Mi --concurrency 80 --max-instances 10
  ```

- 如果你使用了环境变量或 secrets：

  ```bash
  --set-env-vars "SPRING_PROFILES_ACTIVE=prod,DATABASE_URL=..."
  ```

#### 其他常见的 Google Cloud 选项（当 Cloud Run 不适用时）

- **Cloud Run jobs** → 用于批处理或一次性任务
- **Google Kubernetes Engine (GKE)** → 当你需要高级网络功能、有状态应用（stateful apps）或极高度的定制化时
- **Compute Engine** → 传统的 VM + Docker（更多手动操作）

对于 blog-server，Cloud Run 通常在价格、简洁性和伸缩性之间提供了最佳平衡。

部署完成后，你将获得如下 URL：

<https://blog-server-abc123-uc.a.run.app>

祝你好运！

References:

- [Deploying container images to Cloud Run](https://docs.cloud.google.com/run/docs/deploying)
- [Quickstart: Build and deploy a Java Spring Boot web app to Cloud Run](https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-java-service)
- [Deploy services from source code | Cloud Run](https://docs.cloud.google.com/run/docs/deploying-source-code)
