---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Nexus 令牌过期策略详解
translated: true
type: note
---

我需要搜索关于 Nexus user tokens 及其 expiration policies 的最新信息。是的，如果管理员启用此功能，Nexus user tokens 可以设置过期日期。以下是关键细节：

**Token Expiration 设置：**

- 管理员可以启用 user token expiration，并设置 1-999 天之间的过期周期，默认值为 30 天
- 此功能在 Nexus Repository 3.69.0 版本中引入
- 启用 token expiration 后，它将同时应用于现有 tokens 和新创建的 tokens，过期时间从 token creation date 开始计算

**重要注意事项：**

- Token expiration 是一个**可选（optional）**功能，管理员必须明确启用
- 如果未启用，tokens 可能会无限期有效（出于 security 原因，不建议这样做）
- 在现有部署中启用过期功能时，在该功能开启前创建的 tokens 也将根据其原始创建日期受到过期限制

**Best Practice：**

建议启用 token expiration 作为良好 security hygiene 的一部分，因为这会强制执行定期的 credential rotation，并降低被泄露 tokens 被长期使用的风险。

您可以向您的 Nexus 管理员确认您的实例中是否启用了 token expiration，以及过期周期设置为多少。
