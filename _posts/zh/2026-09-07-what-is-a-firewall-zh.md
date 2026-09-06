---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 什么是防火墙？
translated: true
type: note
---

问题：在计算中，"firewall"（防火墙）的含义是什么？

答案：防火墙是一种网络安全系统，根据预设的安全规则监控并控制进出网络的流量。它在可信的内部网络与不可信的外部网络（如互联网）之间充当屏障，决定允许或阻止哪些流量。

主要有以下几种类型：

- **包过滤防火墙** — 检查单个数据包，并根据 IP 地址、端口和协议进行过滤。
- **状态检测防火墙** — 跟踪活动连接的状态，基于流量上下文而非单个数据包做出决策。
- **应用层防火墙（代理防火墙）** — 在应用层运行，深入检查特定应用（如 HTTP、FTP）的流量。
- **下一代防火墙（NGFW）** — 将传统防火墙功能与深度包检测、入侵防御、应用感知等高级能力相结合。

主要功能包括：
- 阻止未授权访问
- 防止恶意软件进入或离开网络
- 强制执行组织安全策略
- 记录并监控网络活动

参考：
- [什么是防火墙？ — Cisco](https://www.cisco.com/c/en/us/products/security/firewalls/what-is-a-firewall.html)
- [防火墙 — MDN Web 文档术语表](https://developer.mozilla.org/en-US/docs/Glossary/Firewall)
- [防火墙（计算） — 维基百科](https://en.wikipedia.org/wiki/Firewall_(computing))