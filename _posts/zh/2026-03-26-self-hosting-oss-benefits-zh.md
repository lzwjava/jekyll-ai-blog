---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自托管开源软件的好处
translated: true
type: note
---

问题：为什么我们要为了个人使用而私有化部署（self-host）这些开源项目（Gitea、Jellyfin、LibreChat、Nextcloud、SearXNG 和 Uptime Kuma），这样做有什么好处？

回答：

## 为什么我们要私有化部署这些开源项目

私有化部署这些工具的核心动力可以归结为三大支柱：**隐私（privacy）**、**成本节约（cost savings）**以及**完全控制（full control）**。以下是针对每个项目的分析以及它们共同带来的优势。

---

### 🔷 单个项目的好处

#### 🟢 Gitea — 私有化部署的 Git / 代码仓库

Gitea 是一个极其轻量级的 Git server，能为你的个人基础设施带来企业级的 version control 能力。与 GitLab 等重量级替代品不同，Gitea 在提供完整的 Git 托管解决方案的同时，占用的系统资源极少，非常适合个人项目或小型开发团队。

它还支持在 commit 提交时自动将远程 git 仓库镜像到本地，从而轻松地将你自己的代码（甚至是他人的代码）备份到你的服务器上，以防万一。从 v1.19 版本开始，Gitea 添加了 Actions，这是一个内置的且兼容 GitHub Actions workflow 的 CI 系统。

**替代产品：** GitHub（用于私有/个人用途）

---

#### 🟢 Jellyfin — 个人媒体服务器

Jellyfin 不服务于任何商业模式，也不会像 Plex 多年来经历的那种逐渐“腐化（enshittification）”。它不需要云端连接进行身份验证，没有随机的流媒体服务，性能也非常出色——为你提供一个全功能的、本地优先的 media server 体验。

使用 Jellyfin，你的观看习惯是完全私密的——没有数据收集或追踪算法。你可以完全控制谁能访问你的内容、内容的组织方式以及流媒体播放的质量，不受任何外部第三方的干扰。

**替代产品：** Netflix, Plex (付费订阅), Spotify (用于自有音乐)

---

#### 🟢 LibreChat — 私有化部署的 AI 聊天界面

LibreChat 基本上就是 ChatGPT，但完全开源。它的界面非常熟悉，并且你拥有同样的一系列工具——从 agents 和 code interpreters 到 artifacts 和对话搜索。

你可以控制使用哪些 AI 模型（OpenAI、Anthropic、本地 LLMs 等），且你的对话数据永远不会发送到第三方 SaaS。你可以连接自己的 API keys，避免支付按人头的订阅费用。

**替代产品：** ChatGPT Plus, Claude.ai 付费方案（用于团队/多用户使用）

---

#### 🟢 Nextcloud — 个人云存储与生产力套件

作为 Google 和 Microsoft 等巨头的竞争对手，Nextcloud 是一个“个人云”，提供私有化部署版本的邮件、联系人、日历、看板、视频/音频通话、Web 托管、文件存储/同步、文档编辑、应用商店等。如果你只能选择一个应用程序来构建你的数字生活，那一定是 Nextcloud。

虽然商业云存储起初看起来很便宜，但随着用户增加和存储需求的增长，成本会迅速攀升。每人每年 100 美元的订阅费用对于 10 个用户来说就变成了 1000 美元。通过 Nextcloud，你只需要为你的基础设施支付一次费用，并可以进行扩展，而无需支付重复的按用户收费。

**替代产品：** Google Drive, Google Docs, Microsoft 365, Dropbox

---

#### 🟢 SearXNG — 私有搜索引擎聚合器

SearXNG 不仅仅是 Google 搜索的前端——它是一个聚合器，如果配置得当，它可以从 Bing、Startpage、Wikipedia、DuckDuckGo、Brave 等收集结果。

关键好处是：搜索查询不会与你的身份或浏览轨迹绑定。没有个性化信息茧房，也没有基于你搜索内容的广告精准投放。

**替代产品：** Google Search, Bing (移除追踪)

---

#### 🟢 Uptime Kuma — 服务监控与告警

Uptime Kuma 是一个私有化部署的监控工具，用于跟踪你的所有其他服务（Gitea、Jellyfin、Nextcloud 等）是否正在运行。当服务宕机时，它会通过 Telegram、邮件、Discord 等发送告警。既然你私有化部署了一切，你也就需要自己 *monitor* 一切——这就是完成这项工作的工具。

**替代产品：** UptimeRobot, Better Uptime (付费 SaaS 监控)

---

### 🔷 所有项目的共同好处

| 好处 | 描述 |
|---|---|
| **Privacy** | 你的数据保留在自己的硬件上——没有大科技公司的数据挖掘 |
| **Cost Savings** | 一次性硬件投资取代了多个每月的订阅费用 |
| **Full Control** | 你决定运行时间、更新、功能和访问规则 |
| **No Vendor Lock-in** | 服务不会消失、不会更改条款或被收购 |
| **Learning & Skills** | 运行 homelab 可以建立真实的 DevOps/sysadmin 知识 |
| **Customization** | 开源意味着你可以修改和扩展任何东西 |
| **Data Sovereignty** | 在 GDPR 框架下或处理敏感个人数据时尤为重要 |

---

### 🔷 总结

虽然购买 NAS 设备或搭建 home lab 的前期成本较高，但从长远来看你会节省开支——更重要的是，你获得了独立性，不再依赖于那些可能更改价格、移除功能或直接关闭的大型科技平台。运行你自己的技术栈（stack）意味着你的工具是 *为你* 服务，而不是让你服务于工具。

参考资料：

- [XDA Developers — Self-hosting saves money beyond Jellyfin and Nextcloud](https://www.xda-developers.com/not-just-jellyfin-nextcloud-heres-how-saved-money-thanks-to-home-lab/)
- [DEV Community — Journey into Open Source: Self-Hosting SearXNG](https://dev.to/sai_krishna_f60a5a66237df/my-journey-into-open-source-from-linux-basics-to-self-hosting-searxng-1ae1)
- [Veeble — 10 Open-Source Apps That Will Save You Money](https://www.veeble.com/blog/10-open-source-apps-that-will-save-you-money/)
- [Logan Marchione — Darlings of the Self-Hosted World](https://loganmarchione.com/2022/05/darlings-of-the-self-hosted-open-source-world/)
- [Perfect Media Server — Top 10 Self-Hosted Apps](https://perfectmediaserver.com/04-day-two/top10apps/)
- [DreamHost — 50+ Open-Source Alternatives to Cloud Services](https://www.dreamhost.com/blog/open-source-alternatives/)
- [Glukhov.org — Self-Hosting Nextcloud](https://www.glukhov.org/post/2025/11/next-cloud-selfhosted/)
