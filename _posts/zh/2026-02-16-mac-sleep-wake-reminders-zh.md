---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mac 休眠唤醒提醒
translated: true
type: note
---

Question: 如何检测 macOS 何时合盖或进入 sleep 模式，以及何时唤醒，以便发送通知提醒自己做某事？

Answer:

在 macOS 上有几种实现这一点的实用方法。对于普通用户来说，最可靠且最常用的方法是 **SleepWatcher**（一个小型 daemon）结合简单的 shell scripts。这种方法非常适合在 Mac **进入 sleep**（通常是当你合盖时）和 **唤醒**（通常是当你开盖或按下按键时）时发送提醒。

### 推荐方案：使用 SleepWatcher（对大多数人最简单）

1. 通过 Homebrew 安装 SleepWatcher（如果你没有 Homebrew → `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`）

   ```bash
   brew install sleepwatcher
   ```

2. 在你的 home folder 中创建两个简单的 scripts：

   ```bash
   # 创建在进入 sleep 时运行的脚本（合盖 → sleep）
   cat > ~/.sleep << 'EOF'
   #!/bin/bash
   osascript -e 'display notification "Lid closed / going to sleep — remember to XXX" with title "Reminder"'
   # 你也可以添加：say "Lid closed, remember to do something"
   EOF

   # 创建在唤醒时运行的脚本
   cat > ~/.wakeup << 'EOF'
   #!/bin/bash
   osascript -e 'display notification "Woke up / lid opened — time to do XXX" with title "Reminder"'
   # 可选：say "Welcome back, don't forget to..."
   EOF
   ```

3. 赋予执行权限：

   ```bash
   chmod +x ~/.sleep ~/.wakeup
   ```

4. 启动 SleepWatcher（稍后可以设置为自动启动）：

   ```bash
   sleepwatcher --verbose \
     --sleep ~/.sleep \
     --wake ~/.wakeup
   ```

   若要永久在后台运行：

   ```bash
   sleepwatcher --sleep ~/.sleep --wake ~/.wakeup &
   ```

   更好的做法：创建一个 launchd plist 以在登录时自动启动（存在许多教程，或者如果 Homebrew 支持，使用 `brew services start sleepwatcher`）。

**结果**：

- 合盖 → Mac sleeps → `~/.sleep` 运行 → 你收到通知
- 开盖 / 唤醒 Mac → `~/.wakeup` 运行 → 你收到通知

### 替代方案 1：纯 AppleScript + launchd（无需额外工具）

创建一个定期检查 sleep 状态的脚本（不够优雅，但无需安装任何东西即可工作）：

```applescript
-- 保存为 ~/Library/Scripts/wake-sleep-notifier.scpt
on idle
    tell application "System Events"
        set currentState to (do shell script "pmset -g | grep -i 'sleep prevented' || true")
        -- 非常粗略 — 最好在文件中跟踪之前的状态
    end tell

    -- 更实用：直接使用上面的 sleepwatcher 方式
    return 60 -- 每分钟检查一次
end idle
```

→ 这种方法不够精确；强烈推荐使用 SleepWatcher。

### 替代方案 2：Swift/App 方式（适用于开发者）

如果你想要一个小的 menu bar app：

使用 `NSWorkspace` notifications（简单且原生）：

```swift
import Cocoa

class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        let center = NSWorkspace.shared.notificationCenter

        center.addObserver(forName: NSWorkspace.willSleepNotification, object: nil, queue: .main) { _ in
            let notif = NSUserNotification()
            notif.title = "Going to Sleep"
            notif.informativeText = "Lid closed — remember to ..."
            NSUserNotificationCenter.default.deliver(notif)
        }

        center.addObserver(forName: NSWorkspace.didWakeNotification, object: nil, queue: .main) { _ in
            let notif = NSUserNotification()
            notif.title = "Woke Up"
            notif.informativeText = "Lid open — time to ..."
            NSUserNotificationCenter.default.deliver(notif)
        }
    }
}
```

注意：`willSleepNotification` 和 `didWakeNotification` 通常能很好地对应 MacBook 的合盖和开盖操作。

### 快速检查合盖状态（用于脚本）

```bash
# 返回 Yes/No
ioreg -r -k AppleClamshellState -d 4 | grep AppleClamshellState | awk '{print $NF}' | tr -d '"'
```

你可以通过 cron/launchd 使用此命令进行轮询，但基于事件的（SleepWatcher）效果要好得多。

SleepWatcher + 通知脚本是 2025/2026 年针对该用例最流行、轻量级且可靠的解决方案。

References:

- [SleepWatcher official page](http://www.bernhard-baehr.de/)
- [NSWorkspace sleep/wake notifications](https://developer.apple.com/documentation/appkit/nsworkspace)
- [IORegisterForSystemPower (lower level)](https://developer.apple.com/documentation/iokit/1557114-ioregisterforsystempower)
- [Ask Different – run script on lid close](https://apple.stackexchange.com/questions/104486/macbook-air-pro-run-script-upon-lid-close)
- [Medium – detect system events in Swift](https://medium.com/@clyapp/using-swift-to-detect-osx-system-events-sleep-wakeup-lock-unlock-screensaver-display-change-529cae9a3e23)
