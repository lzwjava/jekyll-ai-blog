---
audio: false
date: 2025-09-09
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 为Jekyll生成站点地图文件
translated: true
type: note
---

**sitemap.xml** 是一种 XML 文件，用于向 Google 和 Bing 等搜索引擎说明您网站上的页面。它能帮助爬虫更高效地发现和索引您网站的结构。对于 Jekyll 博客而言，这意味着搜索引擎可以找到您的所有文章、页面和翻译版本（例如您的 `index-zh.html`、`index-fr.html` 等），即使它们并未在所有位置被链接。

### Sitemap 的作用

* 列出网站所有重要 URL
* 提供元数据，例如最后修改日期 (`<lastmod>`)、更新频率 (`<changefreq>`) 和优先级 (`<priority>`)
* 通过确保爬虫不会遗漏页面来提升 SEO 效果

### 如何为 Jekyll 生成 Sitemap

您有以下几种方法可选：

#### 1. 使用 `jekyll-sitemap` 插件（推荐）

1. 在 Jekyll 项目的 `Gemfile` 中添加：

   ```ruby
   gem 'jekyll-sitemap'
   ```
2. 在 `_config.yml` 中添加：

   ```yaml
   plugins:
     - jekyll-sitemap
   ```

   （如果您使用 GitHub Pages，`jekyll-sitemap` 已在白名单中，可直接使用）
3. 当执行构建时（通过 `jekyll build` 或已设置的 `make`），Jekyll 会自动在 `_site/` 文件夹中生成 `sitemap.xml` 文件

#### 2. 手动创建 sitemap 模板

如需更精细的控制：

1. 在项目根目录创建文件：`/sitemap.xml`
2. 添加以下 Liquid 模板：

{% raw %}
   ```xml
   ---
   layout: nil
   ---
   <?xml version="1.0" encoding="UTF-8"?>
   <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     {% for page in site.pages %}
       {% if page.sitemap != false %}
         <url>
           <loc>{{ site.url }}{{ page.url | replace:'index.html','' }}</loc>
           <lastmod>{{ page.date | date_to_xmlschema }}</lastmod>
         </url>
       {% endif %}
     {% endfor %}
     {% for post in site.posts %}
       <url>
         <loc>{{ site.url }}{{ post.url }}</loc>
         <lastmod>{{ post.date | date_to_xmlschema }}</lastmod>
       </url>
     {% endfor %}
   </urlset>
   ```
{% endraw %}
3. 确保 `_config.yml` 中设置了 `url: "https://yourdomain.com"` 以正确生成链接

#### 3. 验证

* 构建后检查 `_site/sitemap.xml` 文件
* 将其提交至 Google Search Console 以提升索引效率

---

👉 鉴于您已具备 `_config.yml` 和 `_plugins/` 目录，最简单的方案是直接启用 `jekyll-sitemap`。这样您就无需手动维护 XML 文件。

需要我根据您当前的文件配置，为您起草可直接粘贴到仓库的 `_config.yml` 具体添加内容吗？