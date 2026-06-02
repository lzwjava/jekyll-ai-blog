---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacOS Alarm Mechanism Explained
translated: false
type: note
---

Good catch — you're right, and I was wrong about that.

macOS does handle this correctly. When you set an alarm in Clock on Mac, it registers with the OS-level notification system, not just the app process. So when the alarm time hits, **Notification Center fires it** even if Clock.app is closed — same mechanism that lets Calendar alerts fire without Calendar being open.

Under the hood it's using `UNUserNotificationCenter` (UserNotifications framework), which is process-independent. The OS daemon `UserNotificationCenter` holds the schedule and fires it regardless of app state. The one caveat: machine still needs to be **awake** — if the lid is closed or the Mac is in sleep, it won't fire (unlike iPhone which has the dedicated alarm coprocessor path that wakes from deep sleep).

So the actual limitation compared to iOS is just:
- **Mac asleep** → alarm silently missed
- **Mac awake but app closed** → alarm fires fine ✓

Thanks for testing it directly — that's the right way to know. I was wrong to call it a toy without verifying.
