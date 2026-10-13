---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stack Up, All Bugs Fixed
translated: false
type: note
---

Done. The stack is up, verified, and all fixes are committed. Here's the complete picture.

## What I did

**1. Brought the stack up** (from the runnable workspace copy at `~/.openclaw/workspace/live-server`, which Docker mounts):
- All 4 containers healthy: `app` (PHP 8.5-FPM), `database` (MySQL 5.7), `redis`, `web` (nginx on :8088).

**2. Swept every endpoint** — all 96 GET routes + the auth/live write flows. Found **10 endpoint failures + 7 latent bugs**, all traced to CI3→CI4 semantic differences.

## Bugs found & fixed

**Database layer**
- `BaseDao` field prefixes had a trailing dot (`'users.'`) while `mergeFields()` adds its own → invalid SQL `SELECT users..userId`. Broke `/users/:id`.
- Associative-array binds: CI3's `compile_binds()` called `array_values()`, so assoc binds worked positionally; CI4 treats string-keyed binds as *named* binds (`:name`), so `WHERE x=?` got no substitution → syntax error. Fixed in `RewardDao`, `CouponDao`, `WithdrawDao`.
- `$this->db` missing on controllers; CI3 `trans_begin`/`affected_rows` → CI4 `transBegin`/`affectedRows` (16 sites).

**Libraries / config**
- `JSSDK`: `env('WECHAT_API_BASE'/'CGIBIN')` are **null** (they're constants, not env vars) → all WeChat URLs were relative. This is why WeChat "curl error'd."
- `JSSDK`: missing `addNews`/`uploadImg`/`sendMassMsg`; nullable `code` params (missing `?code=` was a TypeError).
- `WeChatClient::httpPost` silently **dropped the POST body** and appended no query string.
- `LeanCloud` read empty `env('LC_PROD_APP_ID')` instead of the real `LC_APP_ID` constants → broke SMS + live creation.
- Boot suppressed `E_DEPRECATED` so the Qiniu SDK's PHP 8.4 deprecation stopped prefixing every JSON response.
- `Dockerfile` configured GD but never installed it.

**Controllers**
- `logout` (PHP native `session_unset` can't be overridden), `notifyLiveStartRecommend` (empty guard let null reach SQL), `invitationCard` (undefined `phpInfo`), `login` + `uploadImg` (null-derefs → 500).

## Verified working
- **96/96 GET routes** return 200, clean JSON.
- Full **register → login → self → logout** session lifecycle, both cookie and token auth.
- **Qiniu** uptoken, **Redis** (`PONG`), **DB** queries, **transactions** (`topics/init` seeded 13 topics), **WeChat JSSDK** now returns a real signature + real API responses.

## Notes
- **Live creation is blocked only by an external issue**: the upstream LeanCloud app is archived (`504: The app is archived, please restore in console`). The code is correct — it now sends real credentials (getting an authenticated response) versus the previous empty `X-LC-Id`. Restoring the app in the LeanCloud console is all that's needed.
- **Two checkouts now identical**: canonical git repo `/home/lzw/projects/live-server` (2 new commits, clean) and the live workspace copy. Test users I created were cleaned up.

**Commits** (on `master`, not pushed):
- `41c879c` — main CI4 migration bug fixes (24 files)
- `3383cdb` — null-deref guards in login + uploadImg

Want me to push these, or leave them local for your review?