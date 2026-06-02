---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 静态路由管理距离默认值
translated: true
type: note
---

**B) 1**

在 Cisco 路由器中（此问题在 CCNA 等网络认证中最常见的语境），静态路由的默认管理距离（AD）是 **1**。AD 对路由来源的可靠性进行排名——值越低越优先。

- 直连接口的 AD 为 0（最优先）。
- 静态路由的 AD 为 1（优先于动态协议）。
- 作为比较：OSPF 为 110，RIP 为 120。

这就是为什么静态路由会覆盖指向同一目的地的动态学习路由，除非手动增加静态路由的 AD（例如，用于浮动静态备份）。

来自可靠来源的证据：

- Cisco 官方文档和社区确认静态路由默认 AD 为 1。
- 标准 AD 表格列出：Static = 1、OSPF = 110、RIP = 120。

选项 C (110) 和 D (120) 分别是 OSPF 和 RIP 的默认值，而 A (0) 用于直连网络。
