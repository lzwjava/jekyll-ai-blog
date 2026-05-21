---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 完整WeType卸载指南
translated: true
type: note
---

## WeType 卸载 — 完整报告

### 已移除的内容（共 11 处）

| # | 目标位置 | 操作方式 | 状态 |
|---|---|---|---|
| 1 | `/Library/Input Methods/WeType.app`（输入法程序包） | `sudo rm -rf` | 已移除 |
| 2 | 启动代理位于 `~/Library/LaunchAgents/` | `launchctl bootout` + `launchctl remove` | 已卸载并注销 |
| 3 | 运行中的进程（PID 9753） | `kill` + `launchctl remove` | 已终止 |
| 4 | `~/Library/Preferences/com.tencent.inputmethod.wetype*` | `rm` | 已清理 |
| 5 | `~/Library/Preferences/com.tencent.WeTypeSettings.plist` | `rm` | 已清理 |
| 6 | `~/Library/Caches/com.tencent.inputmethod.wetype*` | `rm -rf` | 已清理 |
| 7 | `~/Library/Caches/com.tencent.wetype.InstallerApp` | `rm -rf` | 已清理 |
| 8 | `~/Library/Caches/SentryCrash/WeType` | `rm -rf` | 已清理 |
| 9 | `~/Library/Application Support/WeType*` | `rm -rf` | 已清理 |
| 10 | `~/Library/HTTPStorages/com.tencent.wetype.*` | `rm -rf` | 已清理 |
| 11 | `~/Library/WebKit/com.tencent.inputmethod.wetype` | `rm -rf` | 已清理 |
| 12 | `/Library/Logs/DiagnosticReports/WeType_*.diag` | `sudo rm` | 已清理 |

### 您获得的收益

| 指标 | 卸载前 | 卸载后 |
|---|---|---|
| WeType 占用的 RAM | **约 1,614 MB** | **0 MB** |
| 进程数 | 1 个运行中 + 启动代理 | 0 |
| launchd 注册项 | 1 个活跃 | 0 |
| 开机自启 | 是（登录时） | 已清除 |

### 您接下来需要做的

由于 WeType 已移除，您需要另一种中文输入法。苹果自带拼音输入法仅占用不到 100 MB，而 WeType 则占用 1.6 GB：

1. 打开 **系统设置 > 键盘 > 输入法**
2. 点击 **+** > **中文** > **拼音 - 简体**
3. 使用 `Control`+`空格` 或 `地球仪` 键切换输入法

如果您日后决定重新使用 WeType，可从官方网站下载——但我建议您先试试苹果拼音输入法，其内存消耗仅为原来的十六分之一。