---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国境外 Claude 代码中继服务
translated: true
type: note
---

Question: 欧洲或南亚是否有类似于中国 pincc-v2 或 ssssai code 的 Claude Code relay services？

Answer:

是的——但在中国以外，**Claude Code relay services 主要是开源代理或小型社区中继**，而不是像中国那样的大型商业“拼车”平台。以下是主要类别：

---

# 1) pincc-v2 的直接等价物（self-hosted relay / pooling）

这些在全球通用（欧洲 / 南亚均可）：

### 1. Claude Relay Service (CRS / pincc-style)

* Claude / OpenAI / Gemini 的自托管中继
* 支持 **account rotation + pooling + cost sharing**
* 兼容 **Claude Code CLI**
* Docker 一键部署
* 常被团队用于替代购买共享账户

这本质上是与 pincc-v2 相同的架构。([Claude Relay Service][1])

---

### 2. claude-code-proxy (LiteLLM backend router)

* 将 Claude API 转换为 OpenAI / Gemini
* 作为 Claude Code 的即插即用中继
* 用于在 Claude Code 后端切换模型

这更技术化但非常灵活。([SourcePulse][2])

---

### 3. LunaRoute (local relay + session capture)

* Claude Code / Codex CLI 的本地代理
* 零延迟直通
* 完整会话记录 + 调试
* 任何地方均可使用（欧盟/亚洲）

如果您想要**私有中继而非共享服务**，则非常有用。([GitHub][3])

---

# 2) 社区中继服务（非中国但规模较小）

这些类似于 ssssai-code 风格：

### EasyClaude (commercial relay)

* 现成的 Claude Code 中继
* pooled plans
* 无需设置
* 企业级隔离

这基本上是**类似于中国拼车网站的托管中继**。([Easy Claude Code - Claude Code 中转服务][4])

---

# 3) 新兴社区代理（Reddit / 开发者社区）

这些在全球兴起：

* **RelayCode** — 将 Claude 切换到 DeepSeek/Qwen 的本地代理
* **CC-Relay** — 多提供商负载均衡代理
* **tingly-box** — 桌面 Claude Code 路由器

示例开发者描述：

> “RelayCode 运行本地代理… 将 Claude Code 切换到开源模型。” ([Reddit][5])

---

# 地区可用性

这些**均可在欧洲 / 南亚使用**，因为它们是：

* self-hosted
* local proxy
* VPS-deployable
* 无地区限制

与中国的服务不同，它们通常**不宣传特定地区**——只需部署在：

* EU VPS (Hetzner / OVH)
* India VPS
* Singapore VPS
* home server

---

# 为什么中国有更多此类服务

您可能注意到了：

中国：

* pincc-v2
* ssssai code
* aigocode
* sub2api
* CRS
* carpool sites

中国以外：

* 主要是开源
* 较少的共享账户转售商
* 更多 DIY

原因：

* 中国支付访问问题
* 高开发者需求
* 社区团购文化

---

# 最佳选项（中国以外）

如果您想要相同体验：

最相似：

* Claude Relay Service (CRS)
* EasyClaude (hosted)

最强大：

* LunaRoute
* CC-Relay
* claude-code-proxy

最轻量：

* RelayCode
* tingly-box

---

如果您告诉我：

* 想要 hosted（像 ssssai）
* 或 self-hosted
* 或最便宜的 pooling
* 或最快的

…我可以推荐**最佳选项**。

[1]: https://pincc.ai/en/?utm_source=chatgpt.com "Claude Relay Service - Self-hosted Claude API Relay | Claude Code Tutorial"
[2]: https://www.sourcepulse.org/projects/2336256?utm_source=chatgpt.com "claude-code-proxy by 1rgs - SourcePulse"
[3]: https://github.com/erans/lunaroute?utm_source=chatgpt.com "GitHub - erans/lunaroute: LunaRoute is a high-performance local proxy for AI coding assistants like Claude Code, OpenAI Codex CLI, and OpenCode. Get complete visibility into every LLM interaction with zero-overhead passthrough, comprehensive session recording, and powerful debugging capabilities."
[4]: https://easyclaude.com/en?utm_source=chatgpt.com "Claude Code Relay Service | Vibe Coding Platform | Easy Claude Code"
[5]: https://www.reddit.com/r/vscode/comments/1s4o8fi/route_claude_codecopilot_through_opensource/?utm_source=chatgpt.com "Route Claude Code/Copilot through Open-Source models with one click (RelayCode)"