---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Anthropic 在 Bedrock 上屏蔽中国用户
translated: true
type: note
---

问题：Anthropic 模型 (Claude) 是否即使在 AWS Bedrock 上也在封锁中国用户？

回答：

是的 —— **Anthropic 的限制同样适用于通过 AWS Bedrock 使用模型的情况**，而不公局限于直接使用 API。这就是为什么你会看到如下错误：

> “Access to Anthropic models is not allowed from unsupported countries…” (不允许从不支持的国家/地区访问 Anthropic 模型……)

### 1. Anthropic 明确封锁中国（即使通过 AWS Bedrock）

Anthropic 的政策**禁止从中国访问**，且 AWS Bedrock 的客户必须遵守 Anthropic 的最终用户许可条款。
一位 AWS 发言人证实，**不允许在中国通过 Bedrock 或 Anthropic API 访问 Claude**。([Voice of America][1])

这意味着：

* 直接使用 Claude API → 被封锁
* 通过 AWS Bedrock 使用 Claude → 依然被封锁
* 通过云分销商使用 Claude → 仍受限制

### 2. 他们进一步扩大了限制（不仅限于 IP 所在地）

在 2025 年的政策更新中，Anthropic **在全球范围内封锁了中国控制的公司**，即使这些公司托管在海外。([CRN Asia][2])

因此，限制可能会通过以下方式触发：

* IP 所在地（中国）
* 账单账户所在国家
* 公司所有权（中国实体）
* 可疑的路由/代理

### 3. “不支持的地区”名单排除中国

Anthropic 仅在特定国家/地区启用 Claude；在不支持的地区使用违反了 ToS（服务条款），可能会被封锁。([Anthropic][3])

这就是为什么你会收到：

```
ValidationException: Access to Anthropic models is not allowed...
```

### 4. 为什么即使是 Bedrock 也无法绕过

因为 Bedrock 只是一个 **hosting layer（托管层）**。模型提供商 (Anthropic) 仍然强制执行：

* export controls（出口管制）
* 国家安全规则
* ToS 地区限制

AWS 明确表示 **第三方模型的限制依然适用**。([Amazon Web Services, Inc.][4])

---

### 5. 实际影响

典型表现：

| 场景 | 结果 |
| ------------------------------- | ------------------------- |
| 中国 IP + Bedrock | ❌ 被封锁 |
| 中国 AWS 账户 | ❌ 经常被封锁 |
| 中国公司使用美国区域 | ❌ 仍可能被封锁 |
| 美国/欧盟 AWS 账户 | ✅ 正常使用 |
| Proxy/VPN | ⚠️ 有时可用，但有风险 |

---

### 6. 限制在 2025–2026 年变得更加严格

Anthropic：

* 封锁了关联中国的公司
* 加强了对不支持地区的执法力度
* 出于合规/安全原因，愿意损失相关收入 ([www.ndtv.com][5])

所以，是的 —— **他们正在积极收紧访问权限**。

---

### TL;DR（简明总结）

是的。
即便是在 AWS Bedrock 上，**Anthropic 也会封锁中国用户**。
Bedrock 并不能绕过 Anthropic 的区域限制。

---

如果你正尝试通过以下方式使用 Claude：

* Bedrock
* OpenRouter
* Cursor / Claude Code
* API

请告诉我是哪一种 —— 我可以解释哪些配置目前仍然有效，以及哪些会失败。

[1]: https://www.voanews.com/a/chinese-entities-turn-to-amazon-cloud-rivals-to-access-us-chips-ai/7754150.html?utm_source=chatgpt.com "Chinese entities turn to Amazon cloud, rivals to access US ..."
[2]: https://www.crnasia.com/news/2025/artificial-intelligence/anthropic-tightens-ai-access-rules?utm_source=chatgpt.com "Anthropic tightens AI access rules, targeting Chinese- ..."
[3]: https://www.anthropic.com/supported-countries?utm_source=chatgpt.com "Supported countries & regions"
[4]: https://aws.amazon.com/legal/bedrock/third-party-models/?utm_source=chatgpt.com "Serverless Third-Party Models on Amazon Bedrock - AWS"
[5]: https://www.ndtv.com/world-news/anthropic-blocks-ai-model-claude-access-for-firms-linked-to-chinese-communist-party-11143362?utm_source=chatgpt.com "Anthropic Blocks AI Access For Firms Linked To Chinese ..."
