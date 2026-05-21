---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Parblo数位板取证卸载完整版
translated: true
type: note
---

完成。全面取证扫描——**系统中已无任何 Parblo 痕迹**。

---

**彻底卸载报告**

| 扫描位置 | 状态 |
|---|---|
| `/Applications/ParbloTablet`（应用包 + 驱动程序） | 已移除 |
| `/Library/LaunchAgents/com.parblo.Tablet.plist` | 已移除 |
| `~/Library/LaunchAgents/` | 干净 |
| `/Library/LaunchDaemons/`（系统级自启动） | 干净 |
| `com.parblo.Tablet` launchd 服务（加载状态） | 已卸载 |
| `com.parblo.pkg.Tablet`（pkg 收据） | 已遗忘 |
| `/private/var/db/receipts/`（pkg 收据文件） | 干净 |
| `~/Library/Preferences/` | 干净 |
| `~/Library/Caches/` | 干净 |
| `~/Library/Application Support/` | 干净 |
| `~/Library/Containers/` | 干净 |
| `~/Library/Group Containers/` | 干净 |
| `~/Library/Saved Application State/` | 干净 |
| macOS 登录项（系统设置） | 干净 |
| 废纸篓 | 干净 |
| 运行中的 Parblo 进程 | 无 |
| 内核扩展（kext） | 无 |
| 系统扩展 | 无 |
| 网络监听/开放端口 | 无 |

**16 项检查全部通过。** Parblo Tablet 已完全卸载——无启动项、无后台进程、无配置文件、无系统挂钩、无软件包收据残留。