---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw Comprehensive Status Report 2026
translated: false
type: note
---

Here's your comprehensive review, Boss. 🦞

---

## 📋 Comprehensive OpenClaw Status Report — 2026-04-04 20:57 HKT

### 🟢 Overall Health: Mostly Good, With Security & Cleanup Items

---

### 1. Core System

| Item | Status |
|------|--------|
| **Version** | 2026.4.2 (latest, up to date) |
| **OS** | Linux 6.8.0-106-generic (x64), Node 22.22.1 |
| **Gateway** | Running (PID 1161683), reachable in 23ms |
| **Bind** | `127.0.0.1:18789` (local only — good) |
| **Auth** | Token + password enabled |
| **Tailscale** | Off |

### 2. Channels

| Channel | Status | Notes |
|---------|--------|-------|
| **Webchat** | ✅ Active | Current session |
| **Telegram** | ✅ OK | Bot @lzwjava_bot, 1601ms latency |
| **openclaw-weixin** | ⚠️ SETUP | Plugin loaded (v2.1.6 ✅), but **no token configured** — needs QR login |
| **Nextcloud Talk** | ⚠️ SETUP | Not configured |

### 3. Plugins (45/87 loaded)
- **openclaw-weixin** — v2.1.6, loaded successfully (just updated from v1.0.3)
- **nextcloud-talk** — loaded, but **duplicate plugin ID warning** (stock bundled vs global extension)
- **google** — web search enabled
- **browser** — Playwright chromium, headless mode

### 4. Cron Jobs

| Job | Schedule | Status | Issue |
|-----|----------|--------|-------|
| **Critical News Summary** | Every hour | ❌ **74 consecutive errors** | `Delivering to Telegram requires target <chatId>` — missing delivery target |

### 5. Sessions
- **29 active** sessions
- Default model: `minimax/minimax-m2.7` (200k ctx)
- Current session model: `xiaomi/mimo-v2-pro`
- 5 session stores

### 6. Memory
- **0 files, 0 chunks** — vector & FTS ready but empty
- No `MEMORY.md` exists
- Only 1 file in `memory/`: a reasoning note from today

### 7. Security Audit — 🚨 5 CRITICAL issues
1. **Control UI `allowedOrigins` = `*`** — any browser origin accepted
2. **Device auth disabled** (`dangerouslyDisableDeviceAuth=true`)
3. **Elevated exec `allowFrom` = `*`** for webchat — anyone gets root
4. **Elevated exec `allowFrom` = `*`** for telegram — anyone gets root
5. **`plugins.allow` not set** — any discovered extension auto-loads

Plus 9 warnings including `exec security=full` with `ask=off` (no confirmation prompts for commands).

### 8. Issues / TODOs
- **Cron job broken**: 74 consecutive failures on news summary — needs a Telegram chat ID in delivery config
- **Nextcloud Talk duplicate**: stock bundled plugin conflicts with global extension
- **WeChat**: plugin loaded but needs QR login to go from SETUP → OK
- **Password in config**: gateway password `lizhiwei17` is stored in plaintext in `openclaw.json`
- **Workspace**: `BOOTSTRAP.md` still exists (says to delete after first run)

---

### Recommended Actions (Priority Order)

1. **🔴 Security**: Tighten `allowedOrigins`, re-enable device auth, restrict elevated exec allowlists, set `plugins.allow`
2. **🔧 Cron**: Fix the news summary delivery target or disable it (74 errors and counting)
3. **📱 WeChat**: Run QR login to finish setup
4. **🧹 Cleanup**: Delete `BOOTSTRAP.md`, resolve nextcloud-talk duplicate
5. **💾 Memory**: Create `MEMORY.md` for long-term continuity

Want me to tackle any of these? 🦞