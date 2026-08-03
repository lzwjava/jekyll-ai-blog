---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wrangler Routes Update and Deploy
translated: false
type: note
---

Done. Here's the state of things:

## ✅ `wrangler.jsonc` updated & validated

```jsonc
"routes": [
  { "pattern": "lzwjava.com", "custom_domain": true },
  { "pattern": "www.lzwjava.com", "custom_domain": true },
  { "pattern": "*.lzwjava.com/*", "zone_name": "lzwjava.com" }
]
```

Three deliberate choices:

1. **Both custom domains** — `www.lzwjava.com` is the missing piece; Cloudflare will auto-create its DNS record (no conflict there since www has no record today).
2. **Wildcard route preserved** — wrangler *overrides* (full-syncs) routes on deploy; without this entry, the existing `*.lzwjava.com/*` zone route would have been deleted on the next deploy.
3. **`zone_name` added** — wrangler v4 rejects plain routes without a zone reference.

`npx wrangler deploy --dry-run` passes cleanly (7156 files, no binding errors).

## ⚠️ Don't run `wrangler deploy` from this machine right now

Two blockers:

1. **Stale `_site`** — newest content is 2025-09-19, but `_posts/` has posts from *today*. A direct deploy would revert the live site by ~10 months.
2. **Token is too weak** — it can't even *read* DNS records (auth error 10000), and creating the `www.lzwjava.com` custom domain auto-creates a DNS record. That would fail locally.

## 🚀 Recommended path (matches your existing pipeline)

This project deploys via **Workers Builds** (dashboard-side `bundle install && bundle exec jekyll build` on git push — CI here only handles GitHub Pages). So:

```bash
git add wrangler.jsonc
git commit -m "chore(worker): bind lzwjava.com and www.lzwjava.com custom domains"
git push origin main
```

Workers Builds then: rebuilds a fresh `_site` → deploys with the new routes → creates the `www` custom domain with account-level auth (no token limitation). After it finishes (~2–5 min), verify with:

```bash
curl -sI --max-time 15 https://www.lzwjava.com | head -5
```

Want me to commit and push to `origin/main`?
