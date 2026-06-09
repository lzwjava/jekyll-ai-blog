---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS 时钟闹钟通过快捷指令
translated: true
type: note
---

以下是完整的调查摘要：

## 发生了什么

**macOS 26 的 Clock.app 不会从 plist 或 SQLite 数据库中读取闹钟。** `mobiletimerd` 守护进程将所有闹钟保存在内存中，并通过 XPC 在 `com.apple.MobileTimer.alarmserver` 上暴露。Clock.app 只与该守护进程通信——从不直接访问相关文件。

## 不生效的方法（均已测试）

1. **写入 plist**（`~/Library/Preferences/com.apple.mobiletimerd.plist`）——守护进程忽略。Clock.app 显示“无闹钟”。

2. **写入 SQLite**（`group.com.apple.mobiletimerd/local.sqlite`）——守护进程忽略。结果相同。

3. **pyobjc 的 MTAlarmManager.addAlarm_()**——XPC 连接被拒绝：`"not entitled"`。只有拥有 `com.apple.private.mobiletimerd.alarmserver` 授权的 Apple 签名应用才能与守护进程通信。

4. **编译后的 Swift 二进制文件**——同样出现 `"not entitled"` 错误。没有 Apple 的私有授权，代码签名也无济于事。

## 有效的方法

**Shortcuts.app** 拥有正确的授权。用户已经有一个 `中国法定节假日闹钟` 快捷指令，可以创建闹钟。`shortcuts run` 可以正常工作。

## 修复方案

`_set_alarm` 函数需要使用 **Shortcuts.app** 作为桥梁。方法如下：

1. 在 Shortcuts.app 中创建一个可复用的快捷指令（例如 `"ww-create-alarm"`），该快捷指令接收 `hour`、`minute` 和 `label` 作为输入，并使用 `MTCreateAlarm` 意图操作创建 Clock.app 闹钟。

2. 在 `_set_alarm` 中调用 `shortcuts run "ww-create-alarm" --input-path <args>`。

该快捷指令需要通过 Shortcuts.app 的图形界面创建一次（我们可以指导用户），或者我们可以通过编程方式创建 `.shortcut` 文件并导入。`shortcuts` 命令行工具支持 `sign` 但不支持 `import`，因此首次创建快捷指令需要手动完成一次。

**需要我继续创建快捷指令并更新 `alarm.py` 吗？**