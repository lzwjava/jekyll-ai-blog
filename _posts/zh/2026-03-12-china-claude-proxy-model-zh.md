---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国 Claude 代理共享模型
translated: true
type: note
---

问题：什么是“Claude Code mirror”服务，特别是在中国？具体来说，它作为代理/中继服务器的分发模式——一个人购买 Max 计划并与多人共享？

回答：

## 中国中的“Claude Code Mirror”是什么？

### 背景：为什么存在

Claude（以及 Claude Code）在**中国大陆被官方屏蔽**。Anthropic 不支持中国支付方式，中国 IP 地址经常被拒绝，并且从 2025 年 9 月 5 日起，Anthropic 正式宣布一项政策，禁止所有“中国控制的公司”使用 Claude 服务，包括 API 和 Web 产品。这催生了一个巨大的灰色市场 workaround 服务。

---

### 什么是“Claude Code Mirror”？

**Claude Code mirror**（也称为“CC mirror”、镜像服务或 relay service）是一个**第三方代理/中继平台**，位于中国用户和 Anthropic 官方服务器之间。这些是第三方平台，为中国开发者提供 Claude Code mirror 访问，提供与 API 兼容的服务层，实现稳定访问——未经 Anthropic 官方授权。

关键机制：mirror 服务**拦截您的 API 请求**，并代表您转发到 Anthropic，使用托管在合规地区（中国以外）的服务器。用户只需将 `ANTHROPIC_BASE_URL` 环境变量更改为指向 mirror，而不是直接指向 Anthropic 的服务器。

---

### “Bus” / 共享池模式（拼车 / 合租）

您的“bus”比喻非常贴切。在中国开发者社区中，这俗称为**拼车**或**合租**。以下是商业模式的工作原理：

**运营商一方：**
- 某人购买 Claude Max 计划（$100–$200/月）或 Anthropic API key
- 他们部署反向代理 / 中继服务器（工具如 `claude-relay-service` 或自定义 API 网关）
- 他们向众多用户转售访问权，按 token 收费或通过 RMB 订阅费
- 运营商从多人处收取收入，用于覆盖官方计划成本，并额外获利

**用户一方：**
- 用户以 RMB（人民币）支付——通常约 200–300 RMB/月
- 这些 mirror 站点通常允许使用普通邮箱注册，绕过外国手机号或地址需求，定价通常以 RMB 显示。例如，标准使用计划约 359 RMB/月，可能比直接兑换和手续费更划算。
- 用户获得 API 端点 + API key，只需将 `ANTHROPIC_BASE_URL` 设置为 mirror 的 URL

**中继服务基础设施：**
开源工具如 `claude-relay-service` 作为中间件层，转发请求，同时管理认证、路由和成本分担场景。该系统特别适用于希望 pooling 访问或简化与不同 AI 后端集成的团队或社区。

---

### 该生态系统中的服务类型

有几种不同的模式：

| Type | How It Works | Risk Level |
|---|---|---|
| **Official API reseller** | Buys Anthropic API credits, resells at markup | Medium |
| **Subscription sharing (Max pooling)** | One Max plan shared among many users | High — violates ToS |
| **Third-party reverse-engineered** | Uses technical exploits/unofficial endpoints | Very High |
| **VPN + direct access** | User configures VPN proxy themselves | Lower, but still restricted |

---

### 法律与风险问题

这是关键部分：

1. **违反 Anthropic 服务条款**——未经授权共享订阅账户或转售 API 访问明确违反 ToS。2025 年下半年，多家 Claude 转售服务因 Anthropic 加强风险控制而关闭，导致预付费用户重大损失。

2. **账户封禁**——Anthropic 具有多层检测机制，检查 IP 地址、DNS 泄漏位置、浏览器指纹和设备指纹。中国大陆 IP 范围被拒绝，数据中心 IP 或共享 VPN IP 被标记为高风险。

3. **运营商消失风险**——2025 年新兴的第三方 Claude 逆向工程服务中，超过 60% 在运营 3 个月内关闭或消失。预付费用户损失资金。

4. **安全风险**——当您将所有代码和提示通过第三方中继路由时，该运营商可能记录您的代码、API 调用和数据。

5. **中国政策**——第三方逆向工程服务利用技术漏洞提供非官方服务，违反 Anthropic 服务条款，并可能随时被封禁。

---

### 中国开发者的合法替代方案

- **VPN + 官方直连账户**——使用住宅 IP VPN（非数据中心），用虚拟国际卡如 WildCard 支付。工具如 Clash 配合中国以外的代理服务器；只需在 shell 中配置 `HTTPS_PROXY` 环境变量，让 Claude Code CLI 和终端正确通过代理路由。
- **按使用付费 API 通过合规平台**——一些平台如 apiyi.com 在合规地区部署服务器，提供 Claude API 访问，按使用付费，对轻度用户可能更便宜。
- **Anthropic 官方 Team/Enterprise 计划**——这些为组织提供更多灵活性。

---

### 总结

中国中的“Claude Code mirror”本质上是**付费中继代理服务**，解决访问和支付障碍。“bus/pooling”模式特指运营商将众多用户 pooling 到一个或少数账户/API key 上，以 RMB 加价向用户收费。虽然流行且实用，但这些服务存在**真实风险**：违反 ToS、账户封禁、运营商欺诈、数据安全问题和不稳定性。

参考资料：

- [How I Got Claude Code Working in China](https://gist.github.com/docularxu/aa321d6bc4cfe3abde3c098ee42f9908)
- [Lumecoder: Claude Code Mirror (China Direct)](https://lumecoder.com/claude-code-mirror)
- [Claude Code Subscription Purchase Guide for China (apiyi.com)](https://help.apiyi.com/en/claude-code-subscription-purchase-guide-en.html)
- [Claude Account Ban Solutions for China Users 2025 (apiyi.com)](https://help.apiyi.com/claude-account-ban-solutions-china-users-2025-en.html)
- [Navigating Claude's Payment Maze from China (Oreate AI)](https://www.oreateai.com/blog/navigating-claudes-payment-maze-your-guide-to-subscribing-from-china/36e37a9f66d4f611b269f61d2c8e836d)
- [Claude Relay Service (SourceForge mirror)](https://sourceforge.net/projects/claude-relay-service.mirror/)
- [Fix: Claude Code 403 in China (GitHub Issue)](https://github.com/anthropics/claude-code/issues/30318)