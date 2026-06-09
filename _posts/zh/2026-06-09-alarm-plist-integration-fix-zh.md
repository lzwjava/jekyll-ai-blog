---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Alarm plist 集成修复
translated: true
type: note
---

已完成。以下是错误之处及修复内容：

**问题：** `_set_alarm()` 只是启动了一个后台进程（`sleep` + `osascript notification`）并打开了 `clock-alarm://`。它实际上从未向 Clock.app 的 plist 写入任何内容——因此 Clock.app 中没有出现闹钟。

**修复：** 重写 `_set_alarm()` 以实现：

1. 构建一个符合 `mobiletimerd` plist 精确格式的闹钟字典（从你现有的闹钟中逆向工程得出）
2. 读取 plist，将新闹钟追加到 `MTAlarms.MTAlarms` 中
3. 使用 `plistlib.dump` 写回
4. 执行 `killall mobiletimerd`，以便 Clock.app 在重启时能识别到变更

测试结果：

```
$ ww alarm 10 "clothes"
Alarm set for 23:46 (in 10m00s)  label: "clothes"

$ ww alarm list
Found 6 alarm(s) (plist):
  01:50  clothes  [off]
  02:10  (no label)  [off]
  13:32  eat  [off]
  23:30  clothes  [off]
  23:50  clothes  [off]
  23:46  clothes  [on]    ← 新闹钟，已启用
```

该闹钟现在会显示在 Clock.app 中。打开它进行验证——你应该能看到 23:46 的 "clothes" 闹钟已开启。
