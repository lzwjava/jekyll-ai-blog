---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix HDMI Monitor Wake Issue
translated: false
type: note
---

Question: On an MSI Z170A GAMING M5 motherboard (Ubuntu), with the monitor connected through the motherboard's HDMI port, an AOC monitor stays dark after about 30 minutes idle, even when I move the mouse or press a key. How do I fix this?

Answer:

The board and the used-part listing are probably not the cause. This looks like a software or signal-handshake problem. After the screen blanks, the monitor loses the HDMI signal and sleeps. When the PC then tries to wake it, the monitor and graphics driver don't renegotiate the connection properly. Some HDMI monitors are especially prone to this (it is specific to certain monitors and especially affects HDMI-connected monitors).

First, find out whether the PC is awake or suspended. Press Num Lock or Caps Lock after the screen goes dark. If the keyboard light toggles, the PC is awake and only the display is stuck. If the light doesn't respond, the system suspended, and the wake-up problem is a different one.

Try these in order:

1. **Replug the HDMI cable once.** If that brings the picture back, it confirms the handshake problem (unplugging and replugging the HDMI monitor made it light up again for one Arch user with the same symptom).
2. **Switch to a text console and back.** Press Ctrl+Alt+F3, then Ctrl+Alt+F2 (or F1 on older versions). This often forces the display to reinitialize.
3. **Disable automatic suspend and screen blank to test.** In Settings → Power, turn off "Automatic Suspend" and set "Screen Blank" to "Never". Disabling full suspend and testing with screen blank only is a standard diagnostic step (as one troubleshooting guide suggests). If the problem disappears, you've found the trigger.
4. **Turn off X11 DPMS (only if you're on an Xorg session).** Run `xset -dpms s off`. To make it permanent, add it to your startup applications.
5. **Check whether you're on Wayland or Xorg.** Run `echo $XDG_SESSION_TYPE`. If it says `wayland`, log out and choose "Ubuntu on Xorg" from the gear icon on the login screen, then retest, or the reverse if you're already on Xorg.
6. **Set a fixed Xorg config.** One user fixed an HDMI monitor that wouldn't sleep or wake by creating a manual xorg.conf using the current configuration, which stopped X11 from auto-reconfiguring the monitor when DPMS kicked in.
7. **Check the monitor's own settings.** Look in the AOC OSD menu for an auto input source setting, "DDC/CI", or an "HDMI mode / Full Range" option. Try setting the input to HDMI manually instead of Auto. If the monitor has a DisplayPort or DVI input, trying another cable or port is a quick way to rule out the HDMI handshake. The Z170A GAMING M5 has DVI and HDMI outputs, so you can test DVI-to-DVI (or DVI-to-HDMI adapter) with no extra hardware.
8. **Try a different HDMI cable.** A poor cable or a bad port on the secondhand board can cause intermittent handshakes.
9. **Update the system.** Run `sudo apt update && sudo apt full-upgrade`. Intel graphics fixes ship through kernel and Mesa updates.

Because the board is secondhand, also confirm that the CPU you installed has integrated graphics (HDMI on the motherboard only works with a CPU that has Intel HD graphics, not F-series CPUs) and that the BIOS is updated to a recent version.

If none of that helps, send me your Ubuntu version, output of `echo $XDG_SESSION_TYPE`, your CPU model, and the result of the Num Lock test, and I can narrow it down.

References:

- [Why Does My Monitor Go to Sleep But Never Wake Up on Ubuntu?](https://us.ktcplay.com/blogs/support-tips/ubuntu-monitor-wont-wake-up)
- [Monitor won't enter sleep when logged in (Ubuntu Budgie 24.04)](https://discourse.ubuntubudgie.org/t/monitor-wont-enter-sleep-when-logged-in-ubuntu-budgie-24-04/7257)
- [monitor doesn't turn on, dpms after upgrade (Arch Linux forums)](https://bbs.archlinux.org/viewtopic.php?id=259462)
