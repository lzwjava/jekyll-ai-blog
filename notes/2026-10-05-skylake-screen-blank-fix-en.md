---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skylake Screen Blank Fix
translated: false
type: note
---

I dug into the actual machine instead of trusting the generic Q&A, and found several things that change the answer. Here's what's really going on and what I did.

## What the system actually is

| Item | Value |
|---|---|
| Board | MSI **Z170A GAMING M5 (MS-7977)** — matches your MSI board |
| OS / DE | Ubuntu 26.04, **GNOME Shell 50.1** |
| Session | **Wayland** (`XDG_SESSION_TYPE=wayland`) |
| CPU/GPU | i5-6600 → Intel **HD Graphics 530** (i915), so integrated graphics *is* present |
| Second GPU | NVIDIA **Tesla M40** (`prime-select on-demand`, `nvidia_drm.modeset=1`) — compute-only, no display outputs |
| Display | AOC **2369** on `card1-HDMI-A-1`, 1920x1080@60 |
| Idle | `sleep-inactive-ac-timeout=0` (no suspend on AC), `idle-delay=300` (blank after **5 min**), `idle-dim=true` |

Two important corrections to the answer you pasted:

1. **You're on Wayland, not Xorg.** So steps 4 (`xset -dpms s off`) and 6 (hand-made `xorg.conf`) do **nothing** here — GNOME/mutter manages DPMS on Wayland, not the X server. Those are Xorg-only.
2. **Suspend is not your problem.** On AC, `sleep-inactive-ac-timeout` was already `0`. What actually fires is GNOME's **screen blank** (`idle-delay=300`, i.e. ~5 min, not 30 — you likely misremembered, or dim-at-4.5-min made it feel longer). After blanking, mutter turns the i915 pipe off; your HDMI monitor then sleeps and the i915↔AOC link doesn't renegotiate on wake. The kernel even hints at the underlying Skylake weakness in your log:
   ```
   i915 ... Reducing the compressed framebuffer size. ... Try to increase stolen memory size if available in BIOS.
   ```

## What I changed already (no root needed, effective immediately)

```bash
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.settings-daemon.plugins.power idle-dim false
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout 0
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-timeout 0
```
Verified: `idle-delay=0`, `idle-dim=false`, both sleep timeouts `0`. This stops the display from ever entering the state that wedges it. It's a workaround, not the root-cause fix.

## The real fix (needs sudo — you have no passwordless sudo here)

**1. Disable Skylake display power (DC) states — the actual root cause.** This is the known "Intel Skylake screen won't come back after DPMS off" bug:
```bash
sudo cp /etc/default/grub /etc/default/grub.bak
# append to GRUB_CMDLINE_LINUX_DEFAULT (inside the quotes):
#   i915.enable_dc=0 i915.enable_fbc=0
sudo sed -i 's/\\(GRUB_CMDLINE_LINUX_DEFAULT="[^"]*\\)"/\1 i915.enable_dc=0 i915.enable_fbc=0"/' /etc/default/grub
sudo update-grub
sudo reboot
```

**2. Fix the BIOS DVMT/stolen memory (the kernel literally asked for this).** Reboot into MSI BIOS → *Settings → Advanced → Integrated Graphics Configuration*:
- **DVMT Pre-Allocated: 64M** (or higher; default 32M is too small)
- **DVMT Total Gfx Mem: MAX**
- **IGD Multi-Monitor: Enabled**
- Update BIOS to the latest 7977v1x release while you're there.

**3. AOC 2369 OSD** (physical monitor): set *Input Select → HDMI* manually instead of Auto, and turn off any **Off Timer / Auto Power Off / Eco** mode. Auto source-scan is a common trigger for this exact HDMI handshake loss.

**4. Rule out HDMI itself.** The board also has DVI-D. Try the other HDMI port or a DVI–HDMI adapter and a different cable to isolate a bad secondhand port.

**5. Optional: test the NVIDIA coexistence.** The Tesla M40 has no display outputs, yet `prime-select on-demand` is active with `nvidia_drm.modeset=1`. If the i915 fix alone doesn't hold, test `sudo prime-select intel` (and reboot) to see if the NVIDIA DRM stack is interfering with Wayland wake.

## How to confirm the diagnosis next time it happens

- Before touching anything, note `cat /sys/class/drm/card1-HDMI-A-1/status` and `.../dpms`. If `status` flips to `disconnected` while the cable is still in, it's the link-loss/handshake bug (confirms DC-state fix). If it stays `connected` but `dpms=Off`, mutter is failing to re-enable.
- Num Lock test: if the LED toggles, the PC is awake and only the display is stuck; if not, it suspended.
- Recovery that works on Wayland: `Ctrl+Alt+F3` then `Ctrl+Alt+F2` (VT switch forces a modeset), or unplug/replug HDMI once.

Bottom line: the pasted answer's X11 `xset`/`xorg.conf` advice doesn't apply to your Wayland session, and suspend was already off. The trigger was GNOME's 5-minute screen blank on a Skylake iGPU with an HDMI handshake bug — I've disabled the blanking now, and `i915.enable_dc=0` + the BIOS DVMT fix are the durable fixes.