---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clean Up Redundant Build Pipeline
translated: false
type: note
---

Workflow is progressing well (translations done ✅, now on lint/tests/build).

## Answer: Yes, clean them up

Right now, **every push triggers two deployers**:

| | GitHub Actions | Workers Builds (dashboard) |
| --- | --- | --- |
| Triggers | ✅ runs (schedule/manual) | ✅ runs on **every push** |
| What it does | translations → build → `wrangler deploy` (**promotes** to production) | `bundle install && jekyll build` → `wrangler versions upload` (uploads version, **doesn't promote**) |
| Result | ✅ production deploy | ❌ duplicate version churn + wasted build minutes + redundant Jekyll build |

Since GH Actions now does the full job (translations → build → deploy to the Worker), Workers Builds is redundant and will fight it on every push — double builds, version clutter, and confusing history.

**Recommended cleanup** — in the Cloudflare dashboard:

> Worker (`jekyll-ai-blog`) → **Settings → Build** → **Disconnect** the git repository

That removes the connected repo, the Build command, and the Deploy command in one step. The Worker itself stays — GH Actions keeps updating it via `wrangler deploy` with your Cloudflare secrets.

(If you'd rather keep Workers Builds as a fallback CI, the alternative is to make its Deploy command a no-op like `echo skip` — but honestly disconnecting is cleaner than maintaining two pipelines for the same Worker.)

---

I'll keep watching the run — the next checkpoint is the **Deploy to Cloudflare Workers** step (after Jekyll build), which is the moment of truth. Let me check again in a few minutes.
