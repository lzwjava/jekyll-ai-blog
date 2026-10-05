---
audio: false
generated: true
image: false
lang: en
layout: post
title: HDMI HPD Fault on i915
translated: false
type: note
---

## Diagnosis: it's an HDMI hot‑plug (HPD) fault on the Intel i915 display, not `ww` and not GNOME screen blanking

### Evidence from your machine

Your monitor is on the **Intel HD 530** (i915), connector **HDMI‑A‑1**:

```
/sys/class/drm/card1-HDMI-A-1/status: connected   (1920x1080)
```

And the kernel logged exactly the signature of an HPD line flapping:

```
Oct 05 19:20:36 kernel: i915 0000:00:02.0: [drm] HPD interrupt storm detected
                        on connector HDMI-A-1: switching from hotplug detection to polling
Oct 05 19:39:12 kernel: workqueue: i915_hpd_poll_init_work [i915] hogged CPU ... 4 times
Oct 05 19:39:35 kernel: workqueue: i915_hpd_poll_init_work [i915] hogged CPU ... 5 times
Oct 05 19:40:20 kernel: workqueue: i915_hpd_poll_init_work [i915] hogged CPU ... 7 times
```

### Why this produces "off 1s / on 30s / off 1s"

The HDMI connector's **Hot‑Plug‑Detect (HPD, pin 19)** signal is bouncing. Each time HPD deasserts, i915 thinks the monitor was unplugged and does a full modeset → screen goes black. When HPD comes back it re‑detects and lights up. The storm got so bad the driver gave up on interrupts and fell back to **polling**, and the polling work (`i915_hpd_poll_init_work`) kept re‑detecting the connector — hence the recurring ~1 s blackouts roughly every 30 s.

I ruled out the software suspects:

- `gsettings`: `idle-delay = 0` → GNOME **never** blanks or DPMS‑offs the screen. `ww linux screen-lock` is not involved.
- No cron jobs, no user timers, no custom watchers touching the display.
- In a live 60 s watch just now, `status` stayed `connected` and no new HPD messages appeared — so the fault is **intermittent**, matching your "time by time".

### Root cause (in order of likelihood)

1. **Bad/marginal HDMI cable** — HPD pin or ground not making solid contact, or signal integrity too poor. This is the #1 cause.
2. **Loose/dirty HDMI port** (monitor or motherboard) — reseat, try another port.
3. **HDMI switch / KVM / adapter in the chain** — remove it, connect direct.
4. **Monitor firmware** pulsing HPD on power‑save or auto‑source‑switch — disable "Auto Select / Auto Source", HDMI‑CEC, and eco/power‑saving in the monitor OSD.

### What to do

1. **Replace the HDMI cable** with a short, known‑good one (do this first).
2. Try a **different HDMI port** on both the monitor and the PC, and another monitor if available.
3. Bypass any switch/KVM.
4. In the monitor OSD, turn off **Auto Source / HDMI‑CEC / Deep Sleep**.
5. Watch live to confirm it's fixed:

   ```bash
   watch -n1 cat /sys/class/drm/card1-HDMI-A-1/status
   journalctl -k -f | grep -iE 'HDMI-A-1|HPD|storm'
   ```

   Any `disconnected` blips or new `HPD interrupt storm` lines = cable/port still bad.

### Software workaround if hardware can't be swapped right now

You can force the connector to stay on regardless of HPD, which stops the blackouts (at the cost of the mode being fixed):

- Add to the kernel cmdline (`/etc/default/grub`, then `sudo update-grub && reboot`):

  ```
  video=HDMI-A-1:1920x1080@60e
  ```

  The trailing `e` forces the connector enabled even when HPD drops. Also add `drm.debug=0` only if you need to debug further.

This masks the symptom — the real fix is the cable/port.

**Bottom line:** your monitor's HDMI hot‑plug‑detect line is flapping, so the Intel driver re‑modesets the display (~1 s black) each time. Replace the HDMI cable first, then the port; that resolves it in the overwhelming majority of cases.
