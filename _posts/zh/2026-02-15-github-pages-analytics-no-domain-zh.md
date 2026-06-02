---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 无域名的 GitHub 1Pages 分析统计
translated: true
type: note
---

**Question:** 如果我没有添加域名，只是在托管于 GitHub Pages（使用 GitHub 域名）的博客上使用 Web Analytics / logs 会怎样？

**Answer:**

你**可以**在托管于 GitHub Pages 的博客上使用 **Cloudflare Web Analytics**（无论使用的是默认的 `username.github.io` 还是项目子域名如 `username.github.io/repo`），而**无需向 Cloudflare 添加任何域名**，也**无需更改你的 DNS 或 nameservers**。

Cloudflare Web Analytics 专为这种场景设计：它是一个**隐私优先、轻量级的基于 JavaScript 的 tracker**，完全独立于 Cloudflare 的 proxy、DNS 或域名设置运行。它**不需要** Zone ID（因为你的账户中没有添加任何 zone/domain），它通过一个微小的 beacon script 在客户端收集数据。

### 如何为你的 GitHub Pages 博客进行设置

1. 登录你的 Cloudflare dashboard（免费账户即可）。
2. 前往 **Analytics & Logs** → **Web Analytics**（或在控制面板中直接搜索 "Web Analytics"）。
3. 点击 **Add a site**（或 "Create" / "Add site"）。
4. 准确输入访客看到的 GitHub Pages hostname：
   - 用户/组织站点：`username.github.io`
   - 项目站点：`username.github.io/repo-name`
5. Cloudflare 将生成一小段 JavaScript snippet（通常约 1 KB），看起来像这样：
   ```html
   <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "YOUR_UNIQUE_TOKEN_HERE"}'></script>
   ```
6. 将此 snippet 添加到你网站 HTML 文件的 `<head>` 部分（如果你使用静态网站生成器，则添加到 Jekyll/Hugo 等的 layout template 中）。
   - 对于纯 HTML：编辑 `index.html` 和其他页面。
   - 对于 Jekyll：将其添加到 `_includes/head.html` 或等效文件中。
   - Push 更改 → GitHub Pages 将自动重新构建并 deploy。
7. 在经过几小时/几天的流量积累后，在 dashboard 的同一个 Web Analytics 部分查看你的统计数据。

### 关键点与限制

- **无需 Zone ID** — 你在这里永远不会看到或使用 Zone ID，因为你没有添加 zone/domain。
- **无 proxy / performance 功能** — 你无法获得 Cloudflare 的 caching、DDoS protection、image optimization 等功能（这些功能需要 proxy 流量，这意味着必须使用 Cloudflare DNS 并添加域名）。
- **数据隐私友好** — 无 cookies，不存储个人 IP，符合 GDPR。
- **适用于任何 hostname** — 包括 `*.github.io`、未指向 Cloudflare 的自定义域名、开发期间的 localhost 等。
- **Pages 项目的替代方案** — 如果你以后将博客从 GitHub Pages 迁移到 **Cloudflare Pages**（强烈推荐，因为速度更快、有免费的 analytics 集成和自定义域名），你可以在项目设置中**一键开启** Web Analytics（Metrics → Enable），Cloudflare 会在 deploy 时自动注入 snippet，无需手动编辑代码。

这是人们在不触动 DNS 的情况下，为纯 GitHub Pages 站点添加免费且优质的 analytics 最简单、最常用的方法。

**References:**

- [Enabling Cloudflare Web Analytics - Get started](https://developers.cloudflare.com/web-analytics/get-started)
- [Enable Web Analytics for Pages projects](https://developers.cloudflare.com/pages/how-to/web-analytics)
- [FAQs - Cloudflare Web Analytics](https://developers.cloudflare.com/web-analytics/faq)
- [Cloudflare Web Analytics for sites not proxied through Cloudflare](https://developers.cloudflare.com/web-analytics/get-started/#sites-not-proxied-through-cloudflare)
