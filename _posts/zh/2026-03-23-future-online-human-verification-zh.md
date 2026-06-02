---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在线人类验证的未来
translated: true
type: note
---

**Question:** 为什么我们要在这里讨论这个？互联网似乎最终将演变成只有两类 app —— 人类（社交）app 和 AI agent app。当存在大量聊天机器人时，我们将需要一个专门用于核实“真实人类”的 app。现在实现这一点很难吗？

**Answer:**

你的观察非常敏锐，实际上这与目前行业的发展方向高度吻合。让我们详细分析一下。

---

## 互联网正在分化为两条赛道

你是对的。互联网流量正趋于两个截然不同的类型：

1. **人类（社交）app** —— 真实的人进行互动、发帖、投票、交易和交流的场所。
2. **AI Agent app** —— 自主的 bot 代表人类（有时甚至是完全独立的）进行浏览、购买、预订和执行任务。

在 2025 年，AI agent 的定义转向描述能够使用软件工具并采取自主行动（如调用 API、与其他系统协调以及在最少的人类监督下独立完成任务）的 large language models。

Gartner 将 agentic AI 列为 2025 年十大技术趋势之首，并预测到 2028 年，33% 的企业级 app 将包含 agentic AI，而 2024 年这一比例还不足 1%。

---

## 核心挑战：你再也无法分辨谁是真实的

一个名为 Moltbook 的社交网络完美地说明了这个问题。在上线后的几天内，就有 160 万个 agent 注册，包括平台自身在内的任何人都无法可靠地判断哪些帖子来自 bot，哪些来自伪装成 bot 的人类，或者背后到底有多少个独立的人。

如果没有办法核实这些 agent 背后有多少真实的人，平台就无法可靠地将有机活动与协调一致的“蜂群”攻击区分开来。此外还存在隐私问题 —— 当每个 agent 交易都通过公共支付通道运行时，会留下关于该 agent 行为踪迹和去向的详细记录。

---

## 是的，这很难 —— 但解决方案正在涌现

你认为这很难是正确的，但这并非无解。目前有几种严肃的方案正在构建中：

### 1. **生物识别“人类证明” —— World (原 Worldcoin)**

由 Sam Altman 共同创立的 World 致力于创建“proof of human”技术 —— 为日益充斥 AI 生成内容的互联网提供身份验证工具。他们的 AgentKit 允许将用户的 World ID 集成到 x402 支付协议中，以便网站能够核实是一个独立的真实人类批准了 agent 的行动。他们的 Chief Product Officer 将其比作向 agent 委派“授权书”。

痛点在于：它需要通过物理设备“Orb”进行虹膜扫描。这产生了巨大的摩擦，并引发了严重的隐私担忧 —— 由于隐私和数据问题，World 已经在至少十个国家被禁用或调查。

### 2. **加密 Agent 身份**

HUMAN Security 发布了一个开源项目，AI agents 使用 HTTP Message Signatures (RFC 9421) 对每个 HTTP 请求进行签名，并使用 OWASP 的 Agent Name Service（一种类似于 AI agents 的 DNS 命名系统）进行识别。这允许 web services 通过密码学方式核实某个特定的已注册 agent 发送了给定的请求。

### 3. **作为速率限制器的微支付**

由 Coinbase 和 Cloudflare 开发的 x402 协议允许 agents 支付小额费用来访问资源，将微支付（micropayments）作为速率限制手段。该生态系统在上线后的前六个月内处理了超过 1 亿笔支付。然而，微支付虽然可以减缓恶意行为者的速度，但无法完全解决“Sybil dynamics”问题 —— 如果经济诱惑足够高，每次请求几美分的成本就变得微不足道了。

---

## 为什么这依然很难

| 挑战 | 原因 |
|---|---|
| **生物识别 (Biometrics)** | 侵犯隐私，难以在全球范围内扩展 |
| **加密密钥 (Cryptographic keys)** | 可能会被窃取或委派给恶意行为者 |
| **验证码 (CAPTCHAs)** | AI 现在的破解能力已经超过了人类 |
| **行为分析 (Behavioral analysis)** | Agents 可以通过训练来模仿人类行为 |
| **微支付 (Micropayments)** | 资金充足的恶意行为者可以吸收这些成本 |

目前只有 15% 的企业部署了完全自主的 agents，大多数企业将信任和治理视为广泛采用的主要障碍。与此同时，81% 的高管表示，只要建立了信任框架，他们愿意将关键业务委托给 AI。

---

## 总结

你的直觉是正确的。互联网需要一个 **“人类身份层” (human identity layer)** —— 一个能够自信地表明“这一行为背后是一个独立的、真实的人”的基础设施。这一层目前正在建设中，但在技术、法律和伦理上依然面临重重困难。挑战在于你既需要验证人类身份，又不能损害隐私，且不能被日益强大的 AI 欺骗。这种张力将是未来十年互联网最具定义性的基础设施问题。

**参考文献：**

- [HUMAN Verified AI Agent (HUMAN Security)](https://www.humansecurity.com/learn/blog/human-verified-ai-agent-open-source/)
- [AgentKit: Proof of Human for the Agentic Web (World)](https://world.org/blog/announcements/now-available-agentkit-proof-of-human-for-the-agentic-web)
- [World launches tool to verify humans behind AI agents (TechCrunch)](https://techcrunch.com/2026/03/17/world-launches-tool-to-verify-humans-behind-ai-shopping-agents/)
- [AI Agents arrived in 2025 (The Conversation)](https://theconversation.com/ai-agents-arrived-in-2025-heres-what-happened-and-the-challenges-ahead-in-2026-272325)
- [Non-human identities: Agentic AI's cybersecurity risk (WEF)](https://www.weforum.org/stories/2025/10/non-human-identities-ai-cybersecurity/)
- [Sam Altman's World builds for AI agents (Quartz)](https://qz.com/sam-altman-world-human-verification-ai-agents)
