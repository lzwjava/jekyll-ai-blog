---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ubuntu USB Installer Stuck at 30 Minutes
translated: false
type: note
---

Question: Your Ubuntu USB boot/install disk has been plugged in, and the progress bar has been running for ~30 minutes. What is happening?

Answer: **30 minutes is unusually long** if the progress bar is actually stuck. Most likely one of these is happening:

1. **USB drive is very slow or failing**

   * Old/cheap USB flash drives can have terrible sustained write speed.
   * A failing flash drive can appear to make progress and then stall.

2. **Ubuntu is verifying/writing the USB**

   * If you're *creating* the Ubuntu boot USB, the tool may be writing the ISO and then verifying it.
   * A normal USB should usually finish in several minutes, not half an hour.

3. **The USB port/controller is problematic**

   * Try another USB port, preferably a motherboard rear I/O port.
   * Avoid USB hubs.

4. **If you're already booting Ubuntu from the USB**

   * A long pause can be caused by hardware initialization, GPU drivers, or filesystem errors.
   * Press `Esc` to see whether Ubuntu is hiding boot messages behind the graphical progress screen.

### If you're currently creating the Ubuntu USB

On another Linux machine, I'd check:

```bash
lsblk
sudo dmesg -w
```

Then plug the USB in and watch for errors such as:

```text
I/O error
Buffer I/O error
device descriptor read error
reset SuperSpeed USB device
```

If you're using `dd` and it looks frozen, you can check its progress with:

```bash
sudo kill -USR1 $(pgrep '^dd$')
```

You'll get something like:

```text
2147483648 bytes copied, 120 s, 17.9 MB/s
```

**Don't unplug it while `dd` is still writing.**

If you tell me **what exactly is showing the progress bar** (Ubuntu installer, Rufus, Startup Disk Creator, Ventoy, or Ubuntu boot screen), I can tell you much more precisely what's happening.