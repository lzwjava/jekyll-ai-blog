---
audio: false
generated: true
image: false
lang: en
layout: post
title: Successful Production Deployment
translated: false
type: note
---

🎉 **Deployed to production successfully** — resolves to the `prod` environment secrets, and the site is live:

- **URL:** https://truth-lab.pages.dev (HTTP 200, title: *Truth Lab — A one-person AI research lab*)
- **Deployment preview:** https://66b2ffaa.truth-lab.pages.dev
- **Run:** `40088249315` — success, 34s (verify credentials → create project → deploy)

What was actually broken along the way, in order:
1. **Secrets empty** → were stored as `prod` *environment* secrets, but the job didn't declare `environment: prod` → added it.
2. **Doubled command** → `wrangler-action@v3` prepends `npx wrangler`, so `command: wrangler pages deploy ...` ran `wrangler wrangler pages deploy ...` → dropped the leading `wrangler` and later switched to a plain `run:` step with `npx --yes wrangler` (also avoids the action's flaky npx install prompt).
3. **Pages project didn't exist** → project was created on the fly: `wrangler pages project create truth-lab --production-branch=main` (idempotent — no-op on future runs).

Site: **https://truth-lab.pages.dev** — deployed to the `prod` environment and serving your content. Now every push to `main` will verify + deploy automatically.
