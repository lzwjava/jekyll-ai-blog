---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to redirect GitHub Pages user site
translated: false
type: note
---

Question: How to redirect the GitHub Pages user site `lzwjava.github.io` to `lzwjava.com`.

Answer: GitHub Pages is static-file hosting only — no server config, so you can't emit a real HTTP 301/302 status code. What people call "redirect" here is an HTML meta-refresh + JS fallback, which browsers treat functionally the same as a redirect (near-instant, no visible content) but crawlers see it as a client-side redirect, not a true 3xx. If you need an actual 301 you'd have to front it with Cloudflare (Workers/Page Rules), not GitHub Pages.

Since `lzwjava.github.io` is your special GitHub *user* page repo, do it there directly:

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
  <title>Redirecting…</title>
  <link rel="canonical" href="https://lzwjava.com/">
  <meta http-equiv="refresh" content="0; url=https://lzwjava.com/">
  <script>location.replace("https://lzwjava.com/");</script>
</head>
<body>
  <p>Moved to <a href="https://lzwjava.com/">lzwjava.com</a></p>
</body>
</html>
```

```bash
rm -f CNAME   # make sure no old custom domain file conflicts with the redirect page
git add -A
git commit -m "redirect lzwjava.github.io -> lzwjava.com"
git push
```

Notes:

- If your repo currently has a `CNAME` file pointing to a custom domain, delete it — otherwise GitHub Pages tries to serve this repo under that domain instead of `lzwjava.github.io`.
- If SEO matters (you don't want Google treating this as duplicate/canonical confusion), the `rel="canonical"` tag above tells crawlers the real URL is `lzwjava.com`, which is the standard mitigation for JS-based redirects.
- If your site is Jekyll and you want per-page redirects (not just root), use `jekyll-redirect-from` plugin — but for a single root→root move, the static `index.html` above is simpler and matches what you already do with `zz`/`ww` CLI-style minimalism.
- True 301 alternative: point `lzwjava.github.io` at a Cloudflare Worker route instead of GitHub Pages, and return `Response.redirect(url, 301)` — but that requires you own DNS for github.io subdomains, which you don't (GitHub does), so this only works if you're redirecting *from* a domain you control, not from the `.github.io` subdomain itself.

References:
- [Redirects for GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/setting-up-a-custom-domain-for-your-github-pages-site)
- [jekyll-redirect-from plugin](https://github.com/jekyll/jekyll-redirect-from)