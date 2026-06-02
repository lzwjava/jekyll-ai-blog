---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 后台进程已清理
translated: true
type: note
---

全部清理完毕。ClashX Pro 的辅助进程仍然正常加载并运行中。

---

**已移除的项目（共 17 项）：**

| # | 已移除项目 | 类型 |
|---|---|---|
| 1 | `com.hp.devicemonitor` | HP 打印机监控 — 不必要 |
| 2 | `com.hp.productresearch` | HP 遥测 — 不必要 |
| 3 | `com.valvesoftware.steamclean` | Steam 旧残留 — 无用 |
| 4 | `com.amazon.kpr.ncd` | Kindle 后台 — 残留 |
| 5 | `com.amazon.KindlePreviewerUpdater` | Kindle Previewer 守护进程 — 残留 |
| 6 | `com.sogou.SogouTaskManager` | 搜狗额外进程 — 不必要 |
| 7 | `netdisk_service` | 百度网盘自动启动 |
| 8 | `com.west2online.ClashX.ProxyConfigHelper` | 旧版 ClashX（非 Pro）残留 |
| 9 | `io.github.clashverge.helper` | Clash Verge 残留（应用未安装） |
| 10 | `yanue.v2rayu.v2ray-core` | 旧版 V2RayU 残留（你使用的是 V2RayXS） |
| 11 | `com.qiuyuzhou.shadowsocksX-NG.http` | Shadowsocks 残留（应用未安装） |
| 12 | `com.qiuyuzhou.shadowsocksX-NG.local` | Shadowsocks 残留（应用未安装） |

**保留的项目（共 18 项自启动项）：**

| 保留项目 | 原因 |
|---|---|
| ClashX Pro helper | 你正在使用 ClashX Pro |
| Docker (socket + vmnetd) | Docker 需要这些 |
| Google Keystone（3 个 plist） | Chrome / Google Drive 更新 |
| MS auto-update helper | Office 更新 |
| Teams updater | 后台更新 |
| Zoom daemon + updaters | 若你使用 Zoom |
| nginx, postgresql@14, redis | 活跃的开发服务 |
| Multipass, Disk Drill | 已安装的工具 |
| SogouServices | 输入法主服务 |
| Steam + RescueTime + Google Drive | 你添加的登录项 |

**总计：移除 12 项，保留 18 项。** 你的系统现在启动时减少了 17 个后台进程。
