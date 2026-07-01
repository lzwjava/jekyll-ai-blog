---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choose CI4 Over CI3 Migration
translated: false
type: note
---

Question: Given the current CI4 migration status and the two fix options described, which option should be chosen — Option A (finish the CI4 refactor) or Option B (downgrade to PHP 8.3 + keep CI3)?

Answer:

## Decision Framework: Option A vs Option B

This is not purely a technical decision — it's a **business risk + time horizon** decision. Here's a structured breakdown:

---

### 🔴 Why Option B (Stay on CI3 + PHP 8.3) Is a Trap

Option B feels safe because it's fast, but the landscape in 2026 has changed significantly:

**CI3 has no official PHP 8.2+ support.** CI3 remains in maintenance mode, receiving only limited security fixes, and it is not officially guaranteed to support PHP 8.2 or higher without community-applied patches.

**PHP 8.3 + CI3 is a known problem.** Running PHP 8.3 with CI 3.1.13 generates errors such as "Creation of dynamic property is deprecated" in core files. You'd be manually patching the framework yourself — and that's an ongoing burden, not a one-time fix.

**PHP versions have EOL timelines.** The currently supported PHP versions are 8.2 (until December 2026), 8.3 (until December 2027), and 8.4 (until December 2028). CI3 doesn't officially support any of them — so every PHP version bump creates fresh risk.

**Developer availability will only shrink.** Finding developers willing to work on CodeIgniter 3 in 2026 is increasingly difficult — modern engineers gravitate toward current frameworks and actively avoid legacy stacks.

---

### 🟢 Why Option A (Finish the CI4 Refactor) Is the Right Call

You've already done the heavy lifting. The review shows:

- 25 controllers migrated ✅
- 32 models migrated ✅
- Framework booting, routes resolving, database/Redis connected ✅
- Infrastructure (Docker, Nginx, PHP 8.5 FPM) solid ✅

**The only remaining blockers are 3 legacy libraries:** `JSSDK`, `REST_Controller`, and `WeChat SDK`. These use `get_instance()` — the CI3 global singleton. CI4 is a rewrite of the framework and is not backwards compatible — it is more appropriate to think of converting your app, rather than upgrading it. You've already converted 90% of the app. The last 10% is now concentrated in these libraries.

PHP 8.5 requires CodeIgniter 4.7.0 or later — your stack (PHP 8.5.4 + CI4 v4.7.2) is perfectly matched and officially supported.

---

### 🛠️ Concrete Fix Plan for Option A

**Replace `get_instance()` in JSSDK:**

In CI4, there is no global `get_instance()`. The correct pattern is dependency injection or using the service container:

```php
// CI3 (broken)
$CI =& get_instance();
$CI->load->library('session');

// CI4 replacement
$session = \Config\Services::session();
// or inject via constructor
```

**Replace `REST_Controller`:**

CI4 has native API resource controllers. Replace:

```php
// CI3 pattern (broken)
class Api extends REST_Controller { ... }

// CI4 pattern
use CodeIgniter\RESTful\ResourceController;
class Api extends ResourceController { ... }
```

**Replace `$this->load->*` patterns:**

```php
// CI3 (broken)
$this->load->model('UserModel');

// CI4
$userModel = new \App\Models\UserModel();
// or
$userModel = model('UserModel');
```

**WeChat/WeChatPlatform SDK:**
These likely only use `get_instance()` to access config or DB. Extract those dependencies and pass them in via constructor injection.

---

### 📊 Decision Matrix

| Factor | Option A (CI4 Refactor) | Option B (CI3 + PHP 8.3) |
| --- | --- | --- |
| Time to fix | ~2 hours (estimated) | 5 minutes |
| Long-term viability | ✅ Officially supported | ❌ Unsupported & declining |
| PHP compatibility | ✅ PHP 8.5 officially | ⚠️ Requires manual patches |
| Security posture | ✅ Active development | ❌ Maintenance-only |
| Performance | ✅ JIT + PHP 8.5 gains | ❌ No JIT, older runtime |
| Future dev hiring | ✅ Modern stack | ❌ Shrinking talent pool |
| Work already done | Wasted if you abandon | - |
| Technical debt | Eliminated | Compounded |

---

### ✅ Final Verdict

**Choose Option A.** You are one focused coding session away from a fully modern, officially supported stack. Option B is a 5-minute fix that buys you perhaps 12–18 months before you face the exact same decision again — with even fewer options and more technical debt.

The three libraries blocking you (`JSSDK`, `REST_Controller`, `WeChat SDK`) are well-understood CI3 patterns with direct CI4 equivalents. This is the last mile — don't turn back now.

> **If time pressure is critical today:** Use a temporary shim — wrap `get_instance()` with a compatibility function that returns a service locator object, unblock the app, deploy, then refactor properly. This gets you running in under 30 minutes without abandoning CI4.

References:

- [Still Running CodeIgniter 3? Your Migration Options in 2026](https://pegotec.net/still-running-codeigniter-3-your-options-in-2026/)
- [CodeIgniter 4 Server Requirements](https://codeigniter.com/user_guide/intro/requirements.html)
- [Upgrading from CI3 to CI4 — Official Docs](https://codeigniter4.github.io/userguide/installation/upgrade_4xx.html)
- [Upgrading CodeIgniter — Zend Guide](https://www.zend.com/blog/upgrading-codeigniter)
- [pocketarc/codeigniter — CI3 fork for PHP 8.5](https://github.com/pocketarc/codeigniter)
- [CI3 PHP 8.3 issue tracker](https://github.com/bcit-ci/CodeIgniter/issues/6278)
