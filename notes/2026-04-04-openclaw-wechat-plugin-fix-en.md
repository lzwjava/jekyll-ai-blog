---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw WeChat Plugin Fix
translated: false
type: note
---

Good question. Let me break down exactly what happened — the full chain from "broken plugin" to "WeChat connected."

---

## 🔍 How WeChat Got Connected — Full Breakdown

### Phase 1: Diagnosis

1. **You asked** to check the WeChat plugin
2. **Ran `openclaw status`** — got a clear error:

   ```
   TypeError: (0, _pluginSdk.resolvePreferredOpenClawTmpDir) is not a function
   ```

3. **Checked the plugin version**: `v1.0.3` (installed March 29)
4. **Searched npm** for latest version: `v2.1.6` exists
5. **Root cause**: v1.0.3 called a function from the OpenClaw Plugin SDK that was removed/renamed in newer OpenClaw (2026.4.2)

### Phase 2: Failed Attempt

1. Ran `npm install @tencent-weixin/openclaw-weixin@2.1.6` inside the extension directory
2. **Why it didn't work**: OpenClaw extensions are **source-first** — it loads `index.ts` and `src/` from the extension directory directly, not from `node_modules`. npm only updated `package.json` + `node_modules/` but the old `.ts` source files were untouched.

### Phase 3: The Fix

1. **Backed up** the old extension dir: `mv openclaw-weixin openclaw-weixin.bak`
2. **Installed to a temp dir** using npm to get the v2.1.6 source files:

   ```
   npm install @tencent-weixin/openclaw-weixin@2.1.6 --prefix weixin-tmp
   ```

3. **Copied the source** from `weixin-tmp/node_modules/@tencent-weixin/openclaw-weixin/` → new `openclaw-weixin/` directory (this time getting the actual v2.1.6 source files)
4. **Ran `npm install`** inside the new dir to install dependencies (557 packages)
5. **Cleaned up** temp dirs
6. **Verified**: `package.json` now shows `"version": "2.1.6"` and `openclaw status` no longer throws the SDK error

### Phase 4: QR Login

1. **Read the plugin source** to find the login command — found it registers via `openclaw channels login --channel openclaw-weixin`
2. **The login flow**:
   - Plugin calls `https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3` to get a QR code
   - Renders it in terminal as ASCII art + provides a direct URL
   - Long-polls `get_qrcode_status` every 1 second for up to 8 minutes
   - States: `wait` → `scaned` → `confirmed`
   - On `confirmed`, saves `bot_token` + `ilink_bot_id` + `baseurl` to `openclaw.json`
3. **You scanned the QR code** in WeChat, confirmed in the app
4. Plugin got back `bot_token`, wrote config to disk
5. `openclaw gateway restart` to reload with the new account

### What Each Tool Did

| Tool | Purpose |
| ------ | --------- |
| `exec` | Ran all shell commands — npm install, openclaw status, grep, file reads |
| `process` | Monitored long-running commands (mtr, npm, login) |
| `read` | Read plugin source code to understand the login API |
| `web_search` / `memory_search` | Context gathering (didn't need web search this time) |
| `cron` | Reviewed existing cron jobs for the comprehensive report |

### Why It Worked

The key insight was that OpenClaw extensions are **not standard npm packages** — they're loaded as source from the extensions directory. A simple `npm install` wouldn't replace the `.ts` files. I had to get the new source via npm in a temp location, then copy it over wholesale. 🦞
