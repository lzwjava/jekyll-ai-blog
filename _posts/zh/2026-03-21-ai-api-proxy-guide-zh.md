---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI API 代理通道比较指南
translated: true
type: note
---

问题：在这个服务选择界面中显示的不同 AI model 访问通道组有哪些，它们是什么意思？

答案：

这似乎是一个 **third-party AI API proxy/aggregator platform**（很可能是一个中国服务，向各种 AI models 重新销售访问权限）。界面列出了用户可以路由请求的不同“通道”或“组”，每个都有一个 **cost multiplier (倍率)**。以下是每个组的分解：

---

## Claude (Anthropic) 通道

| 分组 | 倍率 | 描述 |
|---|---|---|
| **Claude Max** | 1.3x | 最佳质量；使用 Claude Max 账户 |
| **Claude Max 备用 (Backup)** | 2.1x | 使用 Max 20X 账户；由于风控，成本激增，因此暂时更高费率 |
| **AWS Bedrock** | 5x | 通过 Amazon Web Services Bedrock 的官方 Claude API — 最稳定但最贵 |
| **AWS Bedrock 低价 (Low Price)** | 2.6x | 相同的 AWS Bedrock 官方通道，略不稳定但更便宜 |
| **CC-Azure** | 1.3x | 通过 Microsoft Azure 云托管的 Claude |
| **CC-逆向渠道B (Reverse Channel B)** | 0.8x | 非官方逆向工程代理；支持 Opus 4.6；质量与 Max 相当 |
| **CC-反重力逆向 (Anti-Gravity Reverse)** | 0.8x | 另一个非官方逆向代理通道 |
| **kiro标准版 (Standard)** | 0.15x | 最便宜的 Claude 选项；不支持 Opus model |
| **kiro企业版 (Enterprise)** | 0.4x | 支持 Opus model；企业级 |
| **CC-TEST分组** | 0.15x | 测试组 — 当前不可用 |
| **CC-其他逆向 (Other Reverse)** | 0.3x | 仅支持 Opus 4.5 和 Haiku 4.5 — 当前不可用 |

---

## OpenAI (GPT) 通道

| 分组 | 倍率 | 描述 |
|---|---|---|
| **Codex (Team)** | 0.3x | 使用 GPT Team + 常规账户池；优先级低于 GPT Pro |
| **Codex (GPT Pro)** | 0.6x | 更高品质；支持所有 Codex models；GPT Pro 账户池 |

---

## Google 通道

| 分组 | 倍率 | 描述 |
|---|---|---|
| **gemini官方 (Gemini Official)** | 0.4x | 官方 Google Gemini API 通道 |

---

## 关键概念解释

**什么是“倍率”（multiplier/rate）？**
这是相对于基础 token 价格的成本缩放因子。5x 费率意味着你支付 5× 基础 token 成本。0.15x 费率意味着你只支付基础成本的 15%。

**什么是“逆向渠道”（reverse channels）？**
这些是 **unofficial reverse-engineered proxies** — 它们拦截 Claude 的 web 接口流量，而不是使用官方 API。它们更便宜，但：

- 稳定性较低
- 可能违反 Anthropic 的服务条款
- 可能不可预测地被封锁/限速（如备用 Max 通道的风控问题所示）

**什么是“官方通道”（AWS Bedrock、gemini官方 等）？**
这些通过各自提供商的 **actual official enterprise APIs** 路由，提供更好的稳定性、合规性和可靠性 — 但成本更高。

**当前选择的通道是哪个？**
界面显示 **Claude Max 备用 (Backup)** 当前被选中（由复选标记 ✓ 表示）。
