---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mac Sleep Wakeup Reminders
translated: false
type: note
---

Question: How to detect when macOS closes the lid or goes to sleep, and when it wakes up, in order to send a notification to remind myself to do something?

Answer:

There are several practical ways to achieve this on macOS. The most reliable and commonly used method for regular users is **SleepWatcher** (a small daemon) combined with simple shell scripts. This approach works well for sending reminders when the Mac **goes to sleep** (usually when you close the lid) and when it **wakes up** (usually when you open the lid or press a key).

### Recommended Solution: Use SleepWatcher (easiest for most people)

1. Install SleepWatcher via Homebrew (if you don't have Homebrew → `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`)

   ```bash
   brew install sleepwatcher
   ```

2. Create two simple scripts in your home folder:

   ```bash
   # Create script that runs when going to sleep (lid close → sleep)
   cat > ~/.sleep << 'EOF'
   #!/bin/bash
   osascript -e 'display notification "Lid closed / going to sleep — remember to XXX" with title "Reminder"'
   # You can also add: say "Lid closed, remember to do something"
   EOF

   # Create script that runs when waking up
   cat > ~/.wakeup << 'EOF'
   #!/bin/bash
   osascript -e 'display notification "Woke up / lid opened — time to do XXX" with title "Reminder"'
   # Optional: say "Welcome back, don't forget to..."
   EOF
   ```

3. Make them executable:

   ```bash
   chmod +x ~/.sleep ~/.wakeup
   ```

4. Start SleepWatcher (you can make it auto-start later):

   ```bash
   sleepwatcher --verbose \
     --sleep ~/.sleep \
     --wake ~/.wakeup
   ```

   To run it in background permanently:

   ```bash
   sleepwatcher --sleep ~/.sleep --wake ~/.wakeup &
   ```

   Better: create a launchd plist to auto-start it at login (many guides exist, or use `brew services start sleepwatcher` if Homebrew supports it).

**Result**:
- Close lid → mac sleeps → `~/.sleep` runs → you get notification
- Open lid / wake Mac → `~/.wakeup` runs → you get notification

### Alternative 1: Pure AppleScript + launchd (no extra tools)

Create one script that checks sleep state periodically (less elegant but works without installing anything):

```applescript
-- Save as ~/Library/Scripts/wake-sleep-notifier.scpt
on idle
    tell application "System Events"
        set currentState to (do shell script "pmset -g | grep -i 'sleep prevented' || true")
        -- Very rough — better to track previous state in a file
    end tell

    -- More practical: just use sleepwatcher style above
    return 60 -- check every minute
end idle
```

→ This is less accurate; SleepWatcher is strongly preferred.

### Alternative 2: Swift/App approach (for developers)

If you want a small menu bar app:

Use `NSWorkspace` notifications (simple & native):

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

Note: `willSleepNotification` and `didWakeNotification` usually correspond well to lid close/open on MacBooks.

### Quick lid state check (for scripts)

```bash
# Returns Yes/No
ioreg -r -k AppleClamshellState -d 4 | grep AppleClamshellState | awk '{print $NF}' | tr -d '"'
```

You can use this in cron/launchd to poll, but event-based (SleepWatcher) is much better.

SleepWatcher + notification scripts is the most popular, lightweight, and reliable solution for your use case in 2025/2026.

References:

- [SleepWatcher official page](http://www.bernhard-baehr.de/)
- [NSWorkspace sleep/wake notifications](https://developer.apple.com/documentation/appkit/nsworkspace)
- [IORegisterForSystemPower (lower level)](https://developer.apple.com/documentation/iokit/1557114-ioregisterforsystempower)
- [Ask Different – run script on lid close](https://apple.stackexchange.com/questions/104486/macbook-air-pro-run-script-upon-lid-close)
- [Medium – detect system events in Swift](https://medium.com/@clyapp/using-swift-to-detect-osx-system-events-sleep-wakeup-lock-unlock-screensaver-display-change-529cae9a3e23)
