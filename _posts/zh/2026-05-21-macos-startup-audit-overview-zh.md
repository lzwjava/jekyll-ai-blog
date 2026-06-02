---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MacOS 启动审计概述
translated: true
type: note
---

以下是您系统的**完整自启动审核** —— 6 个类别，共 35 项。

---

## 1. macOS 登录项（系统设置）

在您登录 GUI 时启动。通过系统设置 > 通用 > 登录项管理。

```
Steam        | /Applications/Steam.app
RescueTime   | (路径缺失 — 旧版登录项)
Google Drive | /Applications/Google Drive.app
```

- **Steam** — 启动时启动 Steam 客户端。如果不每天玩游戏，可禁用。
- **RescueTime** — 生产力追踪器。如果使用则需要运行。
- **Google Drive** — 云同步。如果使用则保留。

---

## 2. Launch Daemons（root 级别，作为系统运行）

启动时对所有用户自启动。位于 `/Library/LaunchDaemons/`。

| Plist | 说明 | 可安全移除？ |
|---|---|---|
| `com.amazon.KindlePreviewerUpdater.plist` | Kindle Previewer 更新 | **是** — 仅当您不使用 Kindle Previewer 时 |
| `com.canonical.multipassd.plist` | Multipass（Ubuntu 虚拟机） | ✓ 如果使用 Multipass 则保留 |
| `com.cleverfiles.cfbackd.plist` | Disk Drill 备份守护进程 | **可能** — 仅当您使用 Disk Drill 时 |
| `com.docker.socket.plist` | Docker | ✓ 如果使用 Docker 则保留 |
| `com.docker.vmnetd.plist` | Docker 网络 | ✓ 如果使用 Docker 则保留 |
| `com.microsoft.autoupdate.helper.plist` | Microsoft Office 自动更新器 | ✓ 如果使用 Office 则保留 |
| `com.microsoft.teams.TeamsUpdaterDaemon.plist` | Teams 后台更新器 | **是** — 如果您不经常使用 Teams |
| `com.west2online.ClashX.ProxyConfigHelper.plist` | ClashX 代理助手 | **可能** — 您有 3 个代理工具 |
| `com.west2online.ClashXPro.ProxyConfigHelper.plist` | ClashX Pro 代理助手 | **可能** — 您有 3 个代理工具 |
| `io.github.clashverge.helper.plist` | Clash Verge 代理助手 | **可能** — 您有 3 个代理工具 |
| `us.zoom.ZoomDaemon.plist` | Zoom 后台服务 | **可能** — 仅当您经常使用 Zoom 时 |

---

## 3. User Launch Agents（您的用户，GUI 上下文）

在*您*登录时自启动。位于 `~/Library/LaunchAgents/`。

| Plist | 说明 | 可安全移除？ |
|---|---|---|
| `com.amazon.kpr.ncd.plist` | Amazon Kindle 相关 | **是** — 如果您不使用 Kindle |
| `com.google.GoogleUpdater.wake.plist` | Google 更新器唤醒触发器 | 保留 — Chrome/Google 更新 |
| `com.google.keystone.agent.plist` | Google Keystone（更新基础设施） | 保留 — Chrome/Google Drive 更新 |
| `com.google.keystone.xpcservice.plist` | Google Keystone 助手 | 保留 — 与上者配对 |
| `com.hp.devicemonitor.plist` | HP 打印机状态监视器 | **是** — 如果没有 HP 打印机 |
| `com.hp.productresearch.plist` | HP 遥测/使用数据 | **是** — 遥测，非必要 |
| `com.qiuyuzhou.shadowsocksX-NG.http.plist` | ShadowsocksX-NG 代理（HTTP） | **可能** — 您有 3 个代理工具 |
| `com.qiuyuzhou.shadowsocksX-NG.local.plist` | ShadowsocksX-NG 代理（本地） | **可能** — 您有 3 个代理工具 |
| `com.valvesoftware.steamclean.plist` | Steam 清理后台任务 | **是** — Steam 已移除该功能，已孤立 |
| `homebrew.mxcl.nginx.plist` | Nginx（已启动） | 保留 — 正在运行 |
| `homebrew.mxcl.postgresql@14.plist` | PostgreSQL 14（已启动） | 保留 — 正在运行 |
| `homebrew.mxcl.redis.plist` | Redis（已启动） | 保留 — 正在运行 |
| `netdisk_service.plist` | 百度网盘后台服务 | **是** — 如果您不每天使用百度网盘 |
| `yanue.v2rayu.v2ray-core.plist` | V2RayU 代理核心 | **可能** — 您有 3 个代理工具 |

---

## 4. System Launch Agents（所有用户）

位于 `/Library/LaunchAgents/`。

| Plist | 说明 | 可安全移除？ |
|---|---|---|
| `com.google.keystone.agent.plist` | Google Keystone（系统级） | 保留 — Chrome 需要 |
| `com.google.keystone.xpcservice.plist` | Google Keystone 助手 | 保留 |
| `com.microsoft.update.agent.plist` | Microsoft 更新代理 | 保留 — Office 更新 |
| `com.sogou.SogouServices.plist` | 搜狗输入法服务 | 保留 — 如果使用搜狗输入法 |
| `com.sogou.SogouTaskManager.plist` | 搜狗任务管理器 | **是** — 不必要的额外进程 |
| `us.zoom.updater.login.check.plist` | Zoom 登录时更新检查 | **可能** |
| `us.zoom.updater.plist` | Zoom 更新器 | 如果使用 Zoom 则保留 |

---

## 5. Brew Services（当前正在运行）

```
nginx        (started)
postgresql@14 (started)
redis         (started)
```

三个服务**均正在运行**，是标准开发工具。除非不需要它们自启动，否则请保留。

---

## 6. Cron 作业与旧版

| 来源 | 状态 |
|---|---|
| crontab | 空 |
| `/Library/StartupItems/` | 空 |
| `/System/Library/StartupItems/` | 空 |
| `~/.zshrc`（自启动命令） | 未发现 |

---

### 推荐的清理列表

**最高价值移除项**（无副作用，很可能未使用或冗余）：

| 项目 | 原因 |
|---|---|
| `com.hp.devicemonitor` + `com.hp.productresearch` | 除非您有 HP 打印机 |
| `com.valvesoftware.steamclean` | 已孤立 — Steam 多年前已移除该功能 |
| `com.amazon.kpr.ncd` + `KindlePreviewerUpdater` | 如果您不使用 Kindle Previewer |
| `com.sogou.SogouTaskManager` | 额外的搜狗进程，主进程已处理所有功能 |
| `netdisk_service` | 如果您不需要百度网盘自启动 |
| 5 个代理工具中的 4 个 | **ClashX** + **ClashXPro** + **Clash Verge** + **ShadowsocksX-NG** + **V2RayU** — 共有 5 个代理工具。您几乎肯定只用其中一个。其他 4 个在浪费后台资源 |

需要我帮您移除其中任何一项吗？
