---
audio: false
generated: true
image: false
lang: en
layout: post
title: Database Connection and Library Fixes
translated: false
type: note
---

**Fixed!** 🦞 Here's what I did in this session:

---

## What was fixed

### 🔴 P0 — Database connection
- **`app/Config/Database.php`** — was hardcoded with `hostname: 'localhost'`. The env vars (`DB_HOST=database`) were injected into the container but never read by CI4's `$default` config. Fixed with `getenv()` calls in the constructor. **Result: DB now connects.**

### 🔴 P0 — Missing `JSSDK` library
- **`app/Libraries/JSSDK.php`** — created from scratch (CI4, no `get_instance()`, proper DI via `WxDao` and `WeChatClient`)
- **`app/Libraries/WeChatPlatform.php`** — created (all notification/template message methods)
- **`app/Models/UserDao.php`** — added `use App\Libraries\JSSDK;` to fix PHP namespace resolution (inside `App\Models`, `new JSSDK()` was resolving as `App\Models\JSSDK`, not global `JSSDK`)

### 🟡 P1 — Missing `Pay`, `Sms`, `LeanCloud` libraries
- **`app/Libraries/Pay.php`** — created (payment processing for Alipay/WeChat)
- **`app/Libraries/Sms.php`** — created (LeanCloud SMS notifications)
- **`app/Libraries/LeanCloud.php`** — created (CI4-compatible HTTP client)
- **`app/Config/Autoload.php`** — added classmap entries for all CI3-style class names

### ✅ Result: `curl localhost:8088/` → **HTTP 200**

---

## What's still outstanding (not blocking, but needed)

| Item | Priority | Notes |
|------|---------|-------|
| `WxPay`, `Alipay`, `WxPayCallback` stubs | 🟡 P1 | Used by `Wechat`, `Charges`, `Rewards` controllers — will 500 if those endpoints hit |
| `$this->load->library()` / `$this->load->model()` in all 20 controllers | 🟡 P1 | Still CI3-style, need DI or `Services::` refactor |
| Routes | 🟡 P1 | Only `/` defined — all other CI3 routes need CI4 `$routes->` entries |
| `REST_Controller` removal | 🟢 P2 | API controllers may still extend it — need to check |

Want me to continue with the P1 items, or are you good for now?