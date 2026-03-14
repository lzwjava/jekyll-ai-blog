---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国适配 OpenClaw 设置指南
translated: true
type: note
---

## 中国技术人员在闲鱼上实际安装的 OpenClaw 配置

这实际上是一个非常复杂的设置，因为原版 OpenClaw 假设使用西方服务（Telegram、Slack、OpenAI API），这些服务都被 GFW 屏蔽了。技术人员必须以多种方式进行适应。

---

### 1. 安装哪个版本 / 分支？

主要有两条路线：

**Option A — 官方 OpenClaw + 中国社区插件**

安装官方上游 OpenClaw，但补充安装 **`openclaw-china`** 插件包，这是一个社区维护的元包。社区创建了多个分支，为中国用户提供优化体验——包括 jiulingyun 的 `openclaw-cn`（内置 Feishu 集成和国内网络环境优化，以解决 GFW 连接问题）、AI-ZiMo 的 `openclaw-cn`（定期与上游同步），以及 SourceForge 上的 OpenClaw CN（专注于让框架对中国开发者可用）。这些分支处理在中国运行 OpenClaw 的实际问题：网络路由、API 端点选择、默认模型配置和 UI 本地化。

**Option B — 一键式中国企业版发行版**

大型科技公司发布了它们自己的变体，本质上是开箱即用的预配置 OpenClaw：

- **AutoClaw** by Zhipu AI —— 被宣传为中国首个“一键安装”本地版，预装超过 50 个技能，并推荐集成 GLM、DeepSeek、Kimi 等中国模型。
- **ArkClaw** by ByteDance's Volcano Engine —— 云端 SaaS 版本，可直接通过网页浏览器使用，深度集成 Feishu 和 DingTalk，支持 24/7 常开云运行。
- **QClaw** by Tencent —— 连接 WeChat 和 QQ，安装只需约 3 分钟，用户可以通过手机上的 WeChat 发送命令远程控制笔记本电脑。

闲鱼上的技术人员可能会根据客户需求和使用的消息平台安装其中任何一个。

---

### 2. 消息通道：替换 Telegram/Slack

由于 Telegram 和 Slack 在中国被屏蔽，技术人员配置中国替代方案。`openclaw-china` 插件包支持 DingTalk (钉钉)、Feishu (飞书)、QQ Bot、WeCom (企业微信 — WeChat Work) 和 WeCom App 作为通道。

以下是每种配置方式：

- **Feishu (Lark)：** 官方 `feishu-bridge` 技能通过 WebSocket 长连接实现连接——无需公共服务器、域名或 ngrok。它能在 NAT 和防火墙后工作，因为它从 OpenClaw 实例发起到 Feishu 服务器的外向连接。这是中国最简单且最可靠的选择。
- **DingTalk：** 阿里巴巴发布了将 OpenClaw 与 DingTalk 集成的全面指南，甚至在 3 月 31 日前提供无限 API 调用。
- **WeCom / QQ：** Tencent 的 WorkBuddy 允许通过 WeCom 在短短一分钟内进行远程配置，同时集成 QQ 和 DingTalk。

对于中国用户，Feishu (Lark) 通常是推荐的通道——API 可靠、消息稳定且免费额度充足。WeChat Work、DingTalk 和 QQ 也受支持，只是配置稍复杂一些。

---

### 3. AI 模型：替换 OpenAI

由于 OpenAI 的 API 也被 GFW 限制且需要海外支付方式，技术人员配置国内中国 LLM。最常见的选项：

| Model | Provider | Notes |
|---|---|---|
| **Qwen (通义千问)** | Alibaba | 最受欢迎的默认选择；设置向导可以自动授权 |
| **DeepSeek** | DeepSeek | 极其受欢迎，API 非常便宜 |
| **Kimi K2.5** | Moonshot AI | 推理能力强，用于 KimiClaw 托管版 |
| **GLM-5** | Zhipu AI | 内置于 AutoClaw |
| **Doubao** | ByteDance | 用于 ArkClaw |
| **MiniMax M2.5** | MiniMax | 还支持语音/音乐生成 |

OpenClaw 正式扩展了对中国 LLM 的支持，如 Zhipu AI 的 GLM-5 和 MiniMax M2.5，这意味着用户可以将这些模型连接到他们的 OpenClaw 安装中，本质上是使用中国提供商为 AI 代理更换新“大脑”。

中国教程中推荐的最快上手路径是选择 Qwen —— 它会自动重定向到 Qwen 的登录页面进行授权，无需 API 密钥。这被描述为任何想立即上手的人的最简单路径。

**OpenRouter** 在面向中国的设置中通常不使用，因为它主要聚合西方 API 提供商（OpenAI、Anthropic 等），需要海外访问。

---

### 4. 云端 vs 本地安装

对于需要 24/7 在线（在 PC 关机时运行定时任务）的用户，技术人员可能会将 OpenClaw 部署到国内云服务器。选项包括 Alibaba Cloud ECS（原生集成 Qwen/DingTalk）、Tencent Cloud（针对 WeChat/WeCom API 调用优化，低延迟）和 VolcEngine（ByteDance 的平台）。

然而，位于中国大陆的云托管服务器无法访问海外服务如 Google 或 Telegram。对于跨边境技能执行或海外 IP 需求，用户必须使用本地执行或购买海外云服务器。

---

### 典型闲鱼安装流程总结

1. **安装** 官方 OpenClaw CLI（或 AutoClaw/ArkClaw 中国分支）
2. **配置中国 LLM** —— 通常是 DeepSeek 或 Qwen API 密钥
3. **配置消息通道** —— 通常是 Feishu 或 DingTalk（替换 Telegram）
4. **安装技能包** —— 如网页搜索、日历、文件管理
5. **测试并移交** —— 用户现在可以在 Feishu/DingTalk 上向 AI 代理发送消息

References:

- [GitHub: BytePioneer-AI/openclaw-china — Chinese Plugin Package](https://github.com/BytePioneer-AI/openclaw-china)
- [OpenClaw Blog: Beyond OpenAI — Chinese LLMs Powering OpenClaw Agents](https://openclaws.io/blog/openclaw-chinese-llm-integrations/)
- [TechFlow: 2026 Hundred Shrimp Battle — OpenClaw Optimized for Chinese Users](https://www.techflowpost.com/en-US/article/30654)
- [SCMP: Chinese Tech Giants Offer Cheap Easy Access to OpenClaw](https://www.scmp.com/tech/article/3346090/chinese-tech-giants-offer-cheap-easy-access-openclaw-amid-lobster-fever)
- [Yicai: Zhipu, ByteDance, Tencent Launch OpenClaw Versions](https://www.yicaiglobal.com/news/zhipu-ai-bytedance-tencent-10-other-chinese-internet-giants-launch-openclaw-versions)
- [StableLearn: OpenClaw Installation Guide for Mac and Windows](https://stable-learn.com/en/openclaw-installation-tutorial/)
- [Trending Topics EU: OpenClaw Expands Support of Chinese AI Models](https://www.trendingtopics.eu/openclaw-expands-support-of-chinese-ai-models-amid-big-tech-interest/)