---
audio: false
generated: true
image: false
lang: en
layout: post
title: Linux Trackpad Different from macOS
translated: false
type: note
---

Question: Is it true that on a 2017 MacBook Pro running Fedora, the trackpad still works quite well? And does it use the same drivers as on macOS?

Answer:

No — this is a common misconception. The trackpad on a 2017 MacBook Pro under Fedora (or any Linux) does **not** use the same drivers as macOS, and the experience is meaningfully worse out of the box.

Two distinct hardware paths exist depending on the exact 2017 model:

**1. Non-Touch Bar 13" (the "MacBookPro14,1")** — uses a more traditional Apple trackpad reachable over the standard `bcm5974` USB driver in the Linux kernel. This one works reasonably well: multitouch, tap-to-click, two-finger scroll all function. Still not macOS-level, but usable.

**2. Touch Bar models (MacBookPro14,2 / 14,3)** — the trackpad and keyboard sit behind Apple's T1 chip and speak over a SPI interface, not standard USB. These need the out-of-tree `applespi` driver, which historically had to be loaded via the `macbook12-spi-driver` DKMS module before parts of it landed in mainline (`apple-ibridge` / `applespi` around kernel 5.x+). Without that, the trackpad and keyboard may not work at all on a fresh Fedora install.

Why the driver story differs fundamentally from macOS:

- macOS uses a closed userspace stack (`AppleMultitouchTrackpad`) with Apple's proprietary gesture-recognition engine. The kernel only delivers raw multitouch contact data; all the "feel" — momentum scrolling, palm rejection tuning, gesture acceleration curves — lives in that closed stack.
- Linux gets raw contacts via `bcm5974`/`applespi` and feeds them to **libinput**, which does its own (good but different) gesture/palm/scroll handling. So the hardware is the same, but the entire processing layer above it is a completely separate, open-source reimplementation.

Net result: scrolling and basic gestures are fine, but you'll notice missing or rougher palm rejection, no haptic Force Touch feedback (the Taptic Engine isn't driven), and three/four-finger gestures need manual config (e.g. `libinput-gestures` or `fusuma`). "Quite good" is fair for the non-Touch-Bar model; "as good as macOS" is not accurate for any of them.

If you want to check what's actually bound on a given unit:

```bash
# See which input devices and drivers are present
sudo libinput list-devices | grep -A6 -i trackpad

# Identify the model
cat /sys/devices/virtual/dmi/id/product_name   # e.g. MacBookPro14,3

# Check if applespi/bcm5974 is loaded
lsmod | grep -E 'applespi|bcm5974|apple_ib'

# Tune libinput behavior (tap, natural scroll) live
gsettings set org.gnome.desktop.peripherals.touchpad tap-to-click true
gsettings set org.gnome.desktop.peripherals.touchpad natural-scroll true
```

So: not the same drivers, and not the same quality — but on the non-Touch-Bar 2017 13", genuinely good enough for daily use.
