---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Jekyll-compatible static site generator
translated: false
type: note
---

Done. Here's what's in `/home/lzw/projects/jepyll`:

## What I built

A Jekyll-compatible static site generator in Python, designed from your actual blog (`~/projects/jekyll-ai-blog`) rather than from Jekyll's full feature list — I read both your site and the Jekyll 4.4.1 Ruby source (`~/projects/jekyll`) to reproduce exactly the behaviour your content depends on.

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

## Validation

- **vs Jekyll 4.4.1** (installed the real gems): built the test fixture with both → **identical file set**, and **12/15 output files byte-identical** after stripping generator comments/timestamps. The remaining 3 differ only in Pygments-vs-rouge code spans and RSS trailing whitespace.
- **Your real blog**: `jepyll build -s ~/projects/jekyll-ai-blog -d /tmp/out -j 4` → **44,573 documents, 0 errors, 70 s** (serial ~3.8 min), 44,446 HTML files. Only 4 harmless warnings (`layout: nil`, `unknown filter: asset_path` ×3 — Ruby Liquid ignores those too).
- **41 tests** pass; `ruff` clean.

## Notable behaviours matched

- URLs: `permalink: /:title` → `/ffmpeg-en` → `ffmpeg-en.html`; `/notes/:path/` → `notes/x/index.html`; slug/date/title extraction from filenames; future posts skipped; `site.pages` sorted by name like `reader.rb:44`
- Liquid: `{% raw %}` swallows bad tags, `{{ ... }}` renders empty, unknown filters pass through, `site[type]` dynamic lookups, `divided_by` integer semantics
- Markdown: math masked then `$$..$$` → `\\[..\\]` like kramdown, `{: .responsive}` IALs, heading `auto_ids`, smart quotes, footnotes, GFM autolink
- `{% seo %}` mirrors jekyll-seo-tag 2.9.1 (excerpt-based descriptions, `og:locale`, JSON-LD), `jekyll-sitemap` emulated when you don't ship your own `sitemap.xml`

```bash
cd /home/lzw/projects/jepyll && source .venv/bin/activate
jepyll serve -s ~/projects/jekyll-ai-blog     # build + watch + http://127.0.0.1:4000
```

README documents the support matrix, the migration steps and the known differences. Two commits are in the repo (`Initial commit`, `feat(markdown): kramdown parity...`).
