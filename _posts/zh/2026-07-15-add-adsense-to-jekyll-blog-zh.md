---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Jekyll博客中添加AdSense
translated: true
type: note
---

问题：如何将 Google AdSense 添加到我的 Jekyll 博客（lzwjava/jekyll-ai-blog）中以实现盈利？

答案：

你的站点是托管在 GitHub Pages 上的静态 Jekyll 站点，因此 AdSense 集成只需一个脚本标签和 `ads.txt` 文件，无需 SDK 或服务器。以下是根据你仓库实际结构的具体差异。

**1. 首先申请 AdSense**——广告展示前需要审核通过。前往 ads.google.com，添加 `lzwjava.github.io` 作为站点，等待审核（可能需要数天到数周）。你将获得一个发布商 ID，格式如 `pub-1234567890123456`。

**2. 在仓库根目录添加 `ads.txt`**（Google 要求，否则你会因“未经授权的卖家”警告而损失收入）：

```bash
cat > /path/to/repo/ads.txt << 'EOF'
google.com, pub-<占位符_发布商_ID>, DIRECT, f08c47fec0942fa0
EOF
```

**3. 将自动广告脚本添加到 `<head>`** 中，位于 `_layouts/default.html`——在现有的 GoatCounter 脚本之后、`</head>` 之前插入：

```diff
   <script data-goatcounter="https://lzwjava.goatcounter.com/count"
         async src="//gc.zgo.at/count.js"></script>
+
+  <!-- Google AdSense -->
+  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-<占位符_发布商_ID>"
+     crossorigin="anonymous"></script>
 </head>
```

仅此即可启用自动广告（由 Google 决定展示位置）。若希望更灵活控制并提升收入，可添加手动内文广告单元。

**4. 手动内文广告单元**——在 `_layouts/post.html` 中，于 `{{ content }}` 之后、结束 `</hr>` 之前插入一个广告单元（位于文章内容边界，点击率较高的位置）：

{% raw %}

```diff
   {{ content }}

+  <div class="ad-container" style="margin: 24px 0; text-align:center;">
+    <ins class="adsbygoogle"
+         style="display:block"
+         data-ad-client="ca-pub-<占位符_发布商_ID>"
+         data-ad-slot="<占位符_广告位_ID>"
+         data-ad-format="fluid"
+         data-ad-layout-key="-gw-3+1f-3d+2z"></ins>
+    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
+  </div>
+
   <hr>
```

{% endraw %}

从 AdSense 控制台获取 `data-ad-slot`：广告 → 按广告单元 → 内文广告 → 创建一个。

**5. 部署**——你现有的 GitHub Actions 工作流（`gh-pages.yml`）已处理构建和部署，无需修改。只需提交并推送即可。

**针对你设置的具体说明：**

- `_config.yml` 中的 `google_analytics: "UA-66656236-1"` 是 Universal Analytics——该服务已于 2023 年停止运行，目前无效。建议替换为 GA4 或直接移除，因为 GoatCounter 已能提供真实分析数据。
- 由于你的博客是双语（`-en`/`-zh`）且由 AI 翻译，请注意 AdSense 关于“自动生成内容”的政策——如果页面前元数据中标记了 `page.generated: true` 和 `page.translated: true`，且未编辑的 AI 输出过多，可能在人工审核中被标记。这并非硬性障碍，但值得了解。
- 以当前流量（仓库 2 星/1 关注者并非流量信号，但若你的 `notes` 页面——共 1992 个——获得真实搜索流量，这些长尾内容恰恰是 AdSense 的主要收入来源，因为它们属于被索引的细分技术内容）。

鉴于你的人工智能代理背景，另一个值得考虑的方案是：完全放弃展示广告，通过赞助商/联盟营销块（例如你构建的工具——`ww`、`iclaw`、`zz`——或 GPU/咨询行动号召）来实现盈利，因为你的流量画像（阅读技术笔记的工程师）转化为咨询线索的效果远优于展示广告的 0.50 美元 CPM。

参考链接：

- [Google AdSense - 入门指南](https://support.google.com/adsense/answer/9711326)
- [ads.txt 指南](https://support.google.com/adsense/answer/7532444)
- [自动广告文档](https://support.google.com/adsense/answer/9261307)
