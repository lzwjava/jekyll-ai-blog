---
audio: false
generated: true
image: false
lang: en
layout: post
title: API Testing and Migration Updates
translated: false
type: note
---

Done. Here's the full rundown:

### ✅ Login/Session Testing — Working
- `POST /login` with `13888888888` + `smsCode=5555` → returns session token (uses `specialPhones` bypass)
- `GET /self` with cookie → returns user data
- `GET /lives/attended` without auth → returns `not_in_session` (was a 500 crash)
- `GET /accounts/me`, `/attendances/me` → all work with auth

### ✅ Query Builder Migration — 21 DAO files fixed
- All `$this->db->insert(TABLE, $data)` → `$this->db->table(TABLE)->insert($data)`
- All `where()+update` patterns → chained calls
- `insert_id()` → `insertID()`, `num_rows()` → `getNumRows()`
- BaseDao field arrays converted from snake_case to camelCase to match DB schema

### ✅ Missing Helpers Added
- `isDebug()`, `specialPhones()`, `channelSet()`, `errorInfos()`, `session_unset()`
- Autoloaded `text` helper for `random_string()`

### ✅ Response Double-Output Bug Fixed
- Echo + empty body trick to prevent CI4 from duplicating output

### ✅ Payment Stubs — Safe
- Return "not configured" errors instead of crashing. Ready for real SDK when credentials are available.

### Still needs real config:
- **LeanCloud** credentials → needed for live creation (IM conversations) and SMS
- **WxPay/Alipay** credentials → needed for real payments

**30/30 routes = HTTP 200**, auth flow works end-to-end. Committed as `48e3c6e`.