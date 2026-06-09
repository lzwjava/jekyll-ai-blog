---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 闹钟SQLite缓存修复
translated: true
type: note
---

问题：为什么即使直接写入 SQLite 数据库并确认数据存在于表中，Clock.app 中的闹钟仍然不显示或不起作用？

答案：

即使你的脚本正确地将数据插入到 `local.sqlite` 中，**Clock.app 仍然不会显示闹钟，因为它依赖于由后台守护进程（`mobiletimerd`）管理的内存缓存 Core Data 堆栈。** 当你绕过 Core Data 直接修改 SQLite 文件时，系统守护进程完全不知道这些更改。它继续使用其内存中的状态，并最终会用其自己的缓存覆盖你手动写入的 SQLite 条目。

要使更改生效并同步到 Clock 应用界面，你需要通知系统或清除守护进程缓存，具体步骤如下：

### 1. 通知系统或强制守护进程重载

仅仅使用 `pgrep` 检查是不够的；你必须强制 `mobiletimerd` 刷新其缓存并从磁盘重新读取数据库。你可以安全地终止后台进程，使其重新启动：

```bash
killall mobiletimerd

```

或者，由于 macOS 上的 Core Data 通常通过 `notifyd` 依赖跨进程通知，如果基本进程重启无法强制同步，你可能需要使用 `notifyutil` 广播状态更改通知：

```bash
notifyutil -p com.apple.mobiletimerd.LocalAlarmChanged

```

### 2. 处理 Core Data 的预写日志（WAL）

Core Data 以 `WAL`（预写日志）模式操作 SQLite。当你的脚本写入 `local.sqlite` 时，数据可能只存在于 `local.sqlite-wal` 中，而在 `mobiletimerd` 再次读取之前没有完全检查点写入主数据库文件。

确保你的 Python 执行强制检查点或干净关闭连接，并在脚本完全执行完毕*之后*重启守护进程。

### 3. 验证 Core Data 的 `Z_PRIMARYKEY` 自增值

如果你在插入 `ZMTCDALARM` 和 `ZMTCDSOUND` 时手动分配了 `Z_PK` 值，则**必须**更新 `Z_PRIMARYKEY` 元数据表中 `MTCDAlarm` 和 `MTCDSound` 的 `Z_MAX` 列。

如果 `Z_MAX` 不匹配或未超过你新的 `Z_PK`，Core Data 在下一次通过界面创建闹钟时将会遇到主键冲突，这将静默失败或导致数据库加载崩溃。

```sql
UPDATE Z_PRIMARYKEY SET Z_MAX = (SELECT MAX(Z_PK) FROM ZMTCDALARM) WHERE Z_NAME = 'MTCDAlarm';
UPDATE Z_PRIMARYKEY SET Z_MAX = (SELECT MAX(Z_PK) FROM ZMTCDSOUND) WHERE Z_NAME = 'MTCDSound';

```