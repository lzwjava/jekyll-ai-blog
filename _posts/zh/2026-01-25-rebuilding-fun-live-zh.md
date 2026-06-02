---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Google Cloud 上重构趣直播
translated: true
type: note
---

问题：如果今天使用 Google Cloud 技术重建趣直播，应该如何架构？

回答：

要在 2025–2026 年重建趣直播——一个集成了实时讲座（编程、设计等）、付费课程、讲师打赏、实时互动、录播回放 (VOD)、类微信通知以及微信小程序集成的知识分享直播平台——建议采用现代化的、可扩展的、Serverless 优先或重度使用托管服务的架构。与原始的自建 PHP/CodeIgniter + SRS + 阿里云技术栈相比，这将大幅减少运维负担。

### 新架构的核心原则

- **Serverless 与托管服务**：尽可能使用，以最小化 DevOps 工作。
- **全球低延迟分发**：针对直播和 VOD 输出。
- **可扩展性**：能够处理突发流量（如热门讲座）。
- **内置安全与商业化**：支付集成、访问控制。
- **微服务或模块化单体**：倾向于独立的服务架构。
- **保持 OBS 兼容性**：讲师端仍普遍使用 OBS。

### 推荐的高层架构

1. **前端 / 客户端 (Frontend / Clients)**
   - **Web 应用**：React / Next.js (或 Vue 3 以保持连续性)，托管在 **Cloudflare Pages** 或 **Firebase Hosting**，SSR/Edge 需求使用 **Cloud Run**。
   - **微信小程序**：继续使用微信 SDK，通过其调用后端 API。
   - **移动应用**（如果扩展）：Flutter 或 React Native，集成 Firebase SDK。

2. **推流 (Ingestion: Lecturer → Server)**
   - 讲师通过 **OBS** 推送 RTMP 流（2025 年这依然是主流）。
   - 推流端点：**Live Stream API** (Cloud Live Stream) —— Google 的全托管服务，接收 RTMP/RTMPS，进行转码并切片为 HLS/DASH。
   - 替代方案（如需更多控制权）：Cloud Run + 自建媒体服务器（如 Ant Media, OvenMediaEngine 或 nginx-rtmp），但首选托管服务。

3. **直播内容分发 (Live Streaming Distribution)**
   - 使用 **Media CDN** (Google 针对媒体优化的 CDN) 进行超低延迟分发。
     - 支持 Low-latency HLS (LL-HLS), WebRTC (通过集成), CMAF。
     - 边缘缓存，全球 Anycast 播发。
   - 源站：Live Stream API 输出 → Media CDN。
   - 备用方案：Cloud Storage 存储桶存放 HLS 切片。

4. **回放 / 点播 (Playback / VOD)**
   - 直播结束后，Live Stream API 将内容归档至 **Cloud Storage**。
   - 使用 **Transcoder API** 进行转码（如需自适应比特率）。
   - 通过 **Media CDN** 或直接从 Storage + Signed URLs 提供 VOD 服务。
   - 元数据（标题、讲师、时长、封面图）存储在 **Firestore** 或 **Cloud SQL**。

5. **后端 / 业务逻辑 (Backend / Business Logic)**
   - **首选方案（推荐）**：**Cloud Run** (容器化服务) 或 **Cloud Functions (2nd gen)**。
     - 使用 Node.js / Go / Python (冷启动速度优于 PHP)。
     - 处理：用户鉴权、支付、讲座排期、打赏、聊天、问答。
   - **数据库**：
     - **Firestore** (NoSQL)：用于用户、讲座、支付记录、实时聊天（其 Real-time Listeners 非常适合直播问答）。
     - **Cloud SQL** (PostgreSQL)：如果需要强关系一致性（如财务交易）。
   - **缓存**：**Memorystore for Redis** (托管 Redis)。
   - **身份验证**：**Firebase Authentication** (轻松集成社交登录/微信登录、手机、邮箱)。
   - **支付与打赏**：通过 Cloud Functions/Run 集成 Stripe、微信支付或支付宝（安全处理 Webhooks）。

6. **实时功能 (Real-time Features: Chat, Q&A, Rewards)**
   - **Firestore** Real-time Listeners（亚毫秒级同步聊天）。
   - 替代方案：更高并发需求下使用 **Pub/Sub** + **Cloud Run**，或 **Firebase Realtime Database**。
   - 极高并发场景：增加 **Memorystore**。

7. **通知 (Notifications)**
   - **Firebase Cloud Messaging (FCM)**：适用于 Web Push、Android 和 iOS。
   - 微信通知：通过 Cloud Functions 调用微信公众号/小程序模板消息 API。

8. **基础设施与运维 (Infrastructure & DevOps)**
   - **IaC**：Terraform 或 Google Cloud Deployment Manager。
   - **监控**：Cloud Monitoring + Cloud Logging + **Firebase Crashlytics**。
   - **CI/CD**：Cloud Build。
   - **密钥管理**：**Secret Manager**。
   - **全球扩展**：为 Firestore 使用多区域配置，使用多区域 Bucket。

### 建议技术栈汇总 (基于 Google Cloud)

| 层级 | 原始方案 (2016–2019) | 现代 Google Cloud 推荐方案 |
| :--- | :--- | :--- |
| 前端 | Vue + HTML | React/Next.js 或 Vue 3 + Firebase Hosting |
| 服务器 | PHP + CodeIgniter | Node.js/Go/Python 运行在 Cloud Run 上 |
| 数据库 | MySQL + Redis | Firestore + Memorystore for Redis |
| 直播推流 | SRS | Live Stream API (接收来自 OBS 的 RTMP) |
| 直播分发 | SRS + Nginx | Media CDN + HLS/LL-HLS |
| VOD 存储 | 阿里云 OSS | Cloud Storage + Transcoder API |
| 通知系统 | 微信集成 | FCM + 微信 API 调用 |
| 身份验证 | 自定义 | Firebase Authentication |
| 托管/计算 | Linux + Nginx | Cloud Run / Firebase |
| 设计工具 | Sketch | Figma (现代替代品) |

### 迁移 / 重建建议

- 从 MVP 开始：Live Stream API + Media CDN + Firestore + Cloud Run API。
- 保持 OBS → RTMP 流程不变，方便讲师操作。
- 再次在 GitHub 上开源——考虑使用 Monorepo 或前后端分离的代码仓库。
- 成本预估：低流量阶段非常便宜 (Serverless)；高流量阶段成本主要由 Media CDN 和流出流量 (Egress) 占据。
- 延迟目标：如果受众主要在中国，使用靠近中国大陆的 Media CDN 边缘节点（如香港、新加坡）。

这套架构比 2016–2019 年的版本更具可扩展性、维护成本更低，并且具备全球分发能力，同时保留了核心体验。

参考资料：

- [Google Cloud Live Stream API Best Practices](https://docs.cloud.google.com/livestream/docs/best-practices)
- [Media CDN for low-latency live streaming](https://discuss.google.dev/t/architecting-low-latency-live-streaming-a-developers-guide-to-media-cdn/296436)
- [Live Streaming with Media CDN and Live Stream API codelab](https://codelabs.developers.google.com/mediacdn-ls-codelab)
- [Google Cloud Video Streaming overview](https://www.vdocipher.com/blog/google-cloud-video-streaming)
