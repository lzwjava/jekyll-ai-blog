---
audio: false
generated: true
lang: en
layout: post
title: Ubuntu Suspend Guide
translated: false
type: note
---

In Ubuntu, you can put your system to sleep or hibernate using several methods:

## GUI Methods:
- **Top-right corner**: Click the power/settings icon in the top panel, then select "Suspend" (sleep) or "Hibernate" if available
- **Activities menu**: Press the Super key, type "power" or "suspend", and select the power options

## Command Line Methods:
```bash
# To suspend (sleep)
systemctl suspend

# To hibernate
systemctl hibernate

# To hybrid sleep (combination of both)
systemctl hybrid-sleep
```

## Keyboard Shortcuts:
- Many Ubuntu systems use **Fn + Sleep key** or **Ctrl + Alt + End** by default
- You can customize these in Settings > Keyboard > Shortcuts

## Important Notes:
- **Sleep/Suspend**: Keeps RAM powered, quick wake-up but uses some battery
- **Hibernate**: Saves everything to disk and shuts down, slower wake-up but no power consumption
- Hibernate might not be enabled by default on newer Ubuntu versions due to potential issues with some hardware

If hibernate isn't working, you may need to enable it first by configuring swap space and editing system settings. Sleep/suspend should work out of the box on most systems.
