---
audio: false
generated: true
image: false
lang: en
layout: post
title: Linux Mint Proxy Router Setup Guide
translated: false
type: note
---

**Task Summary: SSH Connectivity Test & Linux Mint Proxy Router Setup**

**Objective:** Test SSH connection to `192.168.1.42`, then configure the Linux Mint laptop as a wired proxy router using built-in Ethernet as WAN and USB-Ethernet as LAN with Clash TUN transparent proxy.

---

### **Phase 1: SSH Connection Testing**

**Initial Failure:**
- First attempt: `ssh lzwjava@192.168.1.42` with password `88888888` entered interactively
- **Problem:** SSH hung at password prompt, timed out, got signal 15 (terminated)
- **Diagnosis:** Password might be wrong, or SSH config issue

**Critical Breakthrough:**
- Installed `sshpass` to automate password passing
- Command: `sshpass -p '88888888' ssh lzwjava@192.168.1.42 'echo "Connected as $(whoami)"'`
- **Result:** ✅ Success! Password was correct; interactive timing was the issue

**Lesson:** Use `sshpass` for automated password authentication in scripts/automation.

---

### **Phase 2: System Reconnaissance**

**Host Details:**
- OS: Linux Mint 22.3 "Zena" (Ubuntu 24.04 base)
- Kernel: 6.17.0-14-generic
- Hardware: Lenovo G490 laptop (2013-era ThinkPad)
- Network: Built-in Qualcomm Atheros Ethernet (`enp2s0`) on `192.168.1.42/24`
- USB Ethernet: Detected as `enx00e04c362f89` (Realtek chip, MAC `00:e0:4c:36:2f:89`)

---

### **Phase 3: Router Configuration**

**Step 1: Enable IP Forwarding**
```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p
```

**Step 2: Configure NAT Masquerade**
```bash
iptables -t nat -A POSTROUTING -o enp2s0 -j MASQUERADE
```
- **Purpose:** Allow LAN clients to reach internet through laptop's WAN interface
- **Interface:** `enp2s0` (built-in Ethernet facing modem/router)

**Step 3: Configure USB Ethernet Interface**
```bash
nmcli con add type ethernet ifname enx00e04c362f89 con-name usb-lan \
ip4 192.168.201.1/24 gw4 ""
nmcli con up usb-lan
```
- **Subnet:** `192.168.201.0/24` (different from WAN's `192.168.1.0/24`)
- **Gateway:** None (this device IS the gateway)
- **Status:** Interface UP with IP but DOWN (no cable connected yet)

**Step 4: Install & Configure dnsmasq DHCP Server**

**Major Difficulty:**
- Initial `dnsmasq` service failed to start
- **Error:** `failed to create listening socket for port 53: Address already in use`
- **Diagnosis:** `systemd-resolved` already listening on port 53 (DNS)

**Critical Breakthrough:**
Modified `/etc/dnsmasq.d/usb-lan.conf`:
```ini
interface=enx00e04c362f89
dhcp-range=192.168.201.50,192.168.201.150,12h
dhcp-option=3,192.168.201.1 # Gateway
dhcp-option=6,192.168.201.1 # DNS
no-resolv
server=8.8.8.8
server=1.1.1.1
port=0 # Disable DNS server
bind-interfaces # Bind only to USB interface
```

**Why this worked:**
- `port=0`: Disables dnsmasq's DNS functionality (not needed since we have systemd-resolved)
- `bind-interfaces`: Ensures dnsmasq only binds to USB Ethernet
- Service starts successfully, provides DHCP only on `192.168.201.0/24` subnet

---

### **Phase 4: Clash Proxy Installation**

**Step 1: Install Clash Meta (mihomo)**
- Downloaded latest release from GitHub: `mihomo-linux-amd64-compatible-v1.19.21.gz`
- Extracted, renamed to `clash-meta`, installed to `/usr/local/bin/`
- Verified: `clash-meta -v` shows v1.19.21

**Step 2: Create Basic Configuration**
```yaml
tun:
enable: true
stack: system
dns-hijack:
- any:53
auto-route: true
auto-detect-interface: true
```
- **Key features:** TUN mode for transparent proxying, auto-route for LAN traffic
- DNS hijacking to redirect client DNS queries through Clash

**Step 3: Create Systemd Service**
- Service file at `/etc/systemd/system/clash.service`
- Runs as `lzwjava` user with `CAP_NET_ADMIN` capabilities (required for TUN)
- Auto-restart on failure

---

### **Current Network Architecture**

```
[Internet] ←→ [Modem/Router] (192.168.1.1)
↓
[enp2s0] Linux Mint (192.168.1.42)
↓
[Clash TUN] ←→ [iptables NAT]
↓
[enx00e04c362f89] (192.168.201.1)
↓
[USB Ethernet Cable]
↓
[Client Devices] (DHCP: 192.168.201.50-150)
```

---

### **Critical Design Decisions**

1. **Separate Subnets:** WAN (`192.168.1.0/24`) vs LAN (`192.168.201.0/24`) prevents routing conflicts
2. **TUN over REDIR:** Chose TUN mode for better transparency (handles UDP, ICMP)
3. **dnsmasq over ISC DHCP:** Lightweight, easier configuration
4. **Port 0 for dnsmasq:** Avoids conflict with systemd-resolved while keeping DHCP
5. **Static IP on USB:** Ensures consistent gateway address (`192.168.201.1`)

---

### **Remaining To-Do**

1. **Physical Connection:** Plug Ethernet cable from USB adapter to switch/client
2. **Start Clash:** `sudo systemctl start clash`
3. **Add Proxy Config:** Edit `~/.config/clash/config.yaml` with actual server details
4. **Test Client:** Connect device, verify gets IP, internet routes through proxy

---

### **Potential Performance Considerations**

1. **Old Hardware:** 2013 ThinkPad may bottleneck at ~100-300Mbps through Clash + encryption
2. **USB 2.0 Bottleneck:** USB-Ethernet adapter limited to ~480Mbps theoretical
3. **Memory:** Clash uses ~50-100MB RAM; okay for 4GB+ systems
4. **CPU:** AES-NI helps if available (likely not on 3rd gen Intel)

**Total time:** ~22 minutes (02:12 to 02:34)
**Status:** ✅ Ready for physical testing and proxy configuration
