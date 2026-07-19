---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Grok-CLI 设置后被封锁
translated: true
type: note
---

**问题：** 一个中国用户刚配置好 grok-cli 工具就立刻被 grok.com 屏蔽，你怎么看这件事？

**回答：** 好不容易将 `grok-build` 这类工具配置好并集成到工作流中，却突然遭遇屏蔽，这确实令人非常沮丧。

grok.com 上显示的“抱歉，您已被屏蔽”通常与自动化网络安全系统（如 Cloudflare）有关，这类系统会针对特定流量特征触发拦截。当从中国访问该服务时，路由变更、VPN 服务器切换或高频的 API/CLI 请求很容易触发这些安全协议，导致临时或永久性的 IP 屏蔽。

如果你想尝试绕过封锁，可以调整代理规则，使用更干净、不那么拥挤的住宅 IP，清除浏览器 Cookies，或者转而使用其他能通过地区开发者平台稳定访问 Grok API 模型的替代平台。
