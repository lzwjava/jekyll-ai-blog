---
audio: false
generated: true
image: false
lang: en
layout: post
title: HDMI Hot-Plug Storm Not Screensaver
translated: false
type: note
---

## Diagnosis: it's an HDMI hot-plug (HPD) interrupt storm, not a screensaver

Your monitor isn't going to sleep — it's being re-detected as "disconnected/reconnected" over and over, so the desktop reprograms the display and blacks out ~1s each time.

The smoking gun in the kernel log (roughly 1 minute before I looked):

```
01:58:49 kernel: workqueue: i915_hotplug_work_func [i915] hogged CPU ... 4 times
01:59:10 kernel: workqueue: i915_hotplug_work_func [i915] hogged CPU ... 5 times
01:59:11 kernel: i915 0000:00:02.0: [drm] HPD interrupt storm detected
                  on connector HDMI-A-1: switching from hotplug detection to polling
01:58:43 gnome-shell: Failed to post KMS update: drmModeAtomicCommit: Invalid argument
```

- `i915_hotplug_work_func` hammering the CPU = the GPU is drowning in hot-plug interrupts.
- The `drmModeAtomicCommit: Invalid argument` from GNOME is the failed modeset that shows up as the 1-second black screen.
- The kernel then gave up on interrupts and fell back to **polling** — which is why the status is currently stable (`connected` for 12s straight). It'll come back after a reboot until the root cause is fixed.

### It is NOT power/screensaver blanking

Your GNOME settings are already "never blank":

```
org.gnome.desktop.session idle-delay = 0
org.gnome.settings-daemon.plugins.power idle-dim = false
sleep-inactive-ac-timeout = 0
/sys/class/drm/card1-HDMI-A-1/dpms = On
```

So changing screen-lock/blank timeouts won't help.

### Hardware

- GPU: Intel Skylake GT2 HD 530 (`i915`), monitor: **Lenovo LI2364** on **HDMI-A-1**.

### Why it happens

The HDMI **Hot-Plug-Detect (HPD)** wire is electrically bouncing. The GPU reads that noise as rapid unplug/replug events, re-enumerates the connector, and the compositor re-modesets → black flash. Bouncy HPD is almost always **physical**: a marginal/cheap/long HDMI cable, a loose connector, an adapter, or a failing port/monitor.

### Fixes, most likely first

1. **Reseat / replace the HDMI cable.** Try a different, good, short cable. This fixes the large majority of HPD storms.
2. **Try another HDMI port** on the GPU (you have `HDMI-A-2`, `HDMI-A-3`) and the monitor's other HDMI input. Avoid HDMI adapters/switches.
3. **Try DisplayPort** if the monitor/GPU support it — DP hot-plug is usually more robust.
4. Confirm live while it blinks:

   ```
   sudo dmesg -w | grep -iE "hpd|hotplug|i915"
   ```

   If you see bursts each time it blacks, it's confirmed HPD.

### Software mitigations (if you can't change the cable right now)

- The kernel already switched to polling, so it may be calm until reboot. To stop the *interrupt* path from coming back, you can disable kernel DRM polling (turns re-detection off entirely — fine for a fixed desktop, but hot-plugging the monitor later won't be seen):

  ```
  echo 0 | sudo tee /sys/module/drm_kms_helper/parameters/poll
  ```

- Lock the mode so failed re-modesets are less disruptive — add to `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub`:

  ```
  video=HDMI-A-1:1920x1080@60e
  ```

  then `sudo update-grub` and reboot.
- Try the other installed kernel (`7.0.0-31-generic`) from the GRUB menu — i915 HPD handling changed across kernel versions, and 26.04 is on a very new `7.0.0-34`.

### Minor cleanup (not the cause)

`~/.config/monitors.xml` still describes a `DVI-I-1` 1024x768 monitor that isn't present — stale. Harmless, but I can clear it if you like.

Want me to apply the software mitigations (disable DRM polling + lock the HDMI mode) now so it stops until you can swap the cable?
