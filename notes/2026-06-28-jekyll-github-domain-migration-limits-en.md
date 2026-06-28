---
audio: false
generated: true
image: false
lang: en
layout: post
title: Jekyll GitHub Domain Migration Limits
translated: false
type: note
---

Question: Can I deploy my Jekyll blog on Cloudflare Workers/Pages while keeping the `lzwjava.github.io` domain?

Answer:

No — and the constraint is fundamental, not a config issue. The `*.github.io` domain is owned and controlled by GitHub. Cloudflare can't serve content on a hostname it doesn't control DNS for, and you can't point `lzwjava.github.io` anywhere except GitHub Pages.

Here's the breakdown of why and what your actual options are.

**Why it's impossible**

`lzwjava.github.io` resolves through GitHub's DNS (`github.io` zone), not yours. To put a site behind Cloudflare Pages, Cloudflare needs to either be authoritative for the zone or have a CNAME under a domain you own pointing at `your-project.pages.dev`. You own neither `github.io` nor its DNS. GitHub hardcodes `<user>.github.io` to serve from your Pages repo. There's no DNS record you can create to redirect it.

**What you can actually do**

Build the Jekyll site yourself and push the static output to the `lzwjava.github.io` repo. This keeps the domain but moves the build off GitHub's managed Jekyll (which is what you'd want anyway — custom plugins, newer Ruby, faster builds):

```bash
# build locally or in CI, then push _site to a branch GitHub Pages serves
bundle exec jekyll build
# commit _site contents to the gh-pages-serving branch
```

Better: GitHub Actions builds it, GitHub serves it. You get full control of the toolchain while keeping the `.github.io` host:

```yaml
# .github/workflows/deploy.yml
name: deploy
on:
  push: { branches: [main] }
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with: { ruby-version: '3.3', bundler-cache: true }
      - run: bundle exec jekyll build
      - uses: actions/upload-pages-artifact@v3
        with: { path: _site }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages }
    steps:
      - uses: actions/deploy-pages@v4
```

This is the standard "BYO build" pattern — you escape GitHub's restricted Jekyll sandbox entirely while still serving on `lzwjava.github.io`.

**If you genuinely want Cloudflare Pages**

You need a domain you own (e.g. `lzwjava.com`). Then Cloudflare Pages serves it, and optionally you keep `lzwjava.github.io` as a redirect (a tiny GitHub Pages repo with a meta-refresh or just a JS redirect to the apex domain). This is the move most people make eventually — own the apex domain, treat `.github.io` as a legacy redirect. A custom domain also decouples you from GitHub entirely, which fits your autonomy/self-hosting bias.

So the real question isn't "Workers/Pages + github.io" (impossible) but "do I want to register `lzwjava.com` and migrate?" Given you publish ~400 posts and 8,000 notes, owning the apex is worth the ~$10/yr for portability alone — you'd never be locked to a provider again.
