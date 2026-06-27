---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cloudflare 控制面板重新设计详情
translated: true
type: note
---

问题：Cloudflare 最近是否更新了新的用户界面/仪表板？

让我核实一下，而不是猜测。是的。Cloudflare 推出了重大仪表板重新设计——这是自 2010 年以来最大规模的视觉改版。

核心变化：他们取消了“我的网站”页面。取而代之的是，登录后界面左上角会出现一个下拉菜单，供你选择网站。这一改变的动机是规模问题——旧界面在用户管理数百或数千个域名时会出现故障，迫使他们通过 API 管理账户。Matthew Prince 表示，需要一个能够适应 Cloudflare 如今所有新功能以及未来计划功能的界面。

除了整体外壳重新设计外，多个子仪表板也分批进行了重构：

- AI 被提升为侧边栏顶级区域（2026 年 2 月 19 日）——AI 现在在 Cloudflare 仪表板侧边栏中拥有自己的顶级区域，因此无需在菜单中翻找即可找到 AI 功能，同时还进行了导航、新用户引导和无障碍修复。
- Workers KV（2026 年 1 月 20 日）——更新后的仪表板 UI 采用新样式，为命名空间和键操作提供简化首页，与仪表板其他 UI 更新保持一致，并改进了分析视图。
- 安全概览仪表板（约 2026 年 5 月）引入了安全操作项，按严重程度（严重、中等、低优先级）显示漏洞和错误配置。
- Turnstile/验证页面也于 2026 年 2 月重新设计，采用统一且符合 WCAG 2.2 AAA 标准的 UI。

因此，这并非一次性切换——而是一次协调的设计系统迁移，主仪表板外壳已更改，各个产品也在逐步调整以匹配新的设计。

参考文献：

- [CloudFlare 的新仪表板](https://blog.cloudflare.com/cloudflares-new-control-panel/)
- [重新设计 Cloudflare](https://blog.cloudflare.com/redesigning-cloudflare/)
- [AI 仪表板体验改进](https://developers.cloudflare.com/changelog/post/2026-02-19-ai-dashboard-experience-improvements/)
- [新的 Workers KV 仪表板 UI](https://developers.cloudflare.com/changelog/post/2026-01-20-kv-dash-ui-homepage/)
- [Cloudflare 安全概览仪表板 (InfoQ)](https://www.infoq.com/news/2026/05/cloudflare-security-overview-dashboard/)
