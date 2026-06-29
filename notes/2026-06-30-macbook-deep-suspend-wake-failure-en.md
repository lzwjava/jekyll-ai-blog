---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacBook Deep Suspend Wake Failure
translated: false
type: note
---

Here's the complete diagnosis:

---

**Root Cause: System entered deep suspend (S3) and never woke up.**

The previous boot's death sequence at 03:17:58–03:17:59:

```
systemd-logind[1005]: Power key pressed short.
systemd-logind[1005]: The system will suspend now!
NetworkManager: sleep requested
systemd-sleep[28058]: Performing sleep operation 'suspend'...
kernel: PM: suspend entry (deep)
```

Then **nothing** — no `PM: suspend exit`, no resume, no further log entries at all. The system went to sleep fine, but the **wake-up failed completely**. No keyboard, trackpad, or lid-open signal could bring it back, forcing a power-button hard reset.

**Why it happens (Apple MacBook on Linux):**

Your `/proc/acpi/wakeup` shows the problem:

| Device | Wake from S3 (deep)? | Wake from S4? |
|--------|:---:|:---:|
| LID0 (lid open) | **No** | Yes (hibernate only) |
| SPIT (touchpad) | Yes | — |
| Keyboard | **Not listed at all** | — |
| Power button | **Intercepted by systemd-logind** | — |

On Apple MacBook hardware running Linux:
- **No device is properly configured to wake from deep S3 sleep** — the keyboard isn't in the ACPI wakeup table, and lid-open is only wired for S4 (hibernate), not S3.
- The power button was pressed right when suspend was happening (note: two "Power key pressed short" logs at 03:17:58 and 03:17:59) — the first one *triggered* the suspend, the second was eaten by the suspend process.
- Deep suspend (S3) is the default: `s2idle [deep]` — the `[deep]` marks active mode.

**Quick fix — switch to s2idle (modern standby):**

s2idle is a shallower sleep that doesn't fully power off the CPU — it uses slightly more battery but **wakes reliably** on Apple hardware because the keyboard/trackpad stays alive.

```bash
# Make persistent
echo 'SleepMode=s2idle' | sudo tee -a /etc/systemd/sleep.conf.d/disable-deep-suspend.conf
```

Or try it immediately:

```bash
sudo sh -c 'echo s2idle > /sys/power/mem_sleep'
```

**Alternative — disable auto-suspend entirely** if the lid-close suspend isn't intended:

```bash
# Don't suspend on lid close
gsettings set org.gnome.settings-daemon.plugins.power lid-close-ac-action 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
```

Want me to apply either of these?