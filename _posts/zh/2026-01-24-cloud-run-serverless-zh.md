---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Cloud Run：托管式无服务器平台
translated: true
type: note
---

Question: What is an introduction to Cloud Run in Google Cloud Platform (GCP)?

Answer:

Cloud Run 是 Google Cloud 的**全托管 Serverless 平台**，用于运行容器化的应用程序（或简单的代码/Functions），无需管理任何底层服务器或 Clusters。

### 一句话核心理念

你只需向 Cloud Run 提供一个容器镜像（Docker），它就会自动处理：

- 接收 HTTP 请求（或事件）
- 瞬间从 **0 扩展到数千个** 实例
- **仅针对代码实际运行的时间**计费（亚秒级计费）
- 所有的 Infrastructure、Networking、Load Balancing、TLS、Logging、Monitoring 等

### 主要变体 (2025–2026)

| 变体 | 最适合场景 | 触发类型 | 是否支持缩减至零？ | 是否需要容器？ | 语言自由度 |
|--------------------------|---------------------------------------|-----------------------|-----------|----------------------|------------------|
| **Cloud Run (services)** | Web APIs, 网站, Microservices, 后台工作程序 | HTTP + gRPC | 是 | 是 | 任意 |
| **Cloud Run jobs** | 批处理 / 一次性 / 定时任务 | 手动 / Scheduler / Eventarc | 否 (运行直至完成) | 是 | 任意 |
| **Cloud Run functions** (2nd gen) | 轻量化 Functions / 事件驱动代码 | HTTP + 多种事件 (Pub/Sub, Storage 等) | 是 | 否 (仅需源码) | 有限 (Node, Python, Go, Java, .NET, Ruby, PHP) |

大多数人从 **Cloud Run services**（旗舰产品）开始。

### 核心特性

- **按使用付费 (Pay-per-use)** — 你只需支付：
  - vCPU-seconds
  - Memory-seconds
  - 请求数量
  - （极小的）Cloud Run 管理费用
  → **闲置时零费用**（自动缩减至零）

- **基于请求的自动扩展 (Autoscaling)** — 在几秒钟内从 0 → 1,000+ 实例

- **单实例最大请求并发量 (Concurrency)** — 可由你控制（默认 80，最高可达 1,000）

- **冷启动 (Cold starts)** — 对于小型容器通常为 1-4 秒，优于 2025 年的大多数替代方案

- **基于 Knative 构建** — 拥有开源根基，概念具有可移植性

- **支持任何语言 / 框架** — 只要它能运行在容器中（Go, Node.js, Python, Java, .NET, Rust, Deno, PHP, C++ 等）

### 2025–2026 年的典型用例

- REST/GraphQL APIs
- Web 前端（特别是 Next.js, SvelteKit, Remix 等）
- Webhooks 接收器
- 事件驱动架构中的 Microservices
- AI Inference Endpoints（2025 年非常流行）
- 定时批处理作业（配合 Cloud Run jobs + Cloud Scheduler）
- 替代 App Engine, Compute Engine sidecars, 小型 Kubernetes 部署

### 快速横向对比 (2025 视角)

| 特性 / 产品 | Cloud Run | Cloud Functions (2nd gen) | GKE Autopilot | App Engine flexible |
|---------------------------|-----------|----------------------------|---------------|---------------------|
| 容器自由度 | 完全 | 受限 | 完全 | 受限 |
| 缩减至零 | 是 | 是 | 否 | 否 |
| 语言支持 | 任意 | 有限 | 任意 | 有限 |
| HTTP + 事件 | 是 | 最佳事件支持 | 是 | 仅支持 HTTP |
| 运维复杂度 | 极低 | 极低 | 中-高 | 低 |
| 冷启动时间 | 良好 | 极佳 | 无 | 良好 |

### Hello World 部署（2025 年最常见的方式）

```bash
# 1. 编写你的应用 (例如: Node.js)
cat > server.js <<'EOF'
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send(`Hello from Cloud Run! ${new Date()}`);
});

app.listen(process.env.PORT || 8080);
EOF

# 2. 创建 Dockerfile
cat > Dockerfile <<'EOF'
FROM node:20-slim
WORKDIR /app
COPY . .
RUN npm init -y && npm install express
ENV PORT=8080
CMD ["node", "server.js"]
EOF

# 3. 构建并部署 (需要 gcloud CLI 和 Artifact Registry)
gcloud run deploy hello \
  --source . \
  --region asia-southeast1 \
  --allow-unauthenticated
```

2025 年的一键备选方案：

- `gcloud run deploy --source .` (自动检测多种语言)
- GitHub → Cloud Run 持续部署 (Continuous Deployment)
- Cloud Build + Cloud Run
- Cloud Run Button (用于开源仓库)

Cloud Run 依然是 2026 年在 Google Cloud 上运行生产负载最简单、最受欢迎的方式之一。

References:

- [What is Cloud Run - Official Documentation](https://cloud.google.com/run/docs/overview/what-is-cloud-run)
- [Cloud Run Main Page](https://cloud.google.com/run)
- [Cloud Run Documentation Overview](https://cloud.google.com/run/docs)
