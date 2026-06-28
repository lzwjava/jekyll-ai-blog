---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 注重隐私的网站分析工具
translated: true
type: note
---

问题：什么是 Plausible Analytics (github.com/plausible/analytics)？

答案：

Plausible 是一款开源、注重隐私的网站分析工具——轻量级的 Google Analytics 替代品。

核心要点：

- **隐私优先**：无 Cookie、无持久标识符，天然符合 GDPR/CCPA/PECR 规范。不收集任何个人数据，因此无需 Cookie 同意横幅。
- **轻量脚本**：跟踪代码片段小于 1 KB——比 GA 的捆绑包小约 75 倍。页面负担更小，加载更快。
- **单页仪表板**：所有关键指标（访客、页面浏览量、来源、热门页面、国家/地区、设备）集中在一个屏幕上，而非 GA 的多层菜单树。
- **可自托管**：核心采用 Apache 2.0 许可证，附带 Docker Compose 配置（社区版）。你可以运行在自己的服务器上并拥有数据。此外还有付费托管的云版本，用于资助开发。

技术栈（与你相关）：
- **后端**：Elixir / Phoenix
- **数据存储**：ClickHouse（列式 OLAP——可快速处理事件聚合查询），PostgreSQL 用于应用元数据
- **前端**：React + Tailwind

ClickHouse 与 Elixir 的组合是架构上的亮点——事件流式进入 ClickHouse，仪表板针对列式存储运行聚合查询，而非扫描行式表。这就是它在规模下仍保持快速的原因。

对于你的 `lzwjava.github.io` 博客/笔记，通过 Docker Compose 在你的 `192.168.1.36` 工作站（或小型 VPS）上自托管 Plausible，即可获得无 Cookie 的流量统计，免去 GA 的臃肿和隐私负担。脚本只需将你的域名加入白名单即可。

参考：

- [plausible/analytics](https://github.com/plausible/analytics)
- [Plausible docs — self-hosting](https://plausible.io/docs/self-hosting)