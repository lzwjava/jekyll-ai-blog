---
audio: false
generated: true
lang: en
layout: post
title: Fixing Wi-Fi Drops on Ubuntu
translated: false
type: note
---

Wi-Fi disconnections on Ubuntu while wired connections remain stable can be caused by several factors. Here’s a step-by-step guide to diagnose and fix the issue:

---

### **1. Check for Driver Issues**

Your MSI B760M Mortar WiFi motherboard likely uses an **Intel Wi-Fi 6E AX211/AX210** card. While Intel drivers are generally well-supported in Linux, issues can still arise.

#### **Steps:**

- **Identify your Wi-Fi chipset:**
  Run in terminal:

  ```bash
  lspci -knn | grep -iA3 net
  ```

  Look for the Wi-Fi adapter (likely `Intel Corporation Device [8086:...]`).

- **Check if the correct driver is loaded:**

  ```bash
  lsmod | grep iwlwifi
  ```

  If nothing appears, the driver isn’t loaded.

- **Install/Update drivers:**
  Intel Wi-Fi drivers (`iwlwifi`) are included in the Linux kernel, but you may need firmware updates:

  ```bash
  sudo apt update && sudo apt install --reinstall linux-firmware
  ```

---

### **2. Disable Power Saving for Wi-Fi**

Linux sometimes aggressively powers down the Wi-Fi card to save energy, causing drops.

#### **Steps:**

- Temporarily disable power saving:

  ```bash
  sudo sed -i 's/wifi.powersave = 3/wifi.powersave = 2/' /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
  ```

  Or manually check with:

  ```bash
  iw dev wlan0 get power_save
  ```

  (Replace `wlan0` with your interface name from `ip a`.)

- **Apply changes:**

  ```bash
  sudo systemctl restart NetworkManager
  ```

---

### **3. Check for Interference or Router Issues**

- **Test with another device** (phone/laptop) to see if the issue persists.
- **Change Wi-Fi channel** (use `iwlist` to scan for congested channels):

  ```bash
  sudo iwlist wlan0 scan | grep Frequency
  ```

- Try **5GHz band** (if available) for less interference.

---

### **4. Disable IPv6**

Some routers/ISPs have IPv6 compatibility issues.

#### **Steps:**

- Edit `/etc/sysctl.conf` and add:

  ```plaintext
  net.ipv6.conf.all.disable_ipv6=1
  net.ipv6.conf.default.disable_ipv6=1
  ```

- Apply:

  ```bash
  sudo sysctl -p
  ```

---

### **5. Update Kernel & NetworkManager**

Newer kernels often fix Wi-Fi issues.

```bash
sudo apt update && sudo apt upgrade
```

If needed, install a **mainline kernel** (e.g., 6.5+):

```bash
sudo apt install linux-image-generic-hwe-22.04
```

---

### **6. Disable Hardware Encryption (if applicable)**

Some Intel Wi-Fi cards have issues with hardware encryption.
Edit `/etc/modprobe.d/iwlwifi.conf` (create if missing):

```plaintext
options iwlwifi 11n_disable=1
```

Then:

```bash
sudo modprobe -r iwlwifi && sudo modprobe iwlwifi
```

---

### **7. Check for RFKill or Blocked Wi-Fi**

```bash
rfkill list
```

If the Wi-Fi is blocked (e.g., `soft blocked: yes`), unblock it:

```bash
sudo rfkill unblock wifi
```

---

### **8. Test with a USB Wi-Fi Adapter**

If the issue persists, try a **Linux-compatible USB Wi-Fi adapter** (e.g., TP-Link Archer T4U) to isolate whether the problem is with the Intel card.

---

### **9. Check Logs for Errors**

```bash
journalctl -u NetworkManager --no-pager -n 50
```

Look for `iwlwifi` errors or disconnection events.

---

### **Final Notes**

- If none of the above works, consider **dual-booting Windows** to check if the issue is hardware-related.
- Alternatively, use a **USB-to-Ethernet adapter** if Wi-Fi remains unreliable.

Let me know if you need further debugging!
