---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude API 中国中继服务
translated: true
type: note
---

claude-relay-service 是一个自托管的 proxy/relay 工具，它允许用户将请求转发到 Anthropic 官方的 Claude API。它支持添加多个付费 Claude 账户（通过 OAuth），在它们之间自动轮换，为每个用户生成自定义 API key，使用跟踪和成本分摊。该服务本身 **不** 提供 Claude 访问或计划——你必须已经有有效的付费 Claude 账户（例如高阶的 "Claude Code Max" 订阅）才能添加它们。这种设置在中国很受欢迎，用于分发访问权限，因为它允许一个或几个高限额账户在许多用户之间共享（通常 3–5 人分摊成本），同时将数据保存在自己的服务器上。

### 中国人如何获取 “max plan” 并分发访问权限
“Max plan” 通常指 Claude Pro（网页/聊天）或更高阶的 Claude Code Max / Opus 级访问，用于高级模型和更高的 API 速率限制。Anthropic 不官方支持中国大陆，因此使用中国 IP、电话或卡直接注册会被屏蔽或失败。中国用户（公民或居民）通过组合工具和服务绕过此限制，然后使用像 claude-relay-service（或其他类似开源代理）的 relay 服务来转售或共享访问权限。

获取 max plan 账户的常见步骤：
1. **VPN / Proxy**：连接到干净的 US 或加拿大节点（注册和 relay 设置中的 OAuth 必需）。
2. **Email**：使用全新的 Gmail 或其他国际邮箱（许多人购买或自行注册）。
3. **虚拟电话号码**：几乎总是用于 Claude.ai 或 console.anthropic.com 注册时的 SMS 验证。热门平台包括 PingMe、5sim.net 或类似临时号码服务（每次验证成本约 0.5–2 元人民币）。
4. **虚拟信用卡用于支付**：中国银行卡通常被拒绝。用户在 WildCard、Coinepay 或 bpay.net 等平台上充值 USDT 以获取虚拟 US Visa/Mastercard。然后绑定此卡订阅 Claude Pro（约 $20/月）或更高 Code Max 阶层。该卡必须匹配 US 账单地址，并与一致的 US IP 一起使用。
5. **Fingerprint browser**（可选但常见，用于安全）：像 AdsPower 这样的工具保持浏览器指纹和 IP 一致，以降低管理多个账户时的封禁风险。

账户激活后：
- 对于网页/Pro：登录 claude.ai 并升级。
- 对于 API：前往 console.anthropic.com，绑定虚拟卡，申请 API key（批准后按使用付费）。

分发给他人（“reverse channel” 或 逆向渠道 方法）：
- 在服务器上自托管 claude-relay-service（推荐 US 地区 VPS）。
- 通过 OAuth 添加付费 Claude 账户（可能需要 proxy）。
- 通过 web 仪表板为每个客户生成唯一 API key。
- 通过微信群、淘宝店或论坛分享这些 key（或出售访问权限）。客户以人民币支付（支付宝/微信），而 relay 所有者承担 Anthropic 账单。
- relay 中的多账户轮换有助于避免速率限制和 503 错误。

这是大多数中国 relay 操作者和转售商的操作方式。对于不想麻烦设置的人，从国内平台购买现成账户或共享订阅也很常见。

### 风险和注意事项
所有这些方法在技术上违反 Anthropic 的服务条款（不支持中国、无账户共享）。如果 Anthropic 检测到 IP 不匹配、重复验证或异常使用，账户可能被封禁。relay README 明确警告用户接受所有风险。许多人轮换账户或使用 proxy 来最小化检测。

简而言之，中国公民使用上面描述的虚拟电话号码、国际邮箱、VPN 和 US 虚拟卡——没有使用大陆凭证直接合法购买 max plan 的方式。relay 服务使分发变得简单且盈利，前提是获取了主账户。

References:
- [claude-relay-service README_EN.md](https://github.com/Wei-Shaw/claude-relay-service/blob/main/README_EN.md)
- [2026 Latest Claude Pro Subscription & Registration Tutorial (Chinese methods)](https://github.com/imarvinle/Claude-Pro)
- [Claude Pro Payment with Virtual Cards Guide](https://sites.google.com/view/coinepaynet/visa_ka/Claude)
- [YouTube Tutorial on Safe Claude Registration with Virtual Number & WildCard](https://www.youtube.com/watch?v=vvD2jUZYPgI)
- [How to Use Claude in Unsupported Countries (VPN + alternatives)](https://writingmate.ai/blog/how-to-use-claude-3-in-unsupported-countries)
