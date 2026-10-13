---
audio: false
generated: true
image: false
lang: en
layout: post
title: GD rebuild and debug config fix
translated: false
type: note
---

Both done and verified. Here's the summary.

## ✅ #2 — Rebuild image with GD
- Rebuilt the `app` image with the corrected `Dockerfile` (GD is now actually installed, not just configured).
- Verified: `gd`, `imagecreate()`, `imagecreatetruecolor()` all present.
- Outcome: `/lives/:id/card` (invitation cards) now proceeds past the GD check to proper auth handling instead of being degraded.

## ✅ #3 — Production debug config fixed
- **`app/Config/Boot/production.php`** → now production-safe: `CI_DEBUG=false`, `display_errors=0`, `log_errors=1`, `E_DEPRECATED` suppressed. Errors still log to `writable/logs`, but stack traces/paths are no longer leaked to clients. This is what a real deploy uses.
- **Root cause found along the way:** docker-compose set `CI_ENV=production` — but **CI4 reads `CI_ENVIRONMENT`**, so that var was a silent no-op and the app always defaulted to production mode. Fixed the name.
- To avoid killing your error visibility while developing, I pointed the **local** stack at `CI_ENVIRONMENT=development` (docker-compose). You keep full debug traces locally; production stays locked down.
- **Side effect caught & handled:** development mode re-enabled `E_ALL`, which let the Qiniu SDK's PHP 8.5 deprecation (`Config.php:44`) prefix JSON bodies — it corrupted `/wechat/wxpayNotify`, a **payment callback**. Added `& ~E_DEPRECATED` to `development.php` (matching production). Real errors/warnings still display.

## Verified after rebuild
- **96/96 GET routes** return HTTP 200
- **95/96 return clean valid JSON** (the 1 exception, `/wechat/wxpayNotify`, is *intentionally* plain-text `success` — not pollution)
- Stack healthy: app/database/redis/web all up

## One thing to know for your upcoming payment work
In development mode, CI4's **DebugBar appends `<script>` HTML** to responses. That's cosmetic for JSON routes, but for a plain-text payment callback like `wxpayNotify` it appends HTML after `success`. It won't affect real production (CI_DEBUG=false there), but if you **tunnel a live WeChat/Alipay callback to localhost for testing**, that trailing HTML could break callback verification. Worth remembering when you get to the payments port — easy to work around by testing callbacks against a production-mode instance.

## Not yet committed
Three files changed (in the live workspace copy, which Docker mounts):
- `app/Config/Boot/production.php`
- `app/Config/Boot/development.php`
- `docker-compose.yml`

Want me to **sync these to the canonical repo and commit** (and push)? Then you'd be set to move on to **#1, the payment SDK port**, which is the big one.