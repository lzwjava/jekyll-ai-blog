---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cloudflare 控制面板中的区域 ID 位置
translated: true
type: note
---

Question: 为什么我在 Cloudflare 的 Analytics & Logs > Web Analytics 中找不到 Zone ID？

Answer: 

**Zone ID** **不**在 **Analytics & Logs** 区域（包括 Web Analytics）。该区域显示的是流量统计、性能指标、安全事件和日志，并不显示 Account ID 或 Zone ID 等标识符。

Zone ID 是特定域名（Zone）的唯一标识符，位于 Dashboard 的不同部分。

### 查找 Zone ID 的正确步骤（截至 2026 年，参考 Cloudflare 官方文档）

1. 登录您的 Cloudflare Dashboard：[https://dash.cloudflare.com](https://dash.cloudflare.com)。
2. 如果您有多个 Account，请确保选择了正确的账户（您会看到列出的账户；点击进入相关账户）。
3. 从您的网站/域名列表中选择您需要 Zone ID 的特定 **domain** (zone)。  
   → 这将带您进入该域名的 **Overview** 页面。
4. 在 **Overview** 页面，向下滚动（通常位于右侧边栏底部或主要内容区域的底部）。
5. 寻找 **API** 区域（它通常位于底部附近）。
6. 在 **API** 区域，您会看到：
   - **Zone ID**：一个 32 位的十六进制字符串（例如：`023e105f4ecef8ad9ca31a8372d0c353`）。
   - **Account ID**：也列在附近。
7. 点击 Zone ID 旁的 **Click to copy** 即可将其复制到剪贴板。

**重要提示：**
- 您必须处于特定域名的 **Overview** 页面（而不是 Account 级别的首页，也不是 Analytics，也不是单纯的 Workers & Pages 页面）。
- 如果您在 Workers & Pages 的概览页面（未选择特定域名），您可能只能看到 **Account ID** —— 这就是为什么有些用户找不到 Zone ID。
- Zone ID 仅存在于您已添加到 Cloudflare 的域名中。如果没有添加任何域名，则不会有 Zone ID。
- 该位置多年来一直保持一致（域名 Overview 的右侧栏/API 区域），根据最新文档（最后更新于 2025 年 9 月），没有重大变化。

如果您仍然找不到：
- 再次检查您是否处于该域名的 **Overview** 标签页（而不是 Analytics & Logs）。
- 尝试刷新页面或切换域名。
- 使用 API 方法作为备选（需要 API token）：
  ```bash
  curl -X GET "https://api.cloudflare.com/client/v4/zones" \
       -H "Authorization: Bearer YOUR_API_TOKEN" \
       -H "Content-Type: application/json"
  ```
  在每个 zone 对象中查找 `id` 字段。

References:  

- [Find account and zone IDs · Cloudflare Fundamentals docs](https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids)
- [Cloudflare Community threads confirming location on Overview > API section](https://community.cloudflare.com/t/where-to-find-zone-id/132913)
- [Zone Analytics docs (confirming Analytics section is for metrics, not IDs)](https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics)