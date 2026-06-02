---
audio: false
generated: true
image: false
lang: en
layout: post
title: Database Migration Review Findings
translated: false
type: note
---

Here's the migration review:

---

## 🦞 CI3→CI4 Migration Review

**Overall: Good foundation, but the app is still broken at the database layer.**

### ✅ What's Done Well

- **Container stack** is solid — PHP 8.5-FPM + nginx + MySQL 5.7 + Redis, all running and communicating on Docker internal networking
- **BaseController** is properly migrated — CI4-style HTTP request methods, response helpers, session handling
- **BaseDao** exists with `SET NAMES utf8mb4` initialization
- **WeChatClient** is clean CI4-compatible code (no `get_instance()` dependencies)
- **CI4 `public/index.php`** is correct with proper `Boot::bootWeb()` entry point
- **Constants/env** are populated with all the real keys (WeChat, Qiniu, RTMP, DB credentials)

### 🚨 Critical Blockers (App = HTTP 500)

**1. Database connection is completely broken (THE root cause right now)**

```
mysqli_sql_exception: No such file or directory
```

`app/Config/Database.php` has `hostname: 'localhost'` hardcoded — inside the container, MySQL is on the `database` host, not a socket file. The env vars (`DB_HOST=database`, `DB_USER=root`, `DB_PASS=WeImg4096`) are injected into PHP but **never read by the `Database.php` config**. It needs to pull from `$_ENV` or `env()`.

**2. Every controller still uses CI3-style `$this->load`** (~60+ occurrences across ~20 controllers):

```php
$this->load->library(JSSDK::class);
$this->load->model(UserDao::class);
$this->load->library(WeChatPlatform::class);
```

These need to become constructor-injected or service-locator resolved in CI4.

**3. Libraries directory is almost empty** — `WeChatClient.php` is there, but:

- `JSSDK.php` — **missing**, still CI3
- `WeChatPlatform.php` — **missing**, still CI3
- `Pay.php`, `Sms.php`, `wx/WxPay.php`, `wx/WxPayCallback.php` — all missing CI4 versions

**4. No `REST_Controller`** — checking the grep output showed no `REST_Controller` references, which is good (may have already been handled), but need to confirm all API controllers work.

### 📋 Remaining Work (Priority Order)

| Priority | Task | Effort |
|---------|------|--------|
| 🔴 P0 | Fix `Database.php` to read env vars (`hostname => env('DB_HOST', 'database')`) | 5 min |
| 🔴 P0 | Fix `BaseController` constructor — remove eager `new UserDao()` that triggers DB on every request | 10 min |
| 🟡 P1 | Rewrite `JSSDK.php` for CI4 (`Services::curlrequest()`, `Services::cache()`) | ~1 hr |
| 🟡 P1 | Create CI4 `WeChatPlatform` library | ~1 hr |
| 🟡 P1 | Fix all 20 controllers with `$this->load->model/library` → proper DI | ~2 hr |
| 🟢 P2 | Verify Pay, Sms, WxPay libraries | ~1 hr |
| 🟢 P2 | End-to-end test all major routes | ~1 hr |

### 💡 The Fastest Path to HTTP 200

1. Fix `Database.php` env reading → might get to a different error (rather than DB fail)
2. Delay `UserDao` instantiation in `BaseController` → lazy init or remove from constructor
3. Fix `JSSDK.php` → that alone might unblock most WeChat routes
4. Then tackle the `$this->load` refactor controller by controller

Want me to start fixing from the top?
