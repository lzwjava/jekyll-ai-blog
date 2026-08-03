---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何重定向GitHub Pages用户站点
translated: true
type: note
---

问题：如何将 GitHub Pages 用户站点 `lzwjava.github.io` 重定向到 `lzwjava.com`。

答案：GitHub Pages 仅提供静态文件托管——没有服务器配置，因此无法发出真正的 HTTP 301/302 状态码。这里所谓的“重定向”是通过 HTML meta-refresh 配合 JS fallback 实现的，浏览器在功能上视其为重定向（几乎瞬间完成，不显示可见内容），但爬虫将其视为客户端重定向，而非真正的 3xx。如果你需要真正的 301 重定向，必须在 GitHub Pages 前使用 Cloudflare（Workers/Page Rules）进行代理。

由于 `lzwjava.github.io` 是你的特殊 GitHub *用户*页面仓库，可以直接在该仓库中操作：

```bash
git clone git@github.com:lzwjava/lzwjava.github.io.git
cd lzwjava.github.io
```

```html
<!-- index.html -->
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>正在重定向…</title>
  <link rel="canonical" href="https://lzwjava.com/">
  <meta http-equiv="refresh" content="0; url=https://lzwjava.com/">
  <script>location.replace("https://lzwjava.com/");</script>
</head>
<body>
  <p>已迁移至 <a href="https://lzwjava.com/">lzwjava.com</a></p>
</body>
</html>
```

```bash
rm -f CNAME   # 确保没有旧的 custom domain 文件与重定向页面冲突
git add -A
git commit -m "重定向 lzwjava.github.io -> lzwjava.com"
git push
```

注意事项：

- 如果你的仓库当前存在指向自定义域名的 `CNAME` 文件，请删除它——否则 GitHub Pages 会尝试在该域名下提供服务，而非 `lzwjava.github.io`。
- 如果 SEO 对你很重要（你不希望 Google 将其视为重复/权威混淆），上述 `rel="canonical"` 标签会告知爬虫真实 URL 为 `lzwjava.com`，这是针对基于 JS 重定向的标准缓解措施。
- 如果你的站点是 Jekyll 项目，并且需要实现页面级重定向（不仅仅是根路径），可以使用 `jekyll-redirect-from` 插件——但仅针对根路径到根路径的单个迁移，上述静态 `index.html` 更简单，且符合你通过 `zz`/`ww` CLI 式极简风格的做法。
- 真正的 301 替代方案：将 `lzwjava.github.io` 指向 Cloudflare Worker 路由而非 GitHub Pages，并返回 `Response.redirect(url, 301)`——但这要求你拥有 github.io 子域名的 DNS 控制权，而你没有（GitHub 拥有），因此该方案仅在你重定向的*来源*是一个你控制的域名时有效，而非 `.github.io` 子域名本身。

参考文档：
- [GitHub Pages 的重定向](https://docs.github.com/en/pages/getting-started-with-github-pages/setting-up-a-custom-domain-for-your-github-pages-site)
- [jekyll-redirect-from 插件](https://github.com/jekyll/jekyll-redirect-from)