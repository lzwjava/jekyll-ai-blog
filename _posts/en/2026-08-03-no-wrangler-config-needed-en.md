---
audio: false
generated: true
image: false
lang: en
layout: post
title: No Wrangler Config Needed
translated: false
type: note
---

Short answer: **No — you don't need it for this project.**

## Why

Your repo is a Jekyll blog deployed via GitHub Actions to **Cloudflare Pages** (see `.github/workflows/gh-pages.yml` and your post `deploy-jekyll-blog-to-cloudflare-pages`). Pages deploys don't use `wrangler.jsonc` at all — there is no Worker in this project (I checked: no `wrangler.*` file exists in the repo). So this block would be dead config.

## If you ever *do* add a Worker

Then the block is still **optional**:

- Observability (Workers Logs + Trace Logs) is **enabled by default** for new Workers — omitting `observability` entirely means logging is on.
- You only need this config to **disable** it or **tune sampling** (e.g. `head_sampling_rate: 0.1` to log 10% of requests to save on billing).

## Your pasted block is contradictory

```jsonc
"observability": {
  "enabled": false,          // ← master switch: turns EVERYTHING off
  ...
  "logs": { "enabled": true } // ← but this says logs on
  ...
}
```

The top-level `enabled: false` wins — the nested `logs.enabled: true` is ignored. Don't copy this.

If you want simple, sane logging on a future Worker, use the minimal form:

```jsonc
"observability": {
  "enabled": true,
  "head_sampling_rate": 1
}
```

**Bottom line:** skip it here. Your Pages site already gets request logs in the Cloudflare dashboard for free, no config needed.
