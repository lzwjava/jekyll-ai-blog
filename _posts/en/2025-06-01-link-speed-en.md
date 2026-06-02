---
audio: false
generated: true
lang: en
layout: post
title: Check Ethernet Link Speed in Ubuntu
translated: false
type: note
---

In Ubuntu, you can check the Ethernet link speed using several command-line tools. Here are the most common methods:

### **1. Using `ethtool` (Recommended)**
`ethtool` is the most reliable way to check the current link speed of your Ethernet interface.

#### Install `ethtool` (if not already installed):
```bash
sudo apt install ethtool
```

#### Check the link speed:
```bash
sudo ethtool <interface_name>
```
Replace `<interface_name>` with your Ethernet interface (e.g., `eth0`, `enp3s0`, `ens33`).

#### Example:
```bash
sudo ethtool enp3s0
```
Look for the `Speed` and `Duplex` fields in the output:
```
Settings for enp3s0:
    Supported ports: [ TP ]
    Supported link modes:   10baseT/Half 10baseT/Full
                            100baseT/Half 100baseT/Full
                            1000baseT/Full
    Supported pause frame use: No
    Supports auto-negotiation: Yes
    Supported FEC modes: Not reported
    Advertised link modes:  10baseT/Half 10baseT/Full
                            100baseT/Half 100baseT/Full
                            1000baseT/Full
    Advertised pause frame use: No
    Advertised auto-negotiation: Yes
    Advertised FEC modes: Not reported
    Speed: 1000Mb/s   # <--- This is your current link speed
    Duplex: Full      # <--- Full or Half duplex
    Port: Twisted Pair
    PHYAD: 1
    Transceiver: internal
    Auto-negotiation: on
    MDI-X: on (auto)
    Supports Wake-on: pumbg
    Wake-on: d
    Current message level: 0x00000007 (7)
                           drv probe link
    Link detected: yes      # <--- Indicates if the cable is connected
```

---

### **2. Using `ip` or `ifconfig` (Basic Info)**
These commands show whether the interface is up but do not directly display link speed.

#### Using `ip`:
```bash
ip link show <interface_name>
```
Example:
```bash
ip link show enp3s0
```
(Does not show speed, just link status.)

#### Using `ifconfig` (deprecated but still used):
```bash
ifconfig <interface_name>
```
Example:
```bash
ifconfig enp3s0
```
(Shows if the interface is up but not speed.)

---

### **3. Using `dmesg` (Check Driver Logs)**
Sometimes, the Ethernet driver logs the negotiated speed during initialization.
```bash
dmesg | grep <interface_name>
```
Example:
```bash
dmesg | grep enp3s0
```
Look for lines like:
```
[    5.123456] e1000e: enp3s0 NIC Link is Up 1000 Mbps Full Duplex
```

---

### **4. Using `mii-tool` (Older Systems)**
For very old systems, `mii-tool` might work:
```bash
sudo apt install net-tools
sudo mii-tool -v <interface_name>
```
Example:
```bash
sudo mii-tool -v eth0
```
(Not recommended for modern Gigabit Ethernet.)

---

### **Summary**
- **Best method:** `sudo ethtool <interface>` (shows speed, duplex, auto-negotiation).
- **Alternative:** Check `dmesg` logs if `ethtool` is unavailable.
- **Basic status:** `ip link show` or `ifconfig` (does not show speed).

Let me know if you need further clarification! 🚀
