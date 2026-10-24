---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare Worker Deploy Live
translated: false
type: note
---

**Solved — <https://truthlab.cc/> is live with the newest content.**

The investigation found your site was already a **Cloudflare Worker** named `truth-lab` (route `*.truthlab.cc/*`) — not Pages. So your original `npx wrangler deploy` snippet was right, and I'd mistakenly deployed a Pages project. What changed:

1. **`wrangler.jsonc`** (new) — `name: truth-lab`, `assets: ./` serving the static repo root, `workers_dev: false` so nothing spawns at a workers.dev subdomain.
2. **`src/index.js`** (new) — minimal entry point; assets are served automatically by Workers Static Assets before it runs.
3. **Workflow** — now just: checkout → verify credentials (fail-fast) → `npx --yes wrangler deploy`. The existing `*.truthlab.cc/* → truth-lab` route means every push to `main` updates truthlab.cc automatically.
4. **Cleanup** — deleted the accidental `truth-lab` Pages project (`truth-lab.pages.dev`, which you didn't want) and purged the Cloudflare cache.

Proof: `curl https://truthlab.cc/` SHA-256 (`86e950f2…`) matches the repo's `index.html` byte-for-byte, HTTP 200. Deploy version `db2412b4`.

One note: two older probes remain as commits in git history and the workflow file is now minimal. The domain's apex (`truthlab.cc`) is proxied and on Cloudflare's DNS, so HTTPS/edge caching all work out of the box.
