---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ubuntu Shutdown Commands Guide
translated: false
type: note
---

**Question:** How to run "shutdown now" in Ubuntu?

**Answer:**

Here are the correct and commonly used ways to immediately shut down Ubuntu (from the terminal):

### Most recommended modern methods (Ubuntu 18.04 → 2026)

```bash
# Cleanest and most commonly used today
sudo systemctl poweroff

# Immediate shutdown (same as above in most cases)
sudo poweroff

# Alternative spelling that also works
sudo shutdown now
```

### All main variations that actually work

| Command                        | What it does                              | Needs sudo? | Notes                                      |
|-------------------------------|--------------------------------------------|-------------|--------------------------------------------|
| `sudo systemctl poweroff`     | Most modern & recommended way             | Yes         | Cleanest method in 2020–2026               |
| `sudo poweroff`               | Simple shortcut                           | Yes         | Very commonly used                         |
| `sudo shutdown now`           | Classic System V style command            | Yes         | Still works, but considered legacy         |
| `sudo shutdown -h now`        | Same as above (more explicit)             | Yes         | -h = halt/poweroff                         |
| `sudo init 0`                 | Very old-school way                       | Yes         | Works but almost never used anymore        |
| `sudo reboot`                 | Reboot instead of shutdown                | Yes         | Just for reference                         |
| `sudo systemctl reboot`       | Modern way to reboot                      | Yes         | —                                          |

### Quick "I just want to shut down right now" cheat sheet

Pick **any one** of these — they all work in 2025/2026:

```bash
sudo poweroff
# or
sudo systemctl poweroff
# or (still works)
sudo shutdown now
```

### Bonus: Most polite way people usually type

```bash
# Most common real-world command people actually use:
sudo shutdown -h now
```

All of these will close applications cleanly and power off the computer immediately.

**References:**

- None needed (this is standard Ubuntu behavior across recent versions)
