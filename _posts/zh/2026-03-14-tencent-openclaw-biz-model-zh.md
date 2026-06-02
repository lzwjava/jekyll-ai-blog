---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 腾讯云 OpenClaw 商业模式
translated: true
type: note
---

问题：Tencent Cloud 如何实现其 OpenClaw 云版本，以及其商业模式是什么？

答案：

## 背景：OpenClaw 是什么？

OpenClaw（在中国因其爪状图标而被称为“龙虾”）是一个开源 AI agent framework，原本需要复杂的手动设置——租用服务器、配置 Python 环境和管理 API keys。它使用包括 Anthropic 的 Claude 在内的大型语言模型来处理日常数字任务，并在短短几个月内成为 GitHub 历史上增长最快的项目，超越了 Linux 在 GitHub 历史星标排行榜上的位置。

---

## Tencent Cloud 如何实现其 OpenClaw 云版本

Tencent 实际上在 OpenClaw 旗下推出了**多个产品**，每个产品针对不同的使用场景：

### 1. Tencent Cloud Lighthouse（一键云部署）
Tencent Cloud Lighthouse 是一款开箱即用的轻量级云服务器服务，针对轻量级场景设计，适用于希望无需管理基础设施即可方便构建应用的中中小企业（SMEs）和开发者。Tencent 将 Lighthouse 定位为单键部署 OpenClaw 的平台。

用户在控制台选择“OpenClaw 一键镜像”进行购买，即可在 3–5 分钟内自动初始化并运行，通过 web 终端访问。运行在 Tencent 内部网络上，为 WeChat 和 Enterprise WeChat API 调用提供极低延迟，支持 24 小时监控，并可直接将报告推送到 WeChat——形成完整的闭环生态系统。

Tencent Cloud 的 Lighthouse 轻量级服务器上的 OpenClaw 用户已超过 10 万，Tencent Cloud 表示，Lighthouse 的单日部署量自产品推出以来超过了历史峰值。

### 2. QClaw——本地安装，支持 WeChat/QQ 集成
QClaw 是 Tencent PC Manager 的官方产品。用户只需下载安装包即可立即开始使用——无需命令行编码。其最具差异化的竞争优势是原生 WeChat/QQ 集成：用户可以通过 WeChat 或 QQ 发送消息，直接控制电脑执行任务。

下载并安装（约 3 分钟）后，用户可以通过手机上的 WeChat 发送命令远程控制笔记本电脑。

### 3. WorkBuddy——企业 AI Agent
Tencent 发布了 WorkBuddy，这是一款专为职场设计的 AI agent，完全基于 OpenClaw 运行。由于用户流量激增，WorkBuddy 在 3 月 10 日上午因用户访问量远超预期而出现登录和服务不稳定问题，这是其国内公测上线后的情况。

### 4. 企业和安全基础设施
Tencent 推出了企业解决方案，包括支持 Linux、Windows 和云手机的云桌面镜像，这些镜像预装了 OpenClaw 环境。Tencent Computer Manager 18.0 还推出了“AI Security Sandbox”，为 OpenClaw 和其他 Agent 工具提供系统级隔离和行为监控。

对于云部署，Tencent Cloud Lighthouse 和 ClawPro 增强了架构，支持环境隔离和快照回滚。Tencent Cloud AI Agent Security Center 提供 AI agent 的集中管理，监控异常命令并扫描技能相关风险。

### 5. 模型集成
Tencent Cloud 集成了多个主流大模型，包括 Tencent HY 2.0 Instruct、GLM-5、Kimi-k2.5 和 MiniMax-M2.5，并支持 Codebuddy、OpenClaw、Claude Code、Cline 和 Cursor 等工具。

---

## 商业模式

Tencent 的 OpenClaw 商业模式是经典的**“免费入门，付费使用”（freemium + pay-as-you-go）**策略，具有多条收入来源：

### 1. 免费安装，付费基础设施
商业逻辑很简单：安装免费；云服务器租赁、带宽和 API 调用付费。Tencent 的官方文档直言不讳：“OpenClaw 来自开源社区。云应用免费。”下一行补充道：“云服务器和 API 按实际使用计费。”

### 2. 云服务器订阅（Lighthouse）
价格通常为每月 30–60 元。与 SaaS web 版本的订阅模式相比，这种“租电脑”方式对重度脚本用户更具成本效益。

### 3. 基于 Token 的 API 计费
Tencent Cloud 澄清，虽然安装 OpenClaw 免费，但用户在使用大模型时可能因 token 消耗而产生费用。此次澄清源于有用户被收费超过 200 元的报道，Tencent Cloud 将其归因于历史模型 API 调用，而非安装本身。公司强调，基于 token 的计费是类似工具的常见做法。

云服务提供商和大模型制造商已成为这场“龙虾热潮”的最早受益者，作为“工具供应商”。Tencent Cloud 智能开发平台上的一些模型甚至因需求激增而涨价。

### 4. 通过生态系统实现战略锁定
该策略类似于 2000 年代初中国电信的 PHS 策略：以低进入门槛吸引用户，然后通过 recurring 服务费留住他们。通过将 OpenClaw 深度集成到 WeChat、QQ、Enterprise WeChat 和 Tencent 云基础设施中，Tencent 使用户难以脱离其生态系统。

### 5. 企业级升级销售
Agent Development Platform (ADP) 引入了企业级部署解决方案，集成权限管理和安全审查，针对需要合规、安全和规模的企业——以溢价定价。

---

## 总结表格

| 产品 | 目标用户 | 部署方式 | 收入来源 |
|---|---|---|---|
| Lighthouse (Cloud) | 开发者、中小企业 | 一键云部署 | 服务器订阅（30–60 元/月）+ API tokens |
| QClaw | 普通消费者 | 本地 PC | 免费（公测）；未来变现待定 |
| WorkBuddy | 企业 | 云端 | 企业授权 |
| ADP Platform | 企业开发者 | 云端 | 企业 SaaS + 计算资源 |

参考资料：

- [Tencent Cloud OpenClaw Deployment Page](https://www.tencentcloud.com/act/pro/intl-openclaw)
- [Tencent Cloud Lighthouse Product](https://intl.cloud.tencent.com/en/products/lighthouse)
- [OpenClaw China Adoption Analysis — CIW News](https://www.ciw.news/p/openclaw-china-frenzy)
- [OpenClaw Deployment Showdown: Tencent vs ByteDance & Others](https://www.xugj520.cn/en/archives/openclaw-deployment-solutions-comparison.html)
- [Tencent Cloud Clarifies OpenClaw Billing Policy — Phemex](https://phemex.com/news/article/tencent-cloud-clarifies-openclaw-billing-free-installation-usage-fees-apply-65830)
- [Tencent Jumps 6.2% on OpenClaw AI Frenzy — Yahoo Finance](https://finance.yahoo.com/news/tencent-jumps-6-2-openclaw-143115350.html)
- [Behind the AI Lobster Craze — Futunn](https://news.futunn.com/en/post/69903888/behind-the-ai-lobster-craze-domestic-large-models-dominate-rankings)
- [Chinese Tech Giants Offer Cheap OpenClaw Access — SCMP](https://www.scmp.com/tech/article/3346090/chinese-tech-giants-offer-cheap-easy-access-openclaw-amid-lobster-fever)
