---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python Jekyll兼容的静态网站生成器
translated: true
type: note
---

完成。以下是 `/home/lzw/projects/jepyll` 中的内容：

## 我构建了什么

一个用 Python 编写的、兼容 Jekyll 的静态网站生成器。它不是根据 Jekyll 的完整功能列表设计的，而是根据你的实际博客（`~/projects/jekyll-ai-blog`）设计的——我阅读了你的站点和 Jekyll 4.4.1 的 Ruby 源码（`~/projects/jekyll`），以精确复现你的内容所依赖的行为。

```
jepyll/
├── cli.py          jepyll build | serve | clean | new
├── config.py       _config.yml + Jekyll defaults/excludes/collections/permalinks
├── frontmatter.py  YAML front matter (Jekyll's exact regexp, incl. empty --- blocks)
├── urls.py         slugify, permalink templates, destination rules
├── dates.py        timezones + Ruby strftime (%-d, %e, ...)
├── reader.py       layouts/includes/collections/pages/static/data (EntryFilter rules)
├── document.py     Page/Document/StaticFile + Liquid drops (lazy post.content)
├── site.py         payload, render pipeline, writing, pruning, -j N workers
├── converters.py   Markdown (math, IAL, headings, smart quotes, autolink, Pygments)
├── sass.py         libsass/sass-CLI backends
├── server.py       dev server with extensionless URLs + watcher
├── liquid/         full Liquid subset: lexer, expr, filters, parser, tags
└── data/themes/    bundled jekyll-theme-cayman SCSS
```

## 验证

- **与 Jekyll 4.4.1 对比**（安装了真实 gem）：用两者构建了测试夹具 → **文件集合完全相同**，并且在去除生成器注释/时间戳后，**12/15 个输出文件逐字节相同**。其余 3 个文件的差异仅在 Pygments 与 Rouge 生成的代码片段，以及 RSS 尾部空白。
- **你的真实博客**：`jepyll build -s ~/projects/jekyll-ai-blog -d /tmp/out -j 4` → **44,573 个文档，0 个错误，耗时 70 秒**（串行约 3.8 分钟），生成 44,446 个 HTML 文件。只有 4 个无害警告（`layout: nil`、`unknown filter: asset_path` ×3 —— Ruby Liquid 也会忽略这些）。
- **41 个测试**全部通过；`ruff` 检查无问题。

## 已匹配的重要行为

- URL：`permalink: /:title` → `/ffmpeg-en` → `ffmpeg-en.html`；`/notes/:path/` → `notes/x/index.html`；从文件名提取 slug/date/title；跳过未来发布的文章；`site.pages` 按名称排序，与 `reader.rb:44` 一致
- Liquid：`{{ "{%" }} raw %}` 会吞掉非法标签，`{{ "{{" }} ... }}` 渲染为空，未知过滤器直接透传，支持 `site[type]` 动态查找，以及 `divided_by` 的整数语义
- Markdown：先掩蔽数学公式，再将 `$$..$$` → `\\[..\\]`（与 kramdown 一致）；支持 `{: .responsive}` IAL、标题 `auto_ids`、智能引号、脚注、GFM 自动链接
- `{{ "{%" }} seo %}` 镜像了 jekyll-seo-tag 2.9.1（基于摘要的描述、`og:locale`、JSON-LD）；当你没有自带 `sitemap.xml` 时会模拟 `jekyll-sitemap`

```bash
cd /home/lzw/projects/jepyll && source .venv/bin/activate
jepyll serve -s ~/projects/jekyll-ai-blog     # build + watch + http://127.0.0.1:4000
```

README 记录了支持矩阵、迁移步骤和已知差异。仓库中有两个提交（`Initial commit`、`feat(markdown): kramdown parity...`）。
