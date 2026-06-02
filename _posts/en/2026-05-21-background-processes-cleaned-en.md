---
audio: false
generated: true
image: false
lang: en
layout: post
title: Background Processes Cleaned
translated: false
type: note
---

All clean. ClashX Pro's helper is still properly loaded and active.

---

**What was removed (17 items total):**

| # | Removed Item | Type |
|---|---|---|
| 1 | `com.hp.devicemonitor` | HP printer monitor — unnecessary |
| 2 | `com.hp.productresearch` | HP telemetry — unnecessary |
| 3 | `com.valvesoftware.steamclean` | Steam old orphan — useless |
| 4 | `com.amazon.kpr.ncd` | Kindle background — orphan |
| 5 | `com.amazon.KindlePreviewerUpdater` | Kindle Previewer daemon — orphan |
| 6 | `com.sogou.SogouTaskManager` | Sogou extra process — unnecessary |
| 7 | `netdisk_service` | Baidu Netdisk auto-start |
| 8 | `com.west2online.ClashX.ProxyConfigHelper` | Old ClashX (non-Pro) orphan |
| 9 | `io.github.clashverge.helper` | Clash Verge orphan (app not installed) |
| 10 | `yanue.v2rayu.v2ray-core` | Old V2RayU orphan (you use V2RayXS) |
| 11 | `com.qiuyuzhou.shadowsocksX-NG.http` | Shadowsocks orphan (app not installed) |
| 12 | `com.qiuyuzhou.shadowsocksX-NG.local` | Shadowsocks orphan (app not installed) |

**Kept (18 remaining auto-start items):**

| Kept Item | Reason |
|---|---|
| ClashX Pro helper | You actively use ClashX Pro |
| Docker (socket + vmnetd) | Docker needs these |
| Google Keystone (3 plists) | Chrome / Google Drive updates |
| MS auto-update helper | Office updates |
| Teams updater | Background updates |
| Zoom daemon + updaters | If you use Zoom |
| nginx, postgresql@14, redis | Active dev services |
| Multipass, Disk Drill | Installed tools |
| SogouServices | Input method main service |
| Steam + RescueTime + Google Drive | Login items you added |

**Total: 12 removed, 18 kept.** Your system now has 17 fewer background processes starting at boot.
