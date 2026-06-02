---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开放图谱协议详解
translated: true
type: note
---

在HTML元标签（如`<meta property="og:type" content="website">`）的语境中，“og”代表开放图谱协议（Open Graph）。这是由Facebook（现Meta）最初开发的标准协议，允许网页提供结构化元数据，用于控制页面在社交媒体或即时通讯应用中被分享时的展示形式，例如以富预览格式（如图文卡片）显示标题、描述、图片等信息。

该协议使用以“og:”为前缀的属性来定义元素，例如：

- `og:title`：内容标题
- `og:description`：内容摘要
- `og:image`：预览图链接
- `og:type`：内容类型（如网站、文章、视频）

虽然该协议最初为Facebook创建，但包括微信在内的众多平台和应用现已支持开放图谱标签来生成链接预览。当您在微信分享链接时，系统通常会解析这些标签来生成统一的缩略图、标题和描述。若未设置这些标签，平台可能转而抓取其他元标签或页面内容，导致预览效果不可控。

您猜测的“open gx”已接近答案——实际应为“Open Graph”（“open gx”可能是“graph”的输入误差或自动校正）。

### 参考资料

[开放图谱协议官网](https://ogp.me/)
[开放图谱元标签完全指南](https://ahrefs.com/blog/open-graph-meta-tags/)
[开放图谱协议及其应用详解](https://www.freecodecamp.org/news/what-is-open-graph-and-how-can-i-use-it-for-my-website/)
[微信如何选择链接缩略图？](https://stackoverflow.com/questions/44564614/how-does-wechat-choose-the-links-thumbnail)
[微信元标签相关讨论](https://github.com/freeCodeCamp/freeCodeCamp/issues/38707)
