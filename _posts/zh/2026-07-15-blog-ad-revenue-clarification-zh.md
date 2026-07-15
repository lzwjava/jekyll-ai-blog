---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 博客广告收入说明
translated: true
type: note
---

问题：澄清一下——你希望在自己的博客上展示广告来赚取收入，而不是在其他地方投放广告，对吗？

回答：是的——这正是我上一条回复所做的。为了明确每个部分的作用：

- **`ads.txt`** — 这并不是“分享”广告到任何地方。它是 Google 要求 *在你的域名* (`lzwjava.github.io/ads.txt`) 上放置的文件，声明“我，pub-XXXX，授权 Google 在此网站销售广告位。”没有它，Google 根本不会在你的页面上投放广告。这是一个前提条件，而不是独立的广告位。
- **`_layouts/default.html` 中的 `<script>`** — 这是让广告实际出现在你博客页面上的代码。它在每个页面加载 Google 的广告库（因为 `default.html` 是所有页面继承的基础布局）。
- **`post.html` 中的 `<ins class="adsbygoogle">` 代码块** — 这是一个实际的广告位，*在你的博客文章内部* 渲染，位于内容和页脚之间。这是读者在你的网站上看到的广告。

所以完整流程如下：
1. 在 ads.google.com 申请 → 获得 `lzwjava.github.io` 的批准
2. 获取你的 `pub-XXXXXXXXXXXXXXXX` ID
3. 将 `ads.txt` 放在仓库根目录
4. 将脚本标签添加到 `_layouts/default.html` 的 head 中
5. 将 `<ins>` 广告单元添加到 `_layouts/post.html` 中
6. 推送 → GitHub Pages 重新构建 → 广告出现在你的博客文章中

这里没有任何步骤会将你的内容或广告发送到其他网站。AdSense 只是将广告 `<iframe>` 注入到你自己的页面中，Google 根据你的流量按展示/点击付费。

如果你指的是不同的东西——比如嵌入 *你自己的* 产品（趣直播、你的 AI 咨询）的横幅，而不是 Google 的广告网络——那是另一种更简单的构建（只需一个静态的 `<div>` 加上你自己的 CTA，无需 AdSense 批准，Google 不抽成）。你实际想要的是哪一种？