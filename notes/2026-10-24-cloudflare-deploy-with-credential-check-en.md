---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare deploy with credential check
translated: false
type: note
---

Done. The workflow at `.github/workflows/deploy.yml` now deploys to Cloudflare automatically on every push to `main`, with a fail-fast credential check first.

What changed:
- **Added `env:` block** so `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` from GitHub secrets are available to the shell step.
- **Added `Verify Cloudflare credentials` step** (your exact snippet) — hits the Workers API directly and aborts with a clear `::error::` message if the token/account is wrong, instead of wrangler's cryptic `[code: 10000]`.
- **Kept the `Deploy to Cloudflare Pages` step** — I did *not* switch to `npx wrangler deploy` like your snippet, because that would break. Your snippet is from the `jekyll-ai-blog` project: it depends on a `wrangler.jsonc` config and a worker entry that don't exist in this repo. This repo is a static single `index.html`, so `wrangler pages deploy ./` (already working) is the right mechanism. The verify step works for both.

YAML validated. Push to `main` and it'll run the check + deploy automatically.
