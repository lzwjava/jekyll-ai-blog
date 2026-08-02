---
audio: false
generated: true
image: false
lang: en
layout: post
title: Workers Builds wrangler fix
translated: false
type: note
---

Done. Here's what was happening and how it's fixed:

## Root cause

Your repo deploys fine to **GitHub Pages** via GitHub Actions. But the error you pasted is from a **separate Cloudflare Workers Builds** connection — Cloudflare's CI runs `npx wrangler deploy`, and since the repo had no wrangler config, wrangler had no Worker name (`"undefined"`) and no `compatibility_date` → hard failure.

## Changes made (committed as `c33f924ca`)

**1. `wrangler.jsonc` (new, repo root)** — declares the Worker using the documented SSG/static-assets pattern:
```jsonc
{
  "name": "jekyll-ai-blog",
  "compatibility_date": "2026-08-02",
  "assets": {
    "directory": "./_site",
    "not_found_handling": "404-page",
    "html_handling": "auto-trailing-slash"
  }
}
```
- `name` fixes the "undefined" warning; `compatibility_date` fixes the hard error
- No `main` script — it's a pure static-site Worker serving Jekyll's `_site` output
- Verified with `wrangler deploy --dry-run`: reads 7156 files, no errors

**2. `_config.yml`** — excluded `assets/epub/lzwjava-blog-en.epub` (31.8 MiB > Workers' 25 MiB/file limit; unreferenced anywhere). It's actually gitignored so it wouldn't hit CI anyway — this is a harmless safety net for local builds.

## ⚠️ One required dashboard step (can't be done from the repo)

Workers Builds **does not read build commands from `wrangler.jsonc`** (documented limitation). Since `_site` is gitignored, the CI clone has no built site. In the Cloudflare dashboard:

> **Your Worker → Settings → Build → Build command:**
> ```
> bundle install && bundle exec jekyll build
> ```

Ruby 3.4.4 + bundler are preinstalled in the Workers Builds image, so Jekyll builds fine there. (Optionally enable **Build caching** to speed up `bundle install`.)

## Then

1. `git push` (the fix must be in the repo Cloudflare builds from)
2. Retry the failed build in the dashboard (Workers Builds → Retry) — or push will trigger a new build

## Notes

- Your GitHub Pages workflow is unaffected.
- Two of your blog posts now contain outdated advice: *"No Wrangler Config Needed"* (2026-08-03) and *"Wrangler auto config causes Hugo error"* (2026-06-27) — they concluded Workers didn't need a config, but Workers Builds specifically does. Want me to update them?