---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 允许Cloudflare API令牌中的所有IP
translated: true
type: note
---

**问题：** 如何在Cloudflare API token的IP地址过滤字段中允许所有IP地址？

**答案：**

最简单的方法是将**IP地址过滤字段完全留空** —— 不添加任何条目意味着没有限制，因此该token可以从任何IP使用。

如果你确实需要输入明确的“允许所有”CIDR范围，请添加以下两个条目：

| 条目 | 覆盖范围 |
| --- | --- |
| `0.0.0.0/0` | 所有IPv4地址 |
| `::/0` | 所有IPv6地址 |

将每一项输入到字段中，然后按**Enter**（或点击添加按钮）确认，最后提交表单。

**推荐方法：** 直接留空该字段。Cloudflare的IP过滤是选择加入的——空列表意味着无限制访问，这与`0.0.0.0/0` + `::/0`功能相同，但更简洁。

---

**参考文献：**

- [Cloudflare API Tokens – Create and manage tokens](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
- [Cloudflare API Token IP restrictions](https://developers.cloudflare.com/fundamentals/api/reference/restrictions/)
