---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacOS Startup Audit Overview
translated: false
type: note
---

Here's the **complete auto-start audit** of your system — 6 categories, 35 items total.

---

## 1. macOS Login Items (System Settings)

Launched when you log into the GUI. Managed via System Settings > General > Login Items.

```
Steam        | /Applications/Steam.app
RescueTime   | (missing path — legacy item)
Google Drive | /Applications/Google Drive.app
```

- **Steam** — starts Steam client at boot. If you don't game daily, can be disabled.
- **RescueTime** — productivity tracker. Needs to run if you use it.
- **Google Drive** — cloud sync. Keep if you use it.

---

## 2. Launch Daemons (root-level, run as system)

Auto-start at boot for all users. Located in `/Library/LaunchDaemons/`.

| Plist | What | Safe to remove? |
|---|---|---|
| `com.amazon.KindlePreviewerUpdater.plist` | Kindle Previewer updates | **Yes** — only if you don't use Kindle Previewer |
| `com.canonical.multipassd.plist` | Multipass (Ubuntu VMs) | ✓ Keep if you use Multipass |
| `com.cleverfiles.cfbackd.plist` | Disk Drill backup daemon | **Maybe** — only if you use Disk Drill |
| `com.docker.socket.plist` | Docker | ✓ Keep if you use Docker |
| `com.docker.vmnetd.plist` | Docker networking | ✓ Keep if you use Docker |
| `com.microsoft.autoupdate.helper.plist` | MS Office auto-updater | ✓ Keep if you use Office |
| `com.microsoft.teams.TeamsUpdaterDaemon.plist` | Teams background updater | **Yes** — if you don't use Teams often |
| `com.west2online.ClashX.ProxyConfigHelper.plist` | ClashX proxy helper | **Maybe** — you have 3 proxy tools |
| `com.west2online.ClashXPro.ProxyConfigHelper.plist` | ClashX Pro proxy helper | **Maybe** — you have 3 proxy tools |
| `io.github.clashverge.helper.plist` | Clash Verge proxy helper | **Maybe** — you have 3 proxy tools |
| `us.zoom.ZoomDaemon.plist` | Zoom background service | **Maybe** — only if you use Zoom often |

---

## 3. User Launch Agents (your user, GUI context)

Auto-start when *you* log in. Located in `~/Library/LaunchAgents/`.

| Plist | What | Safe to remove? |
|---|---|---|
| `com.amazon.kpr.ncd.plist` | Amazon Kindle related | **Yes** — if you don't use Kindle |
| `com.google.GoogleUpdater.wake.plist` | Google updater wake trigger | Keep — Chrome/Google updates |
| `com.google.keystone.agent.plist` | Google Keystone (update infra) | Keep — Chrome/Google Drive updates |
| `com.google.keystone.xpcservice.plist` | Google Keystone helper | Keep — paired with above |
| `com.hp.devicemonitor.plist` | HP printer status monitor | **Yes** — if no HP printer |
| `com.hp.productresearch.plist` | HP telemetry/usage data | **Yes** — telemetry, unnecessary |
| `com.qiuyuzhou.shadowsocksX-NG.http.plist` | ShadowsocksX-NG proxy (HTTP) | **Maybe** — you have 3 proxy tools |
| `com.qiuyuzhou.shadowsocksX-NG.local.plist` | ShadowsocksX-NG proxy (local) | **Maybe** — you have 3 proxy tools |
| `com.valvesoftware.steamclean.plist` | Steam cleanup background task | **Yes** — Steam removed this feature, orphaned |
| `homebrew.mxcl.nginx.plist` | Nginx (started) | Keep — actively running |
| `homebrew.mxcl.postgresql@14.plist` | PostgreSQL 14 (started) | Keep — actively running |
| `homebrew.mxcl.redis.plist` | Redis (started) | Keep — actively running |
| `netdisk_service.plist` | Baidu Netdisk background service | **Yes** — if you don't use 百度网盘 daily |
| `yanue.v2rayu.v2ray-core.plist` | V2RayU proxy core | **Maybe** — you have 3 proxy tools |

---

## 4. System Launch Agents (all users)

Located in `/Library/LaunchAgents/`.

| Plist | What | Safe to remove? |
|---|---|---|
| `com.google.keystone.agent.plist` | Google Keystone (system-wide) | Keep — needed for Chrome |
| `com.google.keystone.xpcservice.plist` | Google Keystone helper | Keep |
| `com.microsoft.update.agent.plist` | Microsoft update agent | Keep — Office updates |
| `com.sogou.SogouServices.plist` | Sogou input method services | Keep — if you use Sogou input |
| `com.sogou.SogouTaskManager.plist` | Sogou task manager | **Yes** — unnecessary extra process |
| `us.zoom.updater.login.check.plist` | Zoom update check at login | **Maybe** |
| `us.zoom.updater.plist` | Zoom updater | Keep if you use Zoom |

---

## 5. Brew Services (running now)

```
nginx        (started)
postgresql@14 (started)
redis         (started)
```

All three are **actively running** and are standard dev tools. Keep unless you don't need them auto-started.

---

## 6. Cron Jobs & Legacy

| Source | Status |
|---|---|
| crontab | Empty |
| `/Library/StartupItems/` | Empty |
| `/System/Library/StartupItems/` | Empty |
| `~/.zshrc` (auto-start commands) | None found |

---

### Recommended cleanup list

**Highest-value removals** (no downside, these are likely unused or redundant):

| Item | Reason |
|---|---|
| `com.hp.devicemonitor` + `com.hp.productresearch` | Unless you have an HP printer |
| `com.valvesoftware.steamclean` | Orphaned — Steam removed this feature years ago |
| `com.amazon.kpr.ncd` + `KindlePreviewerUpdater` | If you don't use Kindle Previewer |
| `com.sogou.SogouTaskManager` | Extra Sogou process, the main one handles everything |
| `netdisk_service` | If you don't need Baidu Netdisk auto-starting |
| 4 out of 5 proxy tools | **ClashX** + **ClashXPro** + **Clash Verge** + **ShadowsocksX-NG** + **V2RayU** — that's 5 proxy tools. You almost certainly use just one. The other 4 are wasting background resources |

Want me to remove any of these?
