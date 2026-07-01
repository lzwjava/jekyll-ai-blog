---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parblo Tablet Forensic Uninstall Complete
translated: false
type: note
---

Done. Full forensic sweep — **zero traces of Parblo remain on this system**.

---

**Comprehensive Uninstall Report**

| Scan location | Status |
| --- | --- |
| `/Applications/ParbloTablet` (app bundle + driver) | Removed |
| `/Library/LaunchAgents/com.parblo.Tablet.plist` | Removed |
| `~/Library/LaunchAgents/` | Clean |
| `/Library/LaunchDaemons/` (system-level auto-start) | Clean |
| `com.parblo.Tablet` launchd service (loaded state) | Unloaded |
| `com.parblo.pkg.Tablet` (pkg receipt) | Forgotten |
| `/private/var/db/receipts/` (pkg receipt files) | Clean |
| `~/Library/Preferences/` | Clean |
| `~/Library/Caches/` | Clean |
| `~/Library/Application Support/` | Clean |
| `~/Library/Containers/` | Clean |
| `~/Library/Group Containers/` | Clean |
| `~/Library/Saved Application State/` | Clean |
| macOS Login Items (System Settings) | Clean |
| Trash | Clean |
| Running Parblo processes | None |
| Kernel extensions (kext) | None |
| System extensions | None |
| Network listeners / open ports | None |

**16 out of 16 checks clean.** Parblo Tablet is fully uninstalled — no startup items, no background processes, no config files, no system hooks, no package receipt residuals.
