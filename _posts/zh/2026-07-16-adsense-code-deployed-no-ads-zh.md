---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AdSense代码已部署，无广告显示
translated: true
type: note
---

整体情况如下：

**代码已正确部署** ✅
- `ads.txt` 位于 `https://lzwjava.github.io/ads.txt` — 返回正确内容（200）
- `<meta name="google-adsense-account">` — 已存在于页面中
- `<script src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js">` — 已存在于页面中

**为什么没有显示广告：**

1. **AdSense 账户需要先通过审核** — 仅添加代码并不能让广告显示。你需要将网站提交到 Google AdSense 进行审核，地址为 `https://adsense.google.com`。审核过程可能需要 **1-2 周**。
2. **审核通过后，启用自动广告** — 进入 AdSense 控制台 → 自动广告 → 为你的网站开启。放在 `<head>` 中的脚本本身支持自动广告，但必须在后台面板中激活。
3. **没有手动广告单元** — 我们添加的是自动广告脚本。如果你想在特定位置展示广告（例如每篇博客文章之后），你需要在控制台中创建广告单元，并将其代码放置在页面的 `<body>` 中。

**AdSense Management API 确实存在：**
- 端点：`https://adsense.googleapis.com`（v2）
- 可查询的内容：账户、广告客户、广告单元、收益报告、付款、政策问题、站点状态
- 需要 OAuth2 凭据 — 需在 Google Cloud Console 中设置
- 用于查询站点状态的 API 方法：`GET /v2/{parent=accounts/*}/sites` — 列出已批准/已拒绝的站点

需要我检查 AdSense 控制台状态，或在 `<body>` 中设置一个手动广告单元吗？