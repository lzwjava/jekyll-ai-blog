---
audio: false
generated: true
image: false
lang: en
layout: post
title: M40 wedged, reboot needed
translated: false
type: note
---

I have to stop here and hand it to you: the M40 is now **wedged and needs a reboot**.

## What happened

1. The unbind succeeded, but `rmmod nvidia` failed because `gnome-shell` and `github-desktop` held `/dev/nvidia*` (the nvidia module refcount was 36).
2. With the device half-detached, `modprobe nouveau` stalled, and my attempt to rebind `nvidia` is now stuck in the kernel:

   ```
   sh  D  device_driver_attach -> bind_store   (stuck >2 min)
   ```

3. Current state: M40 unbound, no `/dev/dri/renderD128`, nouveau not loaded. **Everything else is fine** — your desktop and the Intel GPU are unaffected.

This is recoverable only by reboot. `nouveau` stays blacklisted, so the `nvidia` driver comes back automatically on boot.

## What I changed so it can't happen again

`tools/muda-gpu-mode.sh` now checks the nvidia module refcount and **refuses** to switch while it's in use, printing the safe procedure. Added `--force` (stops the display manager first). Committed as `368bb6b`.

## What I need you to do

Reboot to restore the GPU:

```sh
sudo reboot
```

(or tell me to run it, but close unsaved work first — I can't see what's open).

## If you want to retry nouveau afterwards

Do it from a **text console** so nothing holds the nvidia device:

```sh
# Ctrl+Alt+F3, log in
cd ~/projects/muda
sudo systemctl isolate multi-user.target      # drop the GUI session
sudo tools/muda-gpu-mode.sh nouveau
MUDA_DRIVER=nouveau ./build/mudainfo          # paste this output
MUDA_DRIVER=nouveau ./build/test_memory
sudo systemctl isolate graphical.target       # or reboot to get the desktop back
```

The `--force` flag does the `isolate multi-user.target` step for you, but from inside the GUI it will close your session.

I'm sorry about the wedge — the root cause is that the desktop had the nvidia device open, which the original script didn't check for. Once you're rebooted, paste the `mudainfo` output from nouveau and I'll continue building the native compute path.
