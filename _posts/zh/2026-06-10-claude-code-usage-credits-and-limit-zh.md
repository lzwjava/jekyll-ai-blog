---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Code 使用额度与限制
translated: true
type: note
---

**问题：** 在 Claude Code 中，`/usage-credits` 命令和月度限制是如何运作的？

**回答：**

`/usage-credits` 控制的是*超额*消费层，而非你套餐中包含的使用量。其逻辑模型分为三个层级：

1. **套餐内使用量**——你的 Pro/Max 订阅提供一定配额，受 5 小时会话窗口和 7 天周上限约束，claude.ai 聊天、桌面应用和 Claude Code CLI 均共享同一预算。这部分是固定费率，你通过 `/usage-credits` 设置的任何内容都不会影响它。

2. **使用额度（按量付费的超额部分）**——当你在会话中耗尽包含的配额时，请求不会受阻，而是开始按标准 API 费率从预付费的额度余额中计费，该费用独立于订阅另行收取。你可以在 claude.ai 的 Settings > Usage 中启用并充值：启用使用额度，添加支付方式，然后通过“Add funds”预存资金。

3. **你刚设置的月度限制（$10）**——这是对层级 2 的消费上限。在 Pro 和 Max 套餐中，`/usage-credits` 设定了使用额度的月度消费上限。如果你达到该上限但仍有可用的额度余额，Claude Code 会提示你提高或移除限制，以便在不离开 CLI 的情况下继续使用。更改限制需要账户的计费访问权限。

因此具体来说：你的订阅配额正常消耗 → 配额耗尽 → 超额计费按 API token 费率启动 → 一旦本月内超额消费累计达到 $10，Claude Code 会停止并请求你提高上限。这是一个断路器，而非你必须花掉的预算。该限制每月重置；预付费余额本身会一直保留直至用完。

作为高频用户，有两点值得了解：

- **使用量套餐**：如果你预期会频繁超额，预先购买的使用量套餐可享受比标准使用额度费率最高 30% 的折扣，更大套餐折扣更多，余额可在 Claude、Claude Code、Cowork 及第三方产品之间共享。
- **独立的编程池**：自 2026 年 6 月 15 日起，Agent SDK 和 `claude -p` 的使用将不再计入你的套餐限制，而是从独立的月度 Agent SDK 额度中扣除——终端中的交互式 Claude Code 仍使用你的常规套餐配额。因此，如果你正在编写无头 `claude -p` 管道（这很符合你的风格），其计量方式与你的 `/usage-credits` 上限不同。当该 SDK 额度用尽后，额外使用只有在启用使用额度的情况下才会按 API 费率计入；否则 SDK 请求会停止直至额度刷新。

CLI 快速查询：`/usage` 显示你的会话/周进度条及重置时间；`/cost` 显示当前会话的 token 消费。

**参考资料：**

- [有效管理成本 — Claude Code 文档](https://code.claude.com/docs/en/costs)
- [管理付费 Claude 套餐的使用额度 — Claude 帮助中心](https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans)
- [购买使用量套餐 — Claude 帮助中心](https://support.claude.com/en/articles/14246112-buy-usage-bundles)
- [将 Claude Agent SDK 与你的 Claude 套餐一起使用 — Claude 帮助中心](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)