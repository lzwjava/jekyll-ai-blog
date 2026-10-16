---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 谷歌云RTMP流媒体替代方案
translated: true
type: note
---

**问题：** 在 Google Cloud 上，除了 SRS，还有哪些其他 RTMP 直播流媒体解决方案可以使用？

**回答：**

是的，有几种可靠的替代方案——从 Google 自家的托管服务到知名的开源和商业媒体服务器。以下是详细介绍：

---

## 1. 🟦 Google Cloud Live Stream API（原生 / 托管）

最“云原生”的选项。Live Stream API 将实时 SRT 或 RTMP 输入信号转码为 HLS 或 DASH 输出流，并保存到 Cloud Storage 存储桶中。然后，您可以将 Cloud Storage 存储桶配置为 Media CDN 的后端。

功能包括自动基础设施预配置、与 Cloud Storage 和 Cloud Audit Logs 的集成、用于冗余备份的输入流、实时转点播（live-to-VOD）、内容加密和 slate（占位画面）。

截至 2025 年 9 月，它还支持通过 SRT 或 RTMP 将直播流内容分发到远程端点，支持 H.265/HEVC 输入和输出，以及 UHD（4K）输入和输出。

**最适合：** 希望零基础设施管理并完全集成 GCP 的团队。

## 2. 🟩 Nginx + nginx-rtmp-module

最受欢迎的开源选项之一。此 Docker 镜像可用于创建 RTMP 服务器，与 nginx 和 nginx-rtmp-module 同时提供 HLS、DASH 和 RTMP 服务。它暴露端口 1935 用于 RTMP 流，端口 8080 用于 HLS 和 DASH 流。

在视频服务器节点上，您可以通过 Kubernetes 编排的 NGINX Web 服务器的 RTMP 模块来传输视频。以下 Kubernetes 配置文件部署了一个运行 NGINX RTMP 模块的工作负载，用于直播视频流。

NGINX 还提供官方的 Google Cloud Platform 部署指南。F5 NGINX Plus 可以直接安装在 Google Cloud Platform 上，支持 RTMP 和 GCP 上的全活跃高可用（all-active HA）配置。

**最适合：** 轻量级、熟悉的堆栈；可部署在 GCE 虚拟机或 GKE 上。

## 3. 🟧 Ant Media Server（开源 / 企业版）

Ant Media Server 是一个可扩展的开源媒体服务器，专为通过 WebRTC（约 0.5 秒）实现超低延迟直播而设计，同时支持 SRT、RTMP、RTSP、HLS 和 CMAF 低延迟 HLS（LL-HLS）。它使开发人员能够构建实时视频应用、直播广播和自适应码率（ABR）工作流。

它可以轻松快速地部署在本地或公共云网络上，包括 AWS、Azure、Google Cloud、Oracle Cloud、Akamai/Linode 和 Digital Ocean。

通过一键应用、云市场或 Docker/Kubernetes/脚本，无缝部署 Ant Media Server。

**最适合：** 在 RTMP 摄取之外还需要超低延迟 WebRTC 的用例；社区版提供免费层级。

## 4. 🟥 Wowza Streaming Engine（商业）

行业标准的商业选择。Wowza 是行业标准的商业流媒体服务器。大多数商业服务器都同时支持 RTMP、HLS、SRT 和 WebRTC，因为实际部署会混合使用协议。它可以部署在 GCE 虚拟机上，或通过 GCP Marketplace 部署。

**最适合：** 企业级可靠性、支持 SLA 和成熟生态系统。

## 5. 🟪 Red5（开源）

Red5 是一个开源媒体服务器，支持 RTMP、RTMPS 和 RTMPE 协议，用于音频/视频流、录制和通用元数据处理。它在 GCE 和 GKE 上运行良好。

**最适合：** 传统 Flash 时代的工作流，或已经熟悉 Red5 基于 Java 架构的团队。

## 6. ⬜ MediaMTX（原名 rtsp-simple-server）

一个用 Go 编写的现代、轻量级、零依赖媒体服务器。支持 RTMP、RTSP、WebRTC、SRT 和 HLS。作为单个二进制文件或 Docker 容器部署在 GCE 或 GKE 上极其容易。

**最适合：** 简单、低开销的部署；非常适合边缘/中继场景。

## 总结对比

| 解决方案 | 类型 | GCP 上的部署 | 协议 |
|---|---|---|---|
| **Google Live Stream API** | 托管服务 | 原生 | RTMP, SRT → HLS/DASH |
| **Nginx-RTMP** | 开源 | GCE / GKE | RTMP, HLS, DASH |
| **Ant Media Server** | 开源 / 商业 | GKE / Marketplace | WebRTC, RTMP, SRT, HLS |
| **Wowza** | 商业 | GCE / Marketplace | RTMP, HLS, SRT, WebRTC |
| **Red5** | 开源 | GCE / GKE | RTMP, RTMPS |
| **MediaMTX** | 开源 | GCE / GKE / Cloud Run | RTMP, RTSP, SRT, WebRTC |

如果你希望运维开销最小，**Google Cloud Live Stream API** 是自然之选。如果你需要完全控制权和开源灵活性，**Nginx-RTMP** 或 **Ant Media Server**（部署在 GKE 上）是最常见的选择。

---

**参考资料：**
- [Google Cloud Live Stream API 概览](https://cloud.google.com/livestream/docs/overview)
- [Google Cloud Live Stream API 发布说明](https://docs.cloud.google.com/livestream/docs/release-notes)
- [Ant Media Server GitHub](https://github.com/ant-media/Ant-Media-Server)
- [nginx-media-server Docker 镜像](https://github.com/woonizzooni/nginx-media-server)
- [Intel：在云原生视频流中利用 GPU（Nginx-RTMP + Kubernetes）](https://www.intel.com/content/www/us/en/developer/articles/technical/leveraging-gpu-in-cloud-native-video-streaming.html)
- [NGINX 文档：Google Cloud Platform 部署](https://docs.nginx.com/nginx/deployment-guides/google-cloud-platform/)