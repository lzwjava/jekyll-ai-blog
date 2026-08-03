---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Jekyll 重定向插件内部机制
translated: true
type: note
---

问题：`jekyll-redirect-from` 插件内部是如何工作的？

答案：它是一个构建时的 Jekyll 生成器——不需要服务器/运行时，因为 Pages 是静态托管。在 `jekyll build` 时，它接入生成器管道，读取每个页面的 `redirect_from`/`redirect_to` 前置元数据，并为列出的每个旧路径生成一个小的静态 HTML 文件，其中包含 meta-refresh + JS 重定向到真实页面。这与之前我给你的手动 `index.html` 原理相同——该插件只是自动为每个旧 URL 生成一个这样的文件，而不需要你手动编写每一个。

机制：

```yaml
---
title: 我的文章
redirect_from:
  - /old-url/
  - /2019/01/01/old-post.html
---
```

构建时这会生成（大致）：

```
_site/old-url/index.html
_site/2019/01/01/old-post.html
```

每个生成的文件看起来像：

```html
<!doctype html>
<html>
<head>
  <link rel="canonical" href="https://lzwjava.com/my-post/">
  <meta http-equiv="refresh" content="0; url=https://lzwjava.com/my-post/">
</head>
<body>
  <p>此页面已移动。 <a href="https://lzwjava.com/my-post/">点击这里</a>。</p>
</body>
</html>
```

反向方向也存在——页面上的 `redirect_to` 会使该页面本身重定向到外部 URL，适用于你的 github.io → lzwjava.com 场景，如果你希望按页面粒度而不是单一根重定向：

```yaml
---
redirect_to: https://lzwjava.com/some-post/
---
```

安装：

```bash
# Gemfile
gem "jekyll-redirect-from"
```

```yaml
# _config.yml
plugins:
  - jekyll-redirect-from
```

```bash
bundle install
bundle exec jekyll build
```

针对你的设置的注意事项：

- 由于它在构建时运行并仅生成静态文件，它在 GitHub Pages 的白名单插件构建中运行良好（它包含在 GH Pages gem 的允许列表中），但如果你在其他地方构建（例如通过 Actions 部署预构建的 `_site`），你甚至不需要 GH Pages gem 的限制——任何 Jekyll 构建都可以工作。
- 底层仍然是 meta-refresh/JS，所以有同样的限制：没有真正的 301 状态码。如果你关心爬虫感知的重定向强度，canonical 标签 + meta-refresh 是公认的变通方案，但如果你控制 DNS，通过 Cloudflare Worker/Page Rule 实现的适当 301 重定向更强大。
- 针对你的实际场景——整个域名的迁移 `lzwjava.github.io` → `lzwjava.com`——你完全不需要这个插件；它用于单个 Jekyll 站点内的按页面重定向（例如在重命名永久链接后）。你之前那个单一的根 `index.html` 才是合适的工具。

参考资料：

- [jekyll-redirect-from GitHub 仓库](https://github.com/jekyll/jekyll-redirect-from)
- [GitHub Pages 支持的插件白名单](https://pages.github.com/versions/)
