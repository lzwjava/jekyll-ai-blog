---
audio: false
generated: true
lang: zh
layout: post
title: 专注隐私的网站分析指南
translated: true
type: note
---

Cloudflare Web Analytics 是一款注重隐私的免费工具，旨在帮助网站所有者追踪和理解网站性能及访客行为，同时不损害用户隐私。以下是根据最新可用信息整理的 Cloudflare Web Analytics 设置和使用全面指南。

### Cloudflare Web Analytics 概述

Cloudflare Web Analytics 提供网站流量、页面浏览量和性能指标的洞察，同时优先考虑用户隐私。与可能追踪个人数据或使用 Cookie 的传统分析工具不同，Cloudflare 的解决方案避免使用侵入式追踪方法，如指纹识别、Cookie 或本地存储用于分析目的。它适用于各种规模的网站，并且可以在使用或不使用 Cloudflare 代理服务的情况下使用。[](https://www.cloudflare.com/web-analytics/)[](https://www.cloudflare.com/en-in/web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)

### 主要特性

- **隐私优先**：不收集个人数据、不使用 Cookie 或通过 IP 地址或用户代理追踪用户，确保符合 GDPR 等隐私法规。[](https://www.cloudflare.com/en-in/web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)
- **两种数据收集方法**：
  - **JavaScript Beacon**：一个轻量级的 JavaScript 代码片段，使用浏览器的 Performance API 收集客户端指标。非常适合详细的真实用户监控（RUM）数据，如页面加载时间和核心网页指标。[](https://www.cloudflare.com/web-analytics/)[](https://developers.cloudflare.com/web-analytics/about/)
  - **边缘分析**：从 Cloudflare 的边缘服务器收集经过 Cloudflare 代理的网站的服务器端数据。无需更改代码，并且能捕获所有请求，包括来自机器人或禁用 JavaScript 的用户的请求。[](https://www.cloudflare.com/web-analytics/)[](https://developers.cloudflare.com/web-analytics/faq/)
- **提供的指标**：追踪页面浏览量、访问次数、热门页面、引荐来源、国家/地区、设备类型、状态码以及性能指标（如页面加载时间）。[](https://www.cloudflare.com/en-in/web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)[](https://usefathom.com/features/vs-cloudflare-web-analytics)
- **自适应比特率（ABR）**：根据数据大小、日期范围和网络条件自动调整数据分辨率，以获得最佳性能。[](https://developers.cloudflare.com/web-analytics/about/)
- **免费使用**：任何拥有 Cloudflare 账户的人都可以使用，即使不更改 DNS 或使用 Cloudflare 代理。[](https://www.cloudflare.com/en-in/web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)
- **仪表盘和过滤器**：提供直观的仪表盘，可按主机名、URL、国家/地区和时间范围查看和筛选数据。您可以放大特定时间段或对数据进行分组以进行更深入的分析。[](https://www.cloudflare.com/web-analytics/)[](https://www.cloudflare.com/en-in/web-analytics/)
- **单页面应用程序（SPA）支持**：通过覆写 History API 的 `pushState` 函数（不支持基于哈希的路由器）自动追踪 SPA 中的路由更改。[](https://scripts.nuxt.com/scripts/analytics/cloudflare-web-analytics)

### 局限性

- **数据保留**：历史数据仅限于 30 天，可能不适合需要长期分析的用户。[](https://plausible.io/vs-cloudflare-web-analytics)
- **数据采样**：指标基于页面加载事件的 10% 样本，与 Plausible 或 Fathom Analytics 等工具相比可能导致不准确。[](https://plausible.io/vs-cloudflare-web-analytics)
- **准确性担忧**：服务器端分析（边缘分析）可能包含机器人流量，与 Google Analytics 等客户端分析相比会夸大数字。客户端分析可能会错过禁用 JavaScript 或使用广告拦截器的用户的数据。[](https://developers.cloudflare.com/analytics/faq/about-analytics/)[](https://plausible.io/vs-cloudflare-web-analytics)[](https://markosaric.com/cloudflare-analytics-review/)
- **不支持 UTM 参数**：目前，查询字符串（如 UTM 参数）不会被记录，以避免收集敏感数据。[](https://developers.cloudflare.com/web-analytics/faq/)
- **导出限制**：没有直接导出数据（例如到 CSV）的方法，这与 Fathom Analytics 等一些竞争对手不同。[](https://usefathom.com/features/vs-cloudflare-web-analytics)
- **基础分析**：与 Google Analytics 相比，缺乏高级功能，如转化跟踪或详细的用户旅程分析。[](https://www.reddit.com/r/webdev/comments/ka8gxv/cloudflares_privacyfirst_web_analytics_is_now/)

### 设置 Cloudflare Web Analytics

#### 先决条件

- 一个 Cloudflare 账户（可在 cloudflare.com 免费创建）。
- 访问您网站的代码（用于 JavaScript beacon）或 DNS 设置（如果使用 Cloudflare 代理，用于边缘分析）。

#### 设置步骤

1. **登录 Cloudflare 仪表盘**：
   - 访问 [cloudflare.com](https://www.cloudflare.com) 并登录或创建账户。
   - 从账户主页，导航至 **Analytics & Logs** > **Web Analytics**。[](https://developers.cloudflare.com/web-analytics/get-started/)

2. **添加站点**：
   - 在 Web Analytics 部分点击 **Add a site**。
   - 输入您网站的主机名（例如 `example.com`）并选择 **Done**。[](https://developers.cloudflare.com/web-analytics/get-started/)

3. **选择数据收集方法**：
   - **JavaScript Beacon（推荐用于非代理站点）**：
     - 从 **Manage site** 部分复制提供的 JavaScript 代码片段。
     - 将其粘贴到您网站的 HTML 中，位于闭合的 `</body>` 标签之前。确保您的网站具有有效的 HTML，以便代码片段正常工作。[](https://developers.cloudflare.com/web-analytics/get-started/)[](https://developers.cloudflare.com/web-analytics/faq/)
     - 对于单页面应用程序，确保在配置中设置 `spa: true` 以启用自动路由追踪（不支持基于哈希的路由器）。[](https://scripts.nuxt.com/scripts/analytics/cloudflare-web-analytics)
     - Nuxt 应用示例：使用 `useScriptCloudflareWebAnalytics` 组合式函数或将令牌添加到 Nuxt 配置中以实现全局加载。[](https://scripts.nuxt.com/scripts/analytics/cloudflare-web-analytics)
   - **边缘分析（用于代理站点）**：
     - 通过将您的 DNS 设置更新为指向 Cloudflare 的域名服务器，将您的网站代理通过 Cloudflare。这可以在几分钟内完成，无需更改代码。[](https://www.cloudflare.com/en-in/web-analytics/)
     - 指标将出现在 Cloudflare 仪表盘的 **Analytics & Logs** 下。[](https://developers.cloudflare.com/web-analytics/faq/)
   - **Cloudflare Pages**：
     - 对于 Pages 项目，一键启用 Web Analytics：从 **Workers & Pages** 中选择您的项目，转到 **Metrics**，然后在 Web Analytics 下点击 **Enable**。[](https://developers.cloudflare.com/pages/how-to/web-analytics/)[](https://developers.cloudflare.com/web-analytics/get-started/)

4. **验证设置**：
   - 数据可能需要几分钟才会出现在仪表盘中。检查 **Web Analytics Sites** 部分以确认站点已添加。[](https://developers.cloudflare.com/web-analytics/get-started/)
   - 如果使用边缘分析，请确保 DNS 传播完成（可能需要 24-72 小时）。[](https://developers.cloudflare.com/analytics/faq/about-analytics/)

5. **配置规则（可选）**：
   - 设置规则以追踪特定网站或路径。使用维度对指标进行分类（例如，按主机名或 URL）。[](https://developers.cloudflare.com/web-analytics/)

#### 注意事项

- 如果您的网站有 `Cache-Control: public, no-transform` 标头，JavaScript beacon 将不会自动注入，Web Analytics 可能无法工作。调整您的缓存设置或手动添加代码片段。[](https://developers.cloudflare.com/web-analytics/get-started/)[](https://developers.cloudflare.com/web-analytics/faq/)
- 某些广告拦截器可能会阻止 JavaScript beacon，但边缘分析不受影响，因为它们依赖于服务器日志。[](https://developers.cloudflare.com/web-analytics/faq/)
- 对于手动设置，beacon 报告到 `cloudflareinsights.com/cdn-cgi/rum`；对于代理站点，它使用您域名的 `/cdn-cgi/rum` 端点。[](https://developers.cloudflare.com/web-analytics/faq/)

### 使用 Cloudflare Web Analytics

1. **访问仪表盘**：
   - 登录 Cloudflare 仪表盘，选择您的账户和域名，然后转到 **Analytics & Logs** > **Web Analytics**。[](https://developers.cloudflare.com/pages/how-to/web-analytics/)[](https://developers.cloudflare.com/analytics/types-of-analytics/)
   - 查看指标，如页面浏览量、访问次数、热门页面、引荐来源、国家/地区、设备类型和性能数据（例如，页面加载时间、核心网页指标）。[](https://www.cloudflare.com/en-in/web-analytics/)[](https://usefathom.com/features/vs-cloudflare-web-analytics)

2. **筛选和分析数据**：
   - 使用筛选器专注于特定指标（例如，按主机名、URL 或国家/地区）。
   - 放大时间范围以调查流量高峰或按指标（如引荐来源或页面）对数据进行分组。[](https://www.cloudflare.com/en-in/web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)
   - 对于高级用户，通过 **GraphQL Analytics API** 查询数据以创建自定义仪表盘。[](https://www.cloudflare.com/application-services/products/analytics/)[](https://www.cloudflare.com/en-in/application-services/products/analytics/)

3. **理解关键指标**：
   - **页面浏览量**：页面加载的总次数（HTML 内容类型且 HTTP 响应成功）。[](https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics/)
   - **访问次数**：来自不同引荐来源（与主机名不匹配）或直接链接的页面浏览量。[](https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)
   - **独立访客**：基于 IP 地址，但出于隐私原因不存储。由于机器人流量或缺乏基于 JavaScript 的去重，可能比其他工具的数字更高。[](https://developers.cloudflare.com/analytics/faq/about-analytics/)[](https://plausible.io/vs-cloudflare-web-analytics)
   - **性能指标**：包括页面加载时间、首次绘制和核心网页指标（仅限客户端）。[](https://usefathom.com/features/vs-cloudflare-web-analytics)

4. **与其他工具比较**：
   - 与 Google Analytics 不同，Cloudflare 不追踪用户旅程或转化，但包含机器人和威胁流量，这可能会夸大数字（大多数网站的 20-50% 流量）。[](https://developers.cloudflare.com/analytics/faq/about-analytics/)[](https://www.cloudflare.com/insights/)
   - 与 Plausible 或 Fathom Analytics 相比，由于采样和有限的保留期，Cloudflare 的数据不够精细。[](https://plausible.io/vs-cloudflare-web-analytics)[](https://usefathom.com/features/vs-cloudflare-web-analytics)
   - 边缘分析可能显示比 Google Analytics 等客户端工具更高的数字，后者排除了机器人和非 JavaScript 请求。[](https://developers.cloudflare.com/analytics/faq/about-analytics/)[](https://www.reddit.com/r/CloudFlare/comments/1alzkwm/why_are_my_cloudflare_traffic_stats_so_different/)

### 最佳实践

- **选择正确的方法**：如果您的网站被代理，使用 JavaScript beacon 获取注重隐私的客户端指标，或使用边缘分析获取全面的服务器端数据。[](https://www.cloudflare.com/web-analytics/)
- **与其他工具结合使用**：与 Google Analytics 或注重隐私的替代方案（如 Plausible 或 Fathom）配对使用，以获得更深入的洞察，因为 Cloudflare 的分析是基础性的。[](https://www.cloudflare.com/insights/)[](https://www.reddit.com/r/webdev/comments/ka8gxv/cloudflares_privacyfirst_web_analytics_is_now/)
- **监控性能**：使用性能指标识别加载缓慢的页面，并利用 Cloudflare 的建议（例如，缓存优化）。[](https://developers.cloudflare.com/web-analytics/)
- **检查广告拦截器问题**：如果使用 JavaScript beacon，请告知用户允许 `cloudflare.com` 或禁用广告拦截器以确保数据收集。[](https://developers.cloudflare.com/analytics/faq/about-analytics/)
- **定期审查数据**：由于数据仅保留 30 天，请频繁检查仪表盘以发现趋势或异常。[](https://plausible.io/vs-cloudflare-web-analytics)

### 故障排除

- **未显示数据**：
  - 验证 JavaScript 代码片段是否正确放置，并且网站具有有效的 HTML。[](https://developers.cloudflare.com/pages/how-to/web-analytics/)[](https://developers.cloudflare.com/web-analytics/faq/)
  - 对于边缘分析，确保 DNS 指向 Cloudflare（传播可能需要 24-72 小时）。[](https://developers.cloudflare.com/analytics/faq/about-analytics/)
  - 检查 `Cache-Control: no-transform` 标头是否阻止了自动 beacon 注入。[](https://developers.cloudflare.com/web-analytics/get-started/)
- **统计不准确**：
  - 边缘分析包含机器人流量，夸大了数字。使用客户端分析以获得更准确的访客计数。[](https://plausible.io/vs-cloudflare-web-analytics)[](https://markosaric.com/cloudflare-analytics-review/)
  - 数据采样（10%）可能导致差异。在与其他工具比较时请考虑这一点。[](https://plausible.io/vs-cloudflare-web-analytics)
- **广告拦截器问题**：某些浏览器扩展会阻止 JavaScript beacon。边缘分析不受此影响。[](https://developers.cloudflare.com/web-analytics/faq/)
- **缺少 SPA 指标**：确保启用了 SPA 支持（`spa: true`）并避免使用基于哈希的路由器。[](https://scripts.nuxt.com/scripts/analytics/cloudflare-web-analytics)

### 高级用法

- **GraphQL Analytics API**：对于自定义分析，查询 Cloudflare 的 API 以构建量身定制的仪表盘或与其他系统集成。需要技术专长。[](https://www.cloudflare.com/application-services/products/analytics/)[](https://www.cloudflare.com/en-in/application-services/products/analytics/)
- **Cloudflare Workers**：将分析数据发送到时间序列数据库进行自定义处理，或使用 Workers 进行高级无服务器分析。[](https://developers.cloudflare.com/analytics/)
- **安全洞察**：结合 Cloudflare 的安全分析，在访客数据旁边监控威胁和机器人。[](https://www.cloudflare.com/insights/)[](https://developers.cloudflare.com/waf/analytics/security-analytics/)

### 与替代方案的比较

- **Google Analytics**：提供详细的用户旅程追踪和转化，但依赖于可能被阻止的 Cookie 和 JavaScript。Cloudflare 更简单且注重隐私，但功能较少。[](https://developers.cloudflare.com/analytics/faq/about-analytics/)[](https://www.reddit.com/r/webdev/comments/ka8gxv/cloudflares_privacyfirst_web_analytics_is_now/)
- **Plausible Analytics**：开源、隐私优先，具有无限数据保留且无采样。对于独立访客更准确，但需要付费计划。[](https://plausible.io/vs-cloudflare-web-analytics)
- **Fathom Analytics**：与 Plausible 类似，具有可导出数据和高级功能（如活动追踪）。Cloudflare 的免费产品功能较弱，但对于基本需求更容易设置。[](https://usefathom.com/features/vs-cloudflare-web-analytics)
- **Jetpack Stats**：特定于 WordPress，数据保留有限（28 天）且无用户级追踪。类似的隐私焦点，但比 Cloudflare 灵活性差。[](https://wordpress.com/support/stats/)

### 其他资源

- **官方文档**：[Cloudflare Web Analytics 文档](https://developers.cloudflare.com/web-analytics/)[](https://developers.cloudflare.com/web-analytics/about/)
- **设置指南**：[启用 Cloudflare Web Analytics](https://developers.cloudflare.com/web-analytics/get-started/)[](https://developers.cloudflare.com/web-analytics/get-started/)
- **常见问题解答**：[Cloudflare Web Analytics 常见问题解答](https://developers.cloudflare.com/web-analytics/faq/)[](https://developers.cloudflare.com/web-analytics/faq/)
- **博客文章**：[Cloudflare 的隐私优先 Web Analytics](https://blog.cloudflare.com/privacy-first-web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)
- **社区支持**：查看 Cloudflare 的社区论坛以获取额外帮助。[](https://developers.cloudflare.com/web-analytics/faq/)

### 结论

Cloudflare Web Analytics 是寻求免费、注重隐私且设置最少的分析工具的网站所有者的绝佳选择。它非常适合基本的流量和性能监控，但由于数据采样、有限的保留期以及缺乏转化跟踪等功能，可能无法满足高级需求。为了获得更深入的洞察，请考虑将其与 Plausible 或 Fathom Analytics 等工具结合使用。在解释数据时，请务必验证设置的准确性并了解其局限性。

如果您需要有关设置的具体帮助或对将 Cloudflare Web Analytics 与您的网站集成有疑问，请告诉我！
