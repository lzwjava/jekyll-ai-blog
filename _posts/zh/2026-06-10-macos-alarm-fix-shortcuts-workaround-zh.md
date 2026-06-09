---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS 闹钟修复：快捷指令解决方案
translated: true
type: note
---

## 摘要

### 根本问题

在 macOS 26 上，Clock.app 的闹钟完全由 `mobiletimerd` 守护进程通过 XPC（`com.apple.MobileTimer.alarmserver`）管理。该守护进程将闹钟保存在内存中。plist 或 SQLite 数据库都不是真实数据源——守护进程本身才是。

**以下方法均无效（已全部测试并确认）：**
1. 写入 `~/Library/Preferences/com.apple.mobiletimerd.plist` —— 守护进程忽略，Clock.app 显示“无闹钟”
2. 写入 `~/Library/Group Containers/group.com.apple.mobiletimerd/local.sqlite` —— 结果相同
3. 通过 pyobjc 调用 `MTAlarmManager.addAlarm_()` —— XPC 拒绝：`"not entitled"`
4. 编译的 Swift 二进制文件调用 MobileTimer 框架 —— 同样出现 `"not entitled"` 错误
5. 通过 `INInteraction` 捐赠 `MTCreateAlarmIntent` —— 捐赠到 Siri 建议中，但不会创建闹钟

这些授权是 Apple 私有的。只有 Apple 签名的进程（Clock.app、Shortcuts.app、Siri）才能与 `mobiletimerd` 通信。

### 可行方法

**Shortcuts.app** 拥有正确的授权，可以创建闹钟。 `shortcuts` CLI 可以运行快捷指令：
```bash
shortcuts run "shortcut-name" --input-path /tmp/input.txt
```

### 已完成的工作

1. **创建并签署了一个 `.shortcut` 文件** —— 发现 `.shortcut` 是纯二进制 plist（不是 ZIP），且 `shortcuts sign` 接受此格式
2. **将 `ww-create-alarm-signed` 导入到 Shortcuts.app** —— 该快捷指令存在但没有任何操作
3. **清理了 `alarm.py`** —— 重写为使用 SQLite（概念上方法正确，但没有守护进程则不足）

### 需要用户执行的操作（一次性手动设置）

用户需要在 Shortcuts.app 中向该快捷指令添加“创建闹钟”操作：

1. 打开 Shortcuts.app → 找到“ww-create-alarm-signed”
2. 点击编辑 → 添加操作 → 搜索“创建闹钟”（来自 Clock app）
3. 配置为接受**快捷指令输入**作为文本（格式：`HH:MM label`）
4. 保存

然后更新 `alarm.py`，使其调用：
```python
subprocess.run(["shortcuts", "run", "ww-create-alarm-signed", "--input-path", tmpfile])
```

**需要我删除这个空快捷指令，创建一个带有正确设置说明的新快捷指令，并更新 `alarm.py` 以使用 `shortcuts run` 方法吗？** 您只需在 Shortcuts.app 中执行一个 2 分钟的手动步骤来添加“创建闹钟”操作即可。