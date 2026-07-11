---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么GoatCounter显示的访问量少得多
translated: true
type: note
---

**问题：** Cloudflare Web Analytics 显示我的博客（lzwjava.github.io）过去 30 天约有 6 万次访问，但 GoatCounter 仅显示约 4000 次。GoatCounter 出了什么问题？代理/机器人流量现在是否真的占这种差异的很大一部分？

**回答：**

你遇到的 15 倍差距几乎可以肯定是 **方法不匹配，而不是 GoatCounter 的 bug**。你比较的是两个根本不同的测量层面。

## 核心问题：你实际看的是 Cloudflare 哪个产品？

Cloudflare 提供两种人们称为“分析”的产品，它们测量的内容完全不同：

| 产品 | 位置 | 机制 | 是否统计机器人？ |
| --- | --- | --- | --- |
| **Web Analytics**（又名 Browser Insights） | Speed 选项卡 / 专用 Web Analytics 部分 | JS 信标，客户端，无 Cookie | 大部分不统计（不执行 JS 的机器人不可见），但 **并未完全过滤** 执行 JS 的机器人——Cloudflare 将其归类为 `Unknown` 浏览器，并且默认情况下通常不会排除它们。Cloudflare Web Analytics 在其网站统计数据中不排除机器人流量；机器人被归类为 'Unknown' 浏览器类型，并在 Cloudflare 的网站统计数据中占显著比例。 |
| **Analytics & Logs**（DNS 附近的“Traffic”/概况选项卡，区域级别） | 仪表板概况 | 服务器端，基于边缘/代理日志——每个到达 Cloudflare 边缘的 HTTP 请求 | **是的，全部统计**——机器人、爬虫、监控 ping、curl、抓取器 |

这是一个非常常见的混淆点，Cloudflare 自己的社区论坛就有确切的答案：Cloudflare 报告你网站的所有访问，包括机器人、爬虫和有隐私措施的用户。而 Google Analytics 只统计执行其 JavaScript 的访问者。GoatCounter 的行为类似于 Google Analytics 那一端——它也是一个 JS 信标，因此在结构上无法看到不执行 JS 的机器人。

如果你的 6 万这个数字来自区域级别的 **Analytics & Logs / Traffic** 概况（而不是专用的 Web Analytics 小部件），那么这个数字包括每一个通过 Cloudflare 代理访问 `lzwjava.github.io` 的爬虫、AI 抓取器、在线监控器和 RSS 阅读器。这不是“6 万读者”——而是“Cloudflare 边缘记录的 6 万次 HTTP 请求”。与 GoatCounter 完全不可比。

**行动项 #1：** 去检查你当时看的是哪个具体面板。如果是仪表板的“Traffic”概况，那么这个差异就已经解释清楚了——无需再添加第三方分析平台来“解决”它，因为你一开始就没有进行同类比较。

## 是的，代理/机器人流量确实已经爆炸性增长——这并非妄想

你的直觉是正确的，而且这已经不是一个微小的影响了：Cloudflare 的 Radar 仪表板显示，截至 2026 年 6 月，机器人占所有 HTML 内容 HTTP 请求的 57.5%，人类占 42.5%——Cloudflare 首席执行官 Matthew Prince 发布消息称，自动化机器人流量已经跨过了行业内没人预料到会这么快达到的阈值：互联网历史上首次，机器生成的网络流量超过了人类。而且不仅仅是老式的抓取——代理型 AI、代表用户行为（而非为训练数据抓取）的机器人，在去年年初仅占自动化流量的 1.7%，到 2025 年底，这一类别增长了 8000%。Cloudflare 一直在积极利用这一转变：2025 年推出了 Pay Per Crawl，允许发布商向 AI 抓取器收取内容访问费用，应网站所有者的要求屏蔽了超过 4160 亿次 AI 机器人请求，并推出了专门为机器消费设计的 Markdown-for-Agents 格式。你的博客约有 8000 条笔记和 400 篇文章——这正是 GPTBot/ClaudeBot/PerplexityBot/Bytespider 为训练/RAG 而大量抓取的那种长尾技术内容。

## GoatCounter 自身的盲点（为什么 4000 可能也低估了真实人类用户）

不要认为 4000 就是真实数据：

- GoatCounter 的脚本域名（`gc.zgo.at` 或你的自定义计数域名）出现在一些广告拦截器/隐私列表过滤集中，因此相当一部分注重隐私的读者（正是那些会阅读自托管的、开源风格博客的人群）会静默地不触发信标。
- 如果你自托管 GoatCounter 并且在信标触发时它变慢或不可达（例如冷虚拟机、DNS 故障），页面浏览就会静默地不被记录——不会向你显示任何错误。
- JS 信标工具会遗漏所有通过 RSS 阅读器、`curl`、`wget` 或越来越多的 **代表人类获取 markdown 的代理**（正是 Cloudflare 刚刚构建的 `Markdown-for-Agents` 模式）阅读的人——这些流量是真实的读者意图，但对 GoatCounter 和 Cloudflare Web Analytics 都不可见。

## 不要添加第三个分析平台——使用 Cloudflare 自身的机器人分类作为交叉参考

既然你已经使用了 Cloudflare 代理，你真正需要的“第三方数据源”不是 Plausible/Umami/Fathom，而是 Cloudflare 自身的 **机器人评分**（对完全相同的请求流），通过 GraphQL Analytics API（适用于免费版/专业版区域，不仅限于企业版）：

```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/graphql" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
  "query": "query {
    viewer {
      zones(filter: { zoneTag: \"<ZONE_ID>\" }) {
        httpRequestsAdaptiveGroups(
          limit: 10000,
          filter: { datetime_geq: \"2026-06-11T00:00:00Z\", datetime_leq: \"2026-07-11T00:00:00Z\" }
        ) {
          count
          dimensions { botScore }
        }
      }
    }
  }"
}'
```

将返回的 `botScore`（0–99，越低越像机器人）分类为人类（>30）和自动化（<=30），并按类别对 `count` 求和。将 **那个仅人类的小计** 与 GoatCounter 的 4000 进行比较。如果它们落在同一数量级，那么你就确认了 GoatCounter 大致正确，而 6 万主要是来自错误 Cloudflare 面板的机器人噪音。如果 GraphQL 的人类类别仍然远高于 GoatCounter，那么你就有一个真正的信标触发/广告拦截问题值得修复（例如，切换到第一方代理路径如 `/api/count`，而不是使用第三方 JS 域名，这也能避开大多数广告拦截列表）。

这比添加 Plausible/Fathom/Umami 作为第四个信标更有用——你只是增加了另一个与 GoatCounter 具有完全相同 JS 执行盲点的工具，而不是在你已有的请求流上真正分离人类和机器人。

**参考资料：**

- [Types of analytics · Cloudflare Analytics docs](https://developers.cloudflare.com/analytics/types-of-analytics/)
- [Cloudflare Bot Analytics · Cloudflare bot solutions docs](https://developers.cloudflare.com/bots/bot-analytics/)
- [Cloudflare Analytics vs Web Analytics — Cloudflare Community discussion](https://community.cloudflare.com/t/traffic-report/561155)
- [Simple Analytics: why Cloudflare Web Analytics doesn't exclude bots](https://www.simpleanalytics.com/blog/why-simple-analytics-is-a-great-alternative-to-cloudflare-web-analytics)
- [Bots Now Outnumber Humans Online — Forbes, June 2026](https://www.forbes.com/sites/josipamajic/2026/06/04/bots-now-outnumber-humans-online-and-the-internet-was-never-built-for-this/)