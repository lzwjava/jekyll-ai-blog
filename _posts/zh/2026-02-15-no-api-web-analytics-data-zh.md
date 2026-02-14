---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 没有用于 Web 分析数据的 API
translated: true
type: note
---

**Question:** 在这种情况下（对没有添加自定义域名的 GitHub Pages 博客使用 Cloudflare Web Analytics），如何使用 API 获取月访问量？

**Answer:**

Cloudflare **不提供公开 API** 来通过程序化方式从 **Web Analytics** 中检索月度（或任何历史）的 Visit / Pageview / Visitor 数据，特别是当站点是通过 JavaScript beacon（基于 token，未添加 Domain / Zone）设置的时候。

核心原因及现状（截至 2026 年初）：

- **Web Analytics API 访问受限**
  与 Web Analytics 相关的唯一公开 Endpoint 仅用于 **Management**（例如通过 `/accounts/{account_id}/rum/site_info` 下的 RUM / site_info 接口列出/创建/删除站点），而不用于查询 Visits、Pageviews 或 Uniques 等指标。

- **没有针对 Web Analytics 指标的 GraphQL 或 REST Endpoint**
  主要的 **GraphQL Analytics API** (`https://api.cloudflare.com/client/v4/graphql`) 涵盖了 Proxied traffic（通过 Cloudflare 的 HTTP 请求）、Workers、Firewall 事件等，但**不包括**来自独立 Web Analytics beacon tracker 的数据。社区报告和文档均确认了这种分离。

- **无法通过 API 进行月度汇总或长期聚合**
  即使对于 Proxied zones，月度 Unique visitors 也无法直接获取（你需要自行累加多天的监控数据，但 Unique 数据在跨天累加时本身就无法保证准确性 —— Cloudflare 官方在大多数情况下也不通过 API 暴露真实的月度 Uniques）。对于 Web Analytics，目前没有等效的、可通过 API 导出的 Daily / Hourly 细分数据。

### 你可以采取的替代方案

1. **从 Dashboard 手动导出（推荐大多数用户使用）**
   - 进入 **Analytics & Logs** → **Web Analytics** → 选择你的站点（例如 `username.github.io`）
   - 查看 **Visitors** 或 **Page views** 图表
   - 使用日期选择器选择完整的一个月（或自定义范围）
   - Cloudflare 会显示所选期间的总数（例如顶部的 "Total visitors: X"，或累加图表数值）
   - 点击图表右上角的按钮将数据导出为 CSV —— 这是无需编写代码获取月度数据的最简单方法。

2. **如果你需要自动化 / 程序化访问**
   - 将你的博客切换到 **Cloudflare Pages**（免费，2 分钟内即可从 GitHub Repo 导入）→ 在其中启用内置的 Web Analytics → 虽然仍基于 JS，但 Cloudflare 会自动处理注入。
     遗憾的是，即使是 Cloudflare Pages 的 Web Analytics 指标也**未通过公开 API 暴露**（存在相同的限制）。
   - 使用支持 API 的第三方 Analytics 工具（例如 Plausible, Fathom, Umami, PostHog，甚至自托管的 Matomo） —— 它们大多提供用于月度汇总的 REST / GraphQL API。
   - 对于极特殊的自定义需求，部分用户会尝试爬取 Dashboard（不推荐，违反服务条款且不稳定），或使用浏览器自动化工具。

简而言之：对于纯粹的 Web Analytics（非代理、像你这样基于 Token 的设置），**月访问量只能在 Dashboard 查看** —— 目前不存在可以程序化获取这些数据的 API Endpoint。

**References:**

- [Cloudflare Web Analytics docs - About](https://developers.cloudflare.com/web-analytics/about)
- [GraphQL Analytics API docs](https://developers.cloudflare.com/analytics/graphql-api)
- [Cloudflare Community - API for Web Analytics](https://community.cloudflare.com/t/api-for-web-analytics/644351)
- [Cloudflare API - RUM / Site Info endpoints](https://developers.cloudflare.com/api/resources/rum/subresources/site_info/methods/list) (Management only, no metrics)