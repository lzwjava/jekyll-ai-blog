---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ubuntu WiFi Adapter Missing Fixes
translated: false
type: note
---

**Question:** In Ubuntu, why does it sometimes say "WiFi adapter not found", so there is no WiFi section in Settings, and thus you can't connect to WiFi?

**Answer:**

This is a very common issue in Ubuntu (and other Linux distributions). The **"No WiFi adapter found"** message appears — and the WiFi section disappears or becomes unavailable in Settings — when Ubuntu cannot properly detect or use your wireless network adapter. Here are the main reasons this happens:

### Main Causes
1. **Missing or incorrect WiFi driver**
   Many WiFi chipsets (especially Broadcom, Realtek, some Qualcomm/Atheros) do not have fully open-source drivers included by default in Ubuntu.
   - If the driver is missing, not loaded, or the wrong one is used → the system does not see a usable wireless interface → NetworkManager hides the WiFi option.

2. **Hardware/firmware not detected at all**
   Run `lspci | grep -i network` (for internal PCIe cards) or `lsusb` (for USB WiFi adapters).
   If your WiFi card does **not** appear → kernel does not see the hardware (rare, but can happen after suspend, kernel update, loose card, or hardware failure).

3. **Driver is loaded but NetworkManager does not recognize the interface**
   You see the card in `lspci` or `lshw -C network`, but Settings still says no adapter.
   This can happen with buggy drivers, rfkill block, or misconfiguration.

4. **Fast Startup / hybrid shutdown from Windows (dual-boot)**
   Windows Fast Startup leaves the WiFi card in a weird powered-off state → Linux cannot wake it properly.

5. **rfkill hardware or software block**
   WiFi can be hard-blocked (physical switch / Fn key) or soft-blocked.

6. **Kernel regression or incompatible version**
   After a kernel update (or fresh install of newer Ubuntu), a previously working chipset stops working.

### Quick Troubleshooting Steps (in order of priority)
1. **Check if the hardware is seen**
   Open Terminal and run:
   ```
   lspci -nnk | grep -iA3 net
   ```
   or
   ```
   lshw -C network
   ```
   Look for "Wireless", "WiFi", "802.11", "Network controller". Note the vendor:device ID (e.g. 14e4:4360 = Broadcom).

2. **Check rfkill status**
   ```
   rfkill list all
   ```
   If "Hard blocked: yes" → press the physical WiFi key or Fn+F-key combo.
   If "Soft blocked: yes" → run `rfkill unblock wifi`.

3. **Try to enable WiFi via terminal**
   ```
   nmcli radio wifi on
   nmcli device wifi list
   ```
   If you see networks → the driver works, but GUI failed.

4. **Install proprietary drivers (most common fix)**
   - Connect via Ethernet, USB tethering from phone, or another way temporarily.
   - Open **Software & Updates** → **Additional Drivers** tab.
   - Select the recommended WiFi driver (e.g. bcmwl-kernel-source for Broadcom, or something for Realtek).
   - Apply Changes → reboot.

5. **Dual-boot Windows fix**
   Boot into Windows → disable **Fast Startup** (Control Panel → Power Options → "Choose what the power buttons do" → uncheck "Turn on fast startup") → shut down completely (not restart) → boot Ubuntu.

6. **Other quick commands people often use**
   ```
   sudo apt update
   sudo apt install --reinstall network-manager
   sudo modprobe -r <driver_name> && sudo modprobe <driver_name>   # e.g. rtl8821ae, rtw89_8852be
   ```

### Summary
In most cases (especially laptops with Broadcom or Realtek chips), the root cause is a **missing proprietary driver**. Ubuntu hides the WiFi section in Settings when NetworkManager sees zero wireless devices. Once you get a working driver (via Additional Drivers + internet), the WiFi section reappears and you can connect normally.

If you share the output of `lspci -nnk | grep -iA3 net` or tell us your laptop model / WiFi chipset, people can usually give the exact command to fix it.

**References:**

- [Ubuntu Community Wireless Troubleshooting Guide](https://help.ubuntu.com/community/WifiDocs/WirelessTroubleShootingGuide)
- [ItsFOSS: Fix No Wireless Network in Ubuntu](https://itsfoss.com/fix-no-wireless-network-ubuntu)
- [Ask Ubuntu: No Wi-Fi Adapter Found threads](https://askubuntu.com/questions/tagged/wifi+no-wifi-adapter-found)
