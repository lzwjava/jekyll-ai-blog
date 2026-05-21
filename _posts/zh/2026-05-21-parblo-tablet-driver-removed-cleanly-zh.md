---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Parblo平板驱动已干净移除
translated: true
type: note
---

一切已清理完毕。以下是最终总结：

| 项目 | 状态 |
|------|------|
| `/Applications/ParbloTablet` | 已移除 |
| `/Library/LaunchAgents/com.parblo.Tablet.plist` | 已移除 |
| `com.parblo.Tablet` launchd 服务 | 已卸载 |
| `com.parblo.pkg.Tablet` 安装记录 | 已遗忘 |
| ~/Library/Preferences/ | 已清理 |
| ~/Library/Caches/ | 已清理 |
| ~/Library/Saved Application State/ | 已清理 |
| 任何正在运行的 Parblo 进程 | 无 |

Parblo Tablet Driver 已**彻底从系统中移除**。无开机启动项、无进程、无残留文件。