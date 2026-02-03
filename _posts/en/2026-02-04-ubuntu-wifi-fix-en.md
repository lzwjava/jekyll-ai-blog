---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Ubuntu WiFi Not Showing
translated: false
type: note
---

The issue "WiFi doesn't show" in Ubuntu (no networks listed in settings, no WiFi icon in the top bar, or "No WiFi adapter found") is very common. It can come from:

- Hardware/rfkill switch turned off
- Driver/firmware not loading properly
- NetworkManager service glitch (very frequent after updates/reboots in 24.04+)
- Interface down or unmanaged
- Kernel/driver mismatch after upgrade

Follow these troubleshooting steps **in order** from the terminal (Ctrl+Alt+T to open it). Run them one by one and check after each if WiFi appears in Settings → Wi-Fi or in the top bar dropdown.

### 1. Quick restarts (fixes ~50–60% of cases)

```bash
# Restart NetworkManager service
sudo systemctl restart NetworkManager

# Or full stop/start
sudo nmcli networking off
sudo nmcli networking on

# Force WiFi rescan
nmcli device wifi rescan
nmcli device wifi list
```

After this, open Settings (or run `gnome-control-center wifi`) and check if networks appear. If not → next.

### 2. Check if WiFi is blocked (hardware switch / soft block – very common)

```bash
rfkill list all
```

Look for **Wireless LAN** lines.

- If you see **Soft blocked: yes** → fix with:
  ```bash
  rfkill unblock wifi
  rfkill unblock all
  ```

- If **Hard blocked: yes** → this is usually a physical switch or Fn + F-key (airplane mode key) on your laptop. Press it to toggle (look for a WiFi/antenna icon on your function keys).

Run `rfkill list` again to confirm both are **no**.

### 3. Check if the WiFi adapter is detected at all

```bash
# Best command – shows interface name (usually wlpXs0 or wlan0)
ip link show | grep -i wl

# Or more detailed
sudo lshw -C network | grep -i wireless -A 12

# Alternative
lspci | grep -i network  # or grep -i wireless
# For USB WiFi adapters: lsusb | grep -i wireless
```

- If you see your WiFi card (e.g., Intel, Realtek, Qualcomm Atheros) → good, proceed.
- If nothing or "**UNCLAIMED**" next to it → driver issue (jump to step 7).
- Note the interface name (e.g., `wlp2s0`) for later.

### 4. Bring the interface up manually

Replace `wlp2s0` with **your** interface name from step 3.

```bash
sudo ip link set wlp2s0 up
nmcli device wifi rescan
nmcli device wifi list
```

### 5. Reinstall NetworkManager (fixes many GUI/icon disappearance cases after updates)

```bash
sudo apt update
sudo apt install --reinstall network-manager network-manager-gnome
sudo systemctl restart NetworkManager
```

Then log out and log back in (or reboot).

### 6. If still nothing – check kernel messages for clues

```bash
dmesg | grep -i -E 'wlan|wifi|iwlwifi|rtl|ath|brcm|firm|error'
```

Common errors:

- "firmware load failed" → missing firmware (e.g., for Intel):
  ```bash
  sudo apt install linux-firmware
  sudo update-initramfs -u
  sudo reboot
  ```

- iwlwifi or Realtek issues → sometimes unloading/reloading helps:
  ```bash
  sudo modprobe -r iwlwifi    # or rtl8723be / whatever your driver is
  sudo modprobe iwlwifi
  ```

### 7. If adapter is detected but still no networks / "No WiFi adapter found"

- Try airplane mode toggle in settings (or `nmcli radio wifi off && nmcli radio wifi on`)
- Boot an **older kernel** if you recently updated (hold Shift during boot → Advanced → choose older kernel)
- In rare cases (broken upgrade), boot into **recovery mode** (hold Shift → Advanced → Recovery):
  - Choose "network" to enable networking
  - Choose "dpkg" to repair broken packages
  - Resume normal boot

### Next steps if nothing works

Run these and paste the output back here (copy-paste the full results):

```bash
rfkill list all
ip link show
sudo lshw -C network
lspci | grep -i network
nmcli device status
nmcli radio
```

Also tell me:

- Your Ubuntu version (`lsb_release -a`)
- Laptop brand/model (or WiFi card if you know)
- Did it work before / after update / fresh install?

Most cases get fixed by steps 1–5. Let me know what you see!