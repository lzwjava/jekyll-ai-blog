---
audio: false
generated: true
image: false
lang: en
layout: post
title: Migrate to Cloudflare Workers Deploy
translated: false
type: note
---

Done. Here's the full picture:

## What I changed

**`.github/workflows/gh-pages.yml`** (commit `17f9a67b6`):
- ✅ Kept all your automation: language translation, notes translation, table fixes, markdown linting, tests, release hash — these **must** stay in GitHub Actions because they push commits back to the repo (Cloudflare's build would loop forever: push → build → push → …)
- ❌ Removed the GitHub Pages steps (`configure-pages`, `upload-pages-artifact`, `deploy-pages`) and the `github-pages` environment
- ➕ Added `Deploy to Cloudflare Workers` step: `npx wrangler deploy` — reads `wrangler.jsonc` and uploads the freshly built `_site` to your `jekyll-ai-blog` Worker
- ➕ Added `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` env vars from secrets

## You must do 2 things

**1. Add GitHub secrets** (otherwise the deploy step fails):
- `CLOUDFLARE_API_TOKEN` — create at dash.cloudflare.com → **My Profile → API Tokens → Create Token** → template **"Edit Cloudflare Workers"** (Workers Scripts: Edit). Copy it.
- `CLOUDFLARE_ACCOUNT_ID` — dash.cloudflare.com → right sidebar shows your Account ID.
- Then: GitHub repo → **Settings → Secrets and variables → Actions → New repository secret** for each.

**2. Disconnect Workers Builds** in the Cloudflare dashboard (the Worker → **Settings → Build → disconnect the repo**). Otherwise every push triggers *both* GitHub Actions and Workers Builds → duplicate deploys and version churn. GH Actions becomes the single deployer; the Worker itself stays.

## Notes

- ⚠️ **Your `lzwjava.github.io` will stop updating** — this workflow was what deployed it. If you want Pages as a fallback, keep it as a second step; say the word.
- 🌐 The site will now live at `jekyll-ai-blog.<your-subdomain>.workers.dev` (or add a custom domain in the Worker → Settings → Domains & Routes). If you serve from a different domain, update `url:` in `_config.yml` — sitemap/SEO/feeds use it.
- ⏰ Deploys run on the 2-hour schedule + manual `workflow_dispatch` (you removed the `push:` trigger earlier to stop the self-cancelling loop — bot commits get deployed on the next scheduled run, which is the intended behavior).

Push `17f9a67b6` (plus the earlier `c33f924ca`) when ready — and trigger the workflow manually (`Actions → Deploy Jekyll → Run workflow`) to verify the first Cloudflare deploy.