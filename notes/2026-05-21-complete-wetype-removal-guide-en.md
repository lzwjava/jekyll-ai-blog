---
audio: false
generated: true
image: false
lang: en
layout: post
title: Complete WeType Removal Guide
translated: false
type: note
---

## WeType Uninstall — Complete Report

### What was removed (11 locations)

| # | Target | Method | Status |
|---|---|---|---|
| 1 | `/Library/Input Methods/WeType.app` (input method bundle) | `sudo rm -rf` | Removed |
| 2 | Launch agent at `~/Library/LaunchAgents/` | `launchctl bootout` + `launchctl remove` | Unloaded + deregistered |
| 3 | Running process (PID 9753) | `kill` + `launchctl remove` | Terminated |
| 4 | `~/Library/Preferences/com.tencent.inputmethod.wetype*` | `rm` | Cleaned |
| 5 | `~/Library/Preferences/com.tencent.WeTypeSettings.plist` | `rm` | Cleaned |
| 6 | `~/Library/Caches/com.tencent.inputmethod.wetype*` | `rm -rf` | Cleaned |
| 7 | `~/Library/Caches/com.tencent.wetype.InstallerApp` | `rm -rf` | Cleaned |
| 8 | `~/Library/Caches/SentryCrash/WeType` | `rm -rf` | Cleaned |
| 9 | `~/Library/Application Support/WeType*` | `rm -rf` | Cleaned |
| 10 | `~/Library/HTTPStorages/com.tencent.wetype.*` | `rm -rf` | Cleaned |
| 11 | `~/Library/WebKit/com.tencent.inputmethod.wetype` | `rm -rf` | Cleaned |
| 12 | `/Library/Logs/DiagnosticReports/WeType_*.diag` | `sudo rm` | Cleaned |

### What you gained

| Metric | Before | After |
|---|---|---|
| RAM used by WeType | **~1,614 MB** | **0 MB** |
| Processes | 1 running + launch agent | 0 |
| Launchd registrations | 1 active | 0 |
| Startup auto-load | Yes (on login) | Gone |

### What you need to do next

Since WeType is gone, you'll need another Chinese input method. Apple's built-in Pinyin uses <100 MB vs WeType's 1.6 GB:

1. Open **System Settings > Keyboard > Input Sources**
2. Click **+** > **Chinese** > **Pinyin - Simplified**
3. Switch between input methods with `Control`+`Space` or `Globe` key

If you later decide you prefer WeType back, it can be downloaded from the official site — but I'd recommend giving Apple Pinyin a try first at 1/16th the memory cost.
