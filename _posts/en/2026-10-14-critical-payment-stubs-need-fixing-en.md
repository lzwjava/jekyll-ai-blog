---
audio: false
generated: true
image: false
lang: en
layout: post
title: Critical Payment Stubs Need Fixing
translated: false
type: note
---

I have a clear picture now. Here's what I found and what I recommend, in priority order.

## 🔴 Critical: Payments are stubs — this is a monetization platform

The CI3→CI4 migration **silently replaced your real payment SDKs with safe-fail stubs**:

| | CI3 (real) | CI4 (current) |
|---|---|---|
| `Alipay.php` | 85 lines, real RSA signing + config load | 56-line **stub** → returns *"Alipay not configured"* |
| `WxPay.php` | 167 lines, real API integration | 87-line **stub** → returns *"WxPay not configured"* |
| `WxPayCallback.php` | real callback handling | **stub** |
| `Pay.php` facade | calls real SDKs | calls the stubs |

The real CI3 code still exists in `application_ci3/libraries/{alipay,wx}/`, so it's recoverable — but **no payments work today**. The Go tests do exercise `charges`/`attendances`/`wxpayNotify`, so this is a confirmed functional regression.

## Recommended next steps (priority order)

**1. Restore real payments** (highest value) — Port the CI3 `alipay/` and `wx/` SDKs into `app/Libraries/`, wire them through the existing `Pay.php` facade (which is already correctly migrated). The stubs keep controllers from crashing, so this is a clean swap.

**2. Rebuild the Docker image** — I fixed the `Dockerfile` to install GD, but the *running container* doesn't have it yet (`/lives/:id/card` invitation cards are degraded). Run `docker compose up -d --build app`. Quick win.

**3. Fix production debug config** — `app/Config/Boot/production.php` has `display_errors=1` + `CI_DEBUG=true`. That leaks stack traces to clients in production. Should be `CI_DEBUG=false`, `display_errors=0`.

**4. Sweep the 40 POST routes** — I verified all 96 GET routes but only ~4 POST routes by hand. The write paths (charges, packets, withdraws, attendances) are where migration bugs hide.

**5. Make the Go test suite runnable** — It's your regression net but currently can't run: missing `test/go.mod`, targets dead port `3005` (should be `8088`), and DB creds `lzw:@/qulive` don't match the Docker MySQL (`root`/`WeImg4096`). Fixing this gives you automated proof the migration works.

**6. Update `crontab.conf`** — Points at `/home/project/live-server` + `/usr/local/php/bin/php` (old server), not the Docker setup. The handlers (`Jobs::alive`, `Withdraws::withdrawAnchor/NonAnchor`) all exist in CI4, so it's just path/invocation fixup.

**7. LeanCloud** — External, but blocks live creation. Restore the archived app in the LeanCloud console.

## My suggestion
Start with **#1 (payments)** since it's the core business function and the only item that's a real regression rather than config. **#2 and #3** are 5-minute fixes I can do immediately alongside.

Want me to:
- **(A)** Start porting the CI3 payment SDKs now (the big one)?
- **(B)** Do the quick wins first — rebuild image + fix prod debug config (#2, #3)?
- **(C)** Both in parallel?

Which direction do you want to go?