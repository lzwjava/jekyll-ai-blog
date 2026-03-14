---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 阿里巴巴携全套产品加入 OpenClaw
translated: true
type: note
---

**问题：** 阿里云（Aliyun）是否发布了自己的 OpenClaw 版本，类似于腾讯和 Kimi（Moonshot）所做的？

**答案：**

## 是的 — Alibaba/Aliyun 已全面加入 OpenClaw 竞赛

阿里巴巴实际上是中国 OpenClaw 生态系统中目前最活跃的参与者之一。以下是他们推出的所有内容的分解：

---

### 1. 🦞 JVS Claw — 移动应用（2026 年 3 月 13 日推出）

阿里巴巴发布了 **"JVS Claw"**，这是一个针对 iOS 和 Android 的移动应用，针对没有编程知识的智能手机用户，让他们可以指示 AI 代理执行现实世界任务。前 14 天免费。它在百度推出自己的 Android OpenClaw 应用后不久发布，腾讯和 MiniMax 也在同一领域竞争。

---

### 2. ☁️ 一键云部署，通过 Simple Application Server（轻量应用服务器）

Alibaba Cloud 支持通过其 **Simple Application Server**（轻量应用服务器）使用一键镜像部署直接部署 OpenClaw。系统会自动检测最近的 Model Studio 端点并提供 API key。截至 2026 年初，默认模型是 **qwen3.5-plus**。

腾讯、Alibaba、Moonshot 和 MiniMax 都提供了自己调整过的 OpenClaw 版本，它们的股价随着炒作而飙升。

---

### 3. 📦 Coding Plan — OpenClaw 的固定费率 API 订阅

Alibaba Cloud 为 OpenClaw 用户创建了专属的 **"Coding Plan"** API 订阅，让他们以固定月费访问 Qwen 模型，而不是按 token 计费的按使用付费。

Coding Plan 支持的模型包括 **qwen3.5-plus**、**qwen3-max**、**qwen3-coder-plus**，甚至第三方模型如 **Kimi K2.5**、**MiniMax-M2.5** 和 **GLM-5**，所有这些都可以通过单个 Alibaba Cloud API key 从 OpenClaw 访问。

---

### 4. 🛠️ Qwen Code — 他们的 Claude Code 等效产品

阿里巴巴还有 **Qwen Code**，这是一个基于终端的编码代理（类似于 Claude Code），它与 Coding Plan 集成。用户可以运行 `/auth` 和 `/model` 命令在所有模型之间切换。

---

### 总结：各大主要玩家的立场

| 公司 | OpenClaw 产品 |
|---|---|
| **Alibaba / Aliyun** | JVS Claw 移动应用 + 一键 ECS 部署 + Coding Plan API |
| **Tencent Cloud** | 一键部署 + 离线安装展台 |
| **Kimi (Moonshot)** | KimiClaw + Kimi K2.5 模型集成 |
| **Baidu** | OpenClaw 的 Android 应用 |
| **ByteDance (Volcengine)** | Coding Plan 订阅 |

因此，如果你在 Aliyun 上运行 OpenClaw，你会得到一个非常紧密的原生集成 — 服务器镜像、自动检测的 API key 以及他们的 Qwen 模型开箱即用即可协同工作。

**参考资料：**

- [Alibaba Debuts OpenClaw App (Bloomberg)](https://www.bloomberg.com/news/articles/2026-03-13/alibaba-debuts-openclaw-app-to-feed-china-s-agentic-ai-addiction)
- [Alibaba Cloud OpenClaw Deployment Docs](https://www.alibabacloud.com/help/en/simple-application-server/use-cases/quickly-deploy-and-use-openclaw)
- [Alibaba Cloud Coding Plan for OpenClaw](https://www.alibabacloud.com/help/en/model-studio/openclaw-coding-plan)
- [OpenClaw China Frenzy — Beyond Cloud Vendors (CIW)](https://www.ciw.news/p/openclaw-china-frenzy)
- [Tom's Hardware: OpenClaw craze in China](https://www.tomshardware.com/tech-industry/artificial-intelligence/openclaw-ai-agent-craze-sweeps-china-as-authorities-seek-to-clamp-down-amid-security-fears-adoption-surges-as-state-run-enterprises-are-barred-from-use)