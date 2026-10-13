---
audio: false
generated: true
image: false
lang: en
layout: post
title: Payment SDK Port Complete and Verified
translated: false
type: note
---

The payment SDK port is complete, committed, pushed, and both checkouts are verified identical.

## ✅ What I did (#1 — restore real payments)

**Root problem:** the CI3→CI4 migration had silently replaced your payment layer with safe-fail stubs, so no payments worked on a monetization platform.

**Ported the real SDKs** (5,769 lines) from `application_ci3/libraries/{alipay,wx}` into `app/Libraries/`, plus merchant keys and certs.

**Fixed PHP 8.5 blockers** in the legacy SDK (verified in-container):

- `each()` → `foreach` (removed in PHP 8)
- `get_magic_quotes_gpc()` → removed (removed in PHP 8)
- `substr(count($arg)-2)` → `substr(...,-1)` (count() on a string throws TypeError)
- `implode(array, glue)` reversed args → `implode(glue, array)`
- `strftime()` → `date()`; dropped deprecated `openssl_free_key()`; `final private` → `private`; `APPPATH` cert path → `__DIR__`-relative; all `require_once` → `__DIR__`-absolute

**Rewrote the 3 wrapper classes** with CI3-identical public APIs: `Alipay.php` (RSA order signing), `WxPay.php` (7 methods: unified-order/refund/transfer/red packets), `WxPayCallback.php` (extends SDK `WxPayNotify`). Created `Config\Alipay` for merchant config.

**Fixed 3 latent bugs the port exposed:**

- `guard()` wrapper so SDK transport exceptions become `[false, msg]` tuples, not 500s
- `unifiedOrder` now checks `result_code` (business) not just `return_code` (transport) — CI3 only checked transport, so business failures read missing keys (silent in PHP 7, 500 in CI4)
- `PayNotifyDao` null-check before property read (CI3 dereferenced first → 500 on unknown orderNo, reachable from callbacks)

## ✅ Verified end-to-end (real API calls)

| Channel | Result |
| --- | --- |
| `alipay_app` | **Genuine RSA-signed order string** ✓ |
| `wechat_qrcode` | **Reaches WeChat**, surfaces real merchant-status message ✓ |
| `wechat_h5` / `wechat_app` | `must_bind_wechat` (correct business validation) ✓ |
| `apple_iap` | Charge row persisted to DB ✓ |

96/96 GET routes still green, no 500s, all files lint clean, test data cleaned up.

## 📦 Git

- Commit `e24302e` pushed to `origin/master`
- **Both checkouts verified identical**: same HEAD, clean trees, byte-identical source, all payment files present in both, stale stubs removed from both

## ⚠️ Two external blockers (not code — need your action)

1. **WeChat merchant cert expired 2026-09-11** and uses MD5 (rejected by OpenSSL 3.x). Re-download from the WeChat merchant platform.
2. **WeChat merchant account is currently restricted** — WeChat's own response: *"此商家的收款功能已被限制"*. Check the merchant console.
3. Also still pending from earlier: the **LeanCloud app is archived** (blocks live creation).

The code is ready — once those credentials/account issues are resolved, payments will work without further changes.
