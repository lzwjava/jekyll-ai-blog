---
audio: false
generated: true
image: false
lang: en
layout: post
title: Node.js Bot Framework Troubleshooting Guide
translated: false
type: note
---

## Summary

### openclaw

**What it is**: A Node.js-based multi-channel bot agent framework (similar to Hermes Agent), installed globally.

| Field | Detail |
| --- | --- |
| Package | `openclaw@2026.5.12` — global npm install |
| Binary | `/home/lzw/.npm-global/bin/openclaw` |
| Install | `/home/lzw/.npm-global/lib/node_modules/openclaw/` |
| Config dir | `~/.openclaw/` (home directory, `~512KB total`) |
| Config file | `~/.openclaw/openclaw.json` |
| Workspace | `~/.openclaw/workspace/` (28 dirs) |
| Channels | Telegram (default), Nextcloud Talk, WhatsApp, WeChat (`openclaw-weixin`) |
| Extensions | `@openclaw/nextcloud-talk`, `@tencent-weixin/openclaw-weixin` |
| Runtime | Node.js v25.8.1 |

**Status**: The Telegram channel is in a crash-loop. Logs at `/tmp/openclaw/openclaw-2026-07-09.log` (~3.5MB) show:

- `fetch timeout` — `getMe` to `api.telegram.org` timing out at 10s repeatedly
- `UND_ERR_CONNECT_TIMEOUT` — DNS resolves but IP unreachable
- Auto-restart attempts (1/10, 2/10, ...) keep failing
- Transport backoff: 10s → 20s → 40s unhealthy mark window
- No successful connection in the last 24h of logs

**Root cause**: Likely a proxy/firewall blocking Telegram API on this machine. The bot token is present but can't reach Telegram's servers to poll/getUpdates.

**Also referenced in your config**:

- `~/ww/ww/config/openclaw.json` — your `ww` tool has an embedded openclaw config pointing to the same workspace
- `~/projects/config/openclaw/openclaw.json` — another config variant

---

### myopia-reversal-app

**Location**: `/home/lzw/.openclaw/workspace/myopia-reversal-app/`

**Type**: Single-page web app (HTML/CSS/JS), no framework/build step — just `index.html` + Vite devDependency (unused for production)

**Purpose**: A calculator that recommends "near-vision" prescription from full far-vision specs — typically **-1.50D reduction** (150 degrees in Asian format). Based on the active myopia reversal / eyeball-shortening theory.

**Features** (all client-side JS):

- Input left/right eye far-vision prescription (sphere + cylinder)
- Output recommended near-vision prescription
- Unit toggle: Asian (degrees) vs Western (Diopters)
- Language: English / Chinese (bilingual toggle)
- Dark/light theme toggle
- Recovery tips section

**Files**:

```
myopia-reversal-app/
  index.html         (14KB, 345 lines — all UI + logic inline)
  README.md          (English)
  README_CN.md       (Chinese)
  package.json       (Vite dev dep only)
  package-lock.json
  node_modules/
  .git/              (1 commit, Mar 14)
```

**Git**: Single branch `master`, one commit from Mar 14. No remote configured (local-only).

---

### nginx setup

**Config**: `/etc/nginx/conf.d/default.conf` — single server block on port 80

**Routes**:

| Path | Target | Type |
| --- | --- | --- |
| `/` | `/var/www/html/` | Static files |
| `/todo/` | `/var/www/html/todo/` | Static files |
| `/myopia/` | `/home/lzw/.openclaw/workspace/myopia-reversal-app/` | **Just added** |
| `/movies/` | `/home/lzw/qDownloads/` | Directory listing |

**Other**: `/etc/nginx/conf.d/pincc-proxy.conf` — reverse proxy on port 8742 → `v2-as.pincc.ai` (Claude Code API proxy with hardcoded auth token `sk-8a2...ea7f` and spoofed client headers)

**Status**: `nginx -t` passed, reloaded successfully, `curl http://localhost/myopia/` → 200

**To open in browser**: `http://<workstation-ip>/myopia/` or `http://localhost/myopia/` if on the workstation.
