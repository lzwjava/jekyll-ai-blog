---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub Copilot 转向令牌计费
translated: true
type: note
---

**问题：** GitHub Copilot 是否已改为按 Token 收费的定价模式？

**回答：**

是的——这项调整刚刚生效。所有 GitHub Copilot 套餐已于 2026 年 6 月 1 日转换为基于使用量的计费模式。不再统计高级请求次数，每个套餐现在都包含每月分配的 GitHub AI Credits（积分），使用量根据 Token 消耗量（输入 Token、输出 Token 和缓存 Token）按各模型公布的 API 费率计算。

运作机制如下：

- 每个 Token 根据所用模型定价，总消耗按 1 积分 = 0.01 美元的比例转换为 AI Credits。每个付费套餐包含与其价格等额的月度积分：Pro 套餐（每月 10 美元）包含 10 美元积分；Pro+ 套餐（每月 39 美元）包含 39 美元积分，超出部分可另行购买。
- **仍然免费的部分：** 所有套餐下的代码补全和“下一编辑建议”功能仍保持免费。本次计费变更仅影响聊天、智能体功能、智能体模式和代码审查所消耗的积分。如果自动补全是您的主要用途，则无任何变化。
- **已取消的部分：** 使用上限。以往重度使用受固定费用限制；现在除非您明确设置消费限额，否则将没有上限，而且 GitHub 默认仅在达到限额时通知您，而非停止使用。备用模型也已移除。
- **隐藏的第二计费项：** GitHub Copilot 代码审查现在运行在 GitHub Actions 上，因此审查一个 PR 将同时消耗您的 AI Credits 和包含的 Actions 分钟数。
- **年度套餐：** 年度 Pro/Pro+ 订阅用户在到期前仍沿用高级请求定价，但自 6 月 1 日起其模型乘数已上调；到期后除非升级为月度套餐，否则将降级为 Copilot Free。

模型费率（示例，每 100 万 Token）：Claude Haiku 4.5 最便宜，输入 1 美元 / 输出 5 美元；Claude Opus 最贵，输入 5 美元 / 输出 25 美元；GPT-5.4 nano 输入 0.2 美元 / 输出 1.25 美元，GPT-5.5 输入 5 美元 / 输出 30 美元。

社区反应强烈：开发者预计运行智能体会话的成本将增加 10 到 50 倍，账单从 29 美元飙升至 750 美元/月的报告在 Reddit、X 和 GitHub 的讨论区中随处可见。值得注意的原因：据 Ed Zitron 报道的内部 Microsoft 文件显示，自 2026 年 1 月以来，Copilot 的周均运行成本几乎翻了一番——智能体工作负载打破了固定费率的经济模式，这与去年 Cursor 重新定价的情况如出一辙。

**对您的实际建议：** 鉴于您每月约 10 亿 Token 的消耗量，Copilot 包含的 10-39 美元积分在智能体工作状态下几小时内就会耗尽。按此 Token 费率，您实际上是在支付 API 价格外加一个订阅外壳——对于智能体循环任务，使用 OpenRouter 搭配 deepseek-v4-flash/mimo-2.5-pro，或使用带有自身额度限制的 Claude Code 订阅，将便宜得多。只有当您纯粹将其用于免费的自动补全，并将所有聊天/智能体流量通过自己的 API 密钥路由时，Copilot 才具有合理性。

**参考链接：**

- [GitHub Copilot 将采用基于使用量的计费模式 — GitHub Blog](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)
- [GitHub Copilot Token 计费 2026：完整成本指南 — DEV Community](https://dev.to/akaranjkar08/github-copilot-token-billing-2026-full-cost-guide-and-alternatives-3bcf)
- ["真是个笑话"：Copilot 新的 Token 计费引发热议 — TechCrunch](https://techcrunch.com/2026/05/30/what-a-joke-github-copilots-new-token-based-billing-spurs-consternation-among-devs/)
- [社区讨论 #192948 — GitHub](https://github.com/orgs/community/discussions/192948)
