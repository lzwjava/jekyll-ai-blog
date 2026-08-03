---
audio: false
generated: true
image: false
lang: en
layout: post
title: Jekyll Redirect Plugin Internals
translated: false
type: note
---

Question: How does the `jekyll-redirect-from` plugin work internally?

Answer: It's a build-time Jekyll generator — no server/runtime involved, since Pages is static hosting. At `jekyll build` time it hooks into the generator pipeline, reads `redirect_from`/`redirect_to` front matter on each page, and for every old path listed, it generates a small static HTML file at that path containing a meta-refresh + JS redirect to the real page. Same primitive as the manual `index.html` I gave you earlier — the plugin just automates generating one of those files per old URL instead of you hand-writing each one.

Mechanics:

```yaml
---
title: My Post
redirect_from:
  - /old-url/
  - /2019/01/01/old-post.html
---
```

At build time this produces (roughly):

```
_site/old-url/index.html
_site/2019/01/01/old-post.html
```

Each generated file looks like:

```html
<!doctype html>
<html>
<head>
  <link rel="canonical" href="https://lzwjava.com/my-post/">
  <meta http-equiv="refresh" content="0; url=https://lzwjava.com/my-post/">
</head>
<body>
  <p>This page has moved. <a href="https://lzwjava.com/my-post/">Click here</a>.</p>
</body>
</html>
```

Reverse direction also exists — `redirect_to` on a page makes that page itself redirect out to an external URL, useful for your github.io → lzwjava.com case if you wanted per-page granularity instead of one root redirect:

```yaml
---
redirect_to: https://lzwjava.com/some-post/
---
```

Install:

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

Caveats given your setup:

- Since it runs at build time and just emits static files, it works fine on GitHub Pages' whitelisted-plugins build (it's in the GH Pages gem allowlist), but if you're building elsewhere (e.g. deploying prebuilt `_site` via Actions), you don't even need the GH Pages gem restriction — any Jekyll build works.
- Still meta-refresh/JS under the hood, so same limitation as before: no real 301 status code. If you care about crawler-perceived redirect strength, canonical tag + meta-refresh is the accepted workaround, but a proper 301 via Cloudflare Worker/Page Rule is stronger if you control DNS.
- For your actual case — whole-domain move `lzwjava.github.io` → `lzwjava.com` — you don't need this plugin at all; it's for per-page redirects within a single Jekyll site (e.g. after renaming permalinks). Your single root `index.html` from before is the right-sized tool.

References:
- [jekyll-redirect-from GitHub repo](https://github.com/jekyll/jekyll-redirect-from)
- [GitHub Pages supported plugins allowlist](https://pages.github.com/versions/)