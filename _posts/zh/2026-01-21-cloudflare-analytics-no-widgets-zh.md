---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 无需小组件即可显示 Cloudflare 分析数据
translated: true
type: note
---

**Question: 如何在我的博客上显示 Cloudflare Web Analytics 数据（如过去 30 天的访问量和页面浏览量）？**

**Answer:**

Cloudflare Web Analytics（注重隐私保护、基于 JS 的产品）目前**不**提供任何官方的可嵌入小组件、徽章、图表或公共分享选项，来直接在你的博客/网站上显示统计数据（如过去 30 天的总访问量或页面浏览量）。

Cloudflare 的 dashboard 仅向账户所有者显示这些数据，并没有像某些其他 analytics 服务那样提供内置的面向公众的徽章或嵌入代码。

以下是人们常用的几种可行方案：

1. **手动更新（最简单，无需编程）**
   每月（或每周）查看一次你的 Cloudflare dashboard → Web Analytics → Overview，记录过去 30 天显示的 "Visits" 和 "Page views" 数值，并手动将其写在博客的页脚、侧边栏或关于页面中，例如：

   ```
   过去 30 天：≈ 12,400 visits • 38,700 page views (via Cloudflare Web Analytics)
   ```

   许多小型/个人博客正是这样做的。

2. **使用 Cloudflare GraphQL Analytics API（最准确，但需要编程）**
   Cloudflare 提供了一个 GraphQL API，可以返回 zone/domain 的 HTTP 级别指标（page views, visits）。
   - 你需要创建一个具有 "Analytics: Read" 权限的 **API token**。
   - 使用诸如 `httpRequests1dGroups` 或 `httpRequestsAdaptiveGroups` 之类的查询来获取过去 30 天的聚合数据。
   - 定期运行此查询（cron job, GitHub Actions, Cloudflare Worker） → 存储结果 → 在博客上显示（静态文件、shortcode 等）。

   大致的 GraphQL 查询结构示例（你需要调整日期和 zoneTag）：

   ```graphql
   query {
     viewer {
       zones(filter: {zoneTag: "YOUR_ZONE_ID"}) {
         httpRequests1dGroups(
           filter: {date_geq: "2025-12-23", date_lt: "2026-01-22"}
           limit: 31
         ) {
           sum { pageViews visits requests }
           dimensions { date }
         }
       }
     }
   }
   ```

   你可以对该期间内的 `pageViews` 和唯一近似访问量进行求和。许多人通过这种方式构建小型仪表板或简易计数器。

3. **Cloudflare Workers + KV / D1 (自定义计数器/徽章)**
   如果你想要一个实时的“本月浏览量”徽章：
   - 使用 Worker 来统计页面浏览量（通过 fetch 事件）。
   - 将总数存储在 KV 或 D1 中。
   - 提供一个类似于 shields.io / badgen 风格的 SVG 徽章。
   这不是直接使用 Web Analytics 数据，而是重新创建一个相似的指标。

4. **如果你需要易于嵌入的第三方替代方案**
   如果公开的徽章/小组件对你很重要，可以考虑切换到（或增加）原生提供此类功能的工具：
   - Plausible Analytics（具有可共享的仪表板 + 简单嵌入）
   - Umami（自托管，具有公共分享功能）
   - Fathom Lite
   - GoatCounter
   - 具有导出功能的简单 analytics → Hugo/Jekyll shortcode

**快速总结 – 静态博客用户的常见做法**
→ 每隔一两个月手动粘贴一次数值（在独立博客中非常普遍）。
→ 如果你想实现自动化 → 使用 GraphQL API + 你的 SSG 数据文件 / API 路由编写一个小脚本。

**References:**

- https://developers.cloudflare.com/web-analytics/
- https://developers.cloudflare.com/analytics/graphql-api/
- https://community.cloudflare.com/t/api-for-web-analytics/644351
- https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics
