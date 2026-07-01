---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chrome DevTools Protocol Setup Report
translated: false
type: note
---

Here's the full report, Boss.

---

## 🦞 Chrome DevTools Protocol (CDP) Setup Report

**Date:** 2026-03-22 03:36–03:42 GMT+8
**Host:** `to` — Linux 6.8.0-106-generic (x64)
**OpenClaw:** 2026.3.13 (61d171a)

---

### Status: ✅ Operational

| Component | State |
| --- | --- |
| Browser Profile | `openclaw` (default) |
| Running | **true** |
| Transport | CDP |
| Port | 18800 |
| URL | `http://127.0.0.1:18800` |
| Active Tabs | 1 |
| Snapshot Verified | ✅ (example.com) |

---

### What Was Done

**Step 1 — Attempted snap Chromium (failed)**

`sudo apt-get install chromium` installed `chromium-browser 146.0.7680.80` — but on Ubuntu this is a **snap wrapper**, not a real binary. OpenClaw tried to launch it and hit:

```
Failed to create SingletonLock: Permission denied (13)
Failed to create a ProcessSingleton for your profile directory. Aborting now to avoid profile corruption.
```

**Root cause:** Snap's AppArmor confinement prevents the Chromium process from writing to `~/.openclaw/browser/openclaw/user-data/`. Adding `noSandbox: true` did not help because the issue is at the snap/system level, not Chrome's renderer sandbox.

**Step 2 — Used Playwright's bundled Chromium (success)**

Playwright 1.58.2 was already installed globally, and it had downloaded Chromium to `~/.cache/ms-playwright/chromium-1208/`. This binary is **not** snap-sandboxed and works fine with CDP.

**Step 3 — Configured OpenClaw**

Set `executablePath` to the Playwright Chromium and started the browser.

---

### Configuration Added

File: `~/.openclaw/openclaw.json`

```json
"browser": {
  "enabled": true,
  "noSandbox": true,
  "headless": true,
  "executablePath": "/home/lzw/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome"
}
```

---

### Browser Inventory

| Binary | Version | Source | CDP Compatible |
| --- | --- | --- | --- |
| `/usr/bin/chromium-browser` | 146.0.7680.80 | snap | ❌ (AppArmor blocks it) |
| `~/.cache/ms-playwright/.../chrome` | 145.0.7632.6 | Playwright 1.58.2 | ✅ **(active)** |

---

### Active Browser Profiles

| Profile | Status | Notes |
| --- | --- | --- |
| `openclaw` | ✅ running (1 tab) | Managed headless, CDP on :18800 |
| `user` | ⬜ stopped | Existing-session mode (requires `--browser-profile user`) |
| `chrome-relay` | ✅ running (0 tabs) | Extension relay on :18792 |

---

### Available Capabilities

All verified and working:

- `openclaw browser navigate <url>` — page navigation
- `openclaw browser snapshot --compact` — DOM tree snapshot with element refs
- `openclaw browser screenshot` — full-page or element screenshots
- `openclaw browser click <ref>` — click elements by ref
- `openclaw browser type <ref> <text>` — fill form fields
- `openclaw browser evaluate <fn>` — run JS in page context
- `openclaw browser console` — read console logs
- `openclaw browser requests` — monitor network traffic
- `openclaw browser pdf` — save pages as PDF
- `openclaw browser cookies` — read/write cookies

---

### ⚠️ Notes

1. **Playwright Chromium version lags behind snap** (145 vs 146) — minor, doesn't affect CDP functionality
2. **Playwright updates may change the binary path** (e.g., `chromium-1208` → `chromium-1300`). If the browser breaks after a `npx playwright install` upgrade, update `executablePath` in config
3. **`headless: true`** means no visible browser window — all interaction is via CLI/agent commands. Set `false` if you want to see it (requires display)
4. **The Telegram group policy warning** in doctor output is unrelated — that's about Telegram channel config, not browser

---

### Alternative: Install Google Chrome Stable

If you want a more permanent solution that survives Playwright upgrades:

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y
```

Then set `executablePath` to `/usr/bin/google-chrome-stable`. That's the officially recommended path per OpenClaw docs.

---

Anything else you want me to test or configure?
