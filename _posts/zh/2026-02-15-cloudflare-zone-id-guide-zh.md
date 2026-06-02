---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 详解 Cloudflare 区域 ID (Zone ID)
translated: true
type: note
---

**Question:** 什么是 Cloudflare 中的 Zone ID？

**Answer:**

在 Cloudflare 中，**Zone ID** 是分配给您账户中每个 **zone** 的唯一标识符（一串长的字母数字字符串）。

Cloudflare 中的 **zone** 指的是您添加到 Cloudflare 进行管理的 domain（或有时是 subdomain）。这包括 DNS hosting、caching、security features（WAF、DDoS protection）、performance optimizations、Workers 等服务。简单来说，您连接到 Cloudflare 的每个 domain 都会成为一个 zone。

Zone ID 是在使用以下功能时引用特定 domain/zone 的主要方式：

- Cloudflare API（最常见的使用场景）
- 具有 zone-level 权限的 API tokens
- Cloudflare Workers 的 routes 或 bindings（当针对特定 domain 时）
- 与 Cloudflare 进行 per-domain 交互的第三方 integrations 或工具
- 某些高级配置（Terraform、wrangler 等 CLI 工具、automation scripts 等）

它**不是敏感信息** —— 与 API keys 或 tokens 不同，Zone ID（以及 Account ID）可以安全地公开分享而不会危害安全，因为它们仅用于标识资源，本身并不授予任何访问权限。

**如何找到您的 Zone ID：**

1. 登录 Cloudflare dashboard：<https://dash.cloudflare.com>
2. 从列表中选择您想要的 domain/zone
3. 进入该 domain 的 **Overview** 选项卡
4. 向下滚动到右侧边栏或底部标记为 **API** 的部分
5. 您会看到列出的 **Zone ID**（通常在 **Account ID** 旁边）
6. 点击 "Click to copy" 复制该值（它看起来类似于 `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`）

查看 zone 设置时，相同的信息也会出现在 URL 中（类似于 `/[account_id]/[zone_id]/...`）。

**References:**

- [Find account and zone IDs · Cloudflare Fundamentals docs](https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids)
- [Accounts, zones, and profiles · Cloudflare Fundamentals docs](https://developers.cloudflare.com/fundamentals/concepts/accounts-and-zones)
- [Cloudflare Community discussions on Zone ID](https://community.cloudflare.com/t/about-zone-id/47514)
