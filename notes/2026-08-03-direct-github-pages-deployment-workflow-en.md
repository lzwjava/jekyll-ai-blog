---
audio: false
generated: true
image: false
lang: en
layout: post
title: Direct GitHub Pages deployment workflow
translated: false
type: note
---

Done. The workflow now builds `_site` in this repo and deploys it via the standard GitHub Pages actions instead of pushing to `lzwjava/lzwjava.github.io`.

**Changes in `.github/workflows/gh-pages.yml`:**
- Removed the `Check out destination repo` and `Sync built site to destination repo` steps (no more PAT_TOKEN / rsync push to the second repo)
- Added the standard Pages deploy chain after `Build with Jekyll` (which already outputs `./_site`):
  - `actions/configure-pages@v5` → `actions/upload-pages-artifact@v3` (path `_site`) → `actions/deploy-pages@v4`
- Enabled `push` on `main` (per your template), kept the 2-hour schedule and `workflow_dispatch`
- Set the environment URL from the deploy step output, concurrency group now `pages`

**`_config.yml`:**
- Set `baseurl: "/jekyll-ai-blog"` — since the site now lives at this repo, GitHub Pages serves it at `https://lzwjava.github.io/jekyll-ai-blog/`. Without this, all asset/link/permalink paths would break.

Two things to note:
1. In repo **Settings → Pages**, set Source to **GitHub Actions** (if it was previously set to a branch).
2. The `PAT_TOKEN` secret is no longer used by this workflow.

Keep in mind the translation steps commit + push to `main`, so with the new push trigger each of those commits will re-run the pipeline (translations are idempotent, so it settles after a no-op run and just rebuilds/deploys).
