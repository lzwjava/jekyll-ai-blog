---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 升级导致无可用账户错误
translated: true
type: note
---

**问题：** 升级到版本 2.1.78 后，Claude 开始报告 "no available accounts" 错误。"Claude Max" 组出现问题，而 "CC-逆向渠道B" 正常工作。发生了什么？

**答案：**

升级到版本 2.1.78（如同项目升级指南中的示例所示）引入了来自 claude-relay-service 主分支的最新更改。这些更新包括对 account routing、error handling、cooldown logic 和 validation rules 的重大改进。这是 "no available accounts" 错误突然仅在 "Claude Max" 组中出现的最可能原因。

触发问题的关键更改（基于 2026 年 3 月左右的最新发布）：
- Account blocking reasons 现在在 UI 中清晰显示（以前隐藏或误诊）。
- 修复了 false 429 rate-limit 标记和 503 backoff 行为，并添加了可配置的 cooldown TTLs。
- 更新了对 team accounts、1M context flags（`allow1mContext`）和 free-tier 误识别的处理方式——这些可能会突然将先前正常工作的账户标记为不可用。
- 移除旧的 models/context windows 硬限制，现在依赖 admin/API-key 设置。

"Claude Max" 很可能是一个使用官方 Anthropic OAuth 账户或特定池的组，受更严格/修正的 validation 影响。相比之下，"CC-逆向渠道B"（您的逆向/代理渠道）使用不同的账户集或 proxy 设置，未受相同 routing blocks 影响。

您共享的 dashboard 显示使用量很低（今天 $0.1052）和最近时间戳（03/18/2026），这符合升级后重启时账户可能被自动标记的状态。

**快速修复方法：**
1. 转到 web 管理 UI（通常在您的服务器上的 `/web`）。
2. 选择 "Claude Max" 组 → 检查 "routing-block reasons" 列（现在显示确切的错误类型、状态码和剩余 cooldown）。
3. 点击受影响账户的 "Reset Status"。
4. 验证每个账户的 proxy 设置和 `allow1mContext` 标志（如果使用 1M models）。
5. 重启服务（`npm run service:restart:daemon`）并再次测试。

如果 block reasons 指向上游 Anthropic 错误，您可能需要在 `.env` 或 Admin UI 中添加 per-account cooldown overrides。"CC-逆向渠道B" 组继续工作证明核心服务正常——只需关注 "Claude Max" 账户池。

这是 2026 年 3 月 account-management 重构后的常见升级后行为；不是您的设置 bug。

**参考：**
- [https://github.com/Wei-Shaw/claude-relay-service/blob/main/README_EN.md](https://github.com/Wei-Shaw/claude-relay-service/blob/main/README_EN.md)
- [https://github.com/Wei-Shaw/claude-relay-service/releases](https://github.com/Wei-Shaw/claude-relay-service/releases)
