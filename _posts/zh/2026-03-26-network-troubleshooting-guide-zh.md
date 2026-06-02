---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 手动网络故障归纳指南
translated: true
type: note
---

Boss，这是针对 **192.168.1.42** 的手动 troubleshooting 指南：

---

## 🔧 Step-by-Step Guide

### Step 1: Check if the machine is alive

```bash
# Open a terminal, check basic system
hostname -I
```

如果你在物理 laptop 旁，首先确保它已开机且有响应。

---

### Step 2: Check network interface

```bash
ip addr show
# Look for your main interface (likely eth0 or enp* or wlan0)
# Make sure it has a valid IP like 192.168.1.42
```

**If no IP on the interface:**

```bash
# Restart network
sudo systemctl restart NetworkManager
# or if using netplan:
sudo netplan apply
```

---

### Step 3: Check if Clash left proxy settings behind

```bash
# Check environment variables for leftover proxy
env | grep -i proxy
# Check /etc/environment for proxy
cat /etc/environment
# Check DNS — Clash often changes this
cat /etc/resolv.conf
```

**If proxy env vars are set, clear them:**

```bash
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
unset no_proxy NO_PROXY
```

---

### Step 4: Fix DNS

```bash
# Check what DNS resolver is active
resolvectl status
# Try setting clean DNS
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
sudo bash -c 'echo "nameserver 114.114.114.114" >> /etc/resolv.conf'
```

---

### Step 5: Test connectivity

```bash
# Test gateway
ping -c 3 192.168.1.1
# Test DNS resolution
ping -c 3 baidu.com
# Test internet
curl -I https://www.baidu.com
```

---

### Step 6: If Clash set system proxy on browser

Go to browser settings:

- **Chrome:** Settings → System → Open proxy settings → make sure nothing is set
- Or check `Settings → System → Use a proxy server` → turn OFF

---

### Step 7: If firewall is blocking

```bash
# Check iptables
sudo iptables -L -n
# Flush all rules to reset
sudo iptables -F
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X
```

---

### Step 8: Nuclear option — full network restart

```bash
sudo ip link set <your_interface> down
sudo ip link set <your_interface> up
sudo dhclient <your_interface>
# Replace <your_interface> with your actual interface name (e.g., enp3s0, wlan0)
```

---

### 📋 Run this all-in-one diagnostic and paste the output here

```bash
echo "=== HOSTNAME/IP ===" && hostname -I && echo "=== INTERFACES ===" && ip addr show | grep -E "^[0-9]|inet " && echo "=== DNS ===" && cat /etc/resolv.conf && echo "=== ENV PROXY ===" && env | grep -i proxy && echo "=== GATEWAY ===" && ping -c2 192.168.1.1 && echo "=== BAIDU ===" && ping -c2 baidu.com && echo "=== IPTABLES ===" && sudo iptables -L -n 2>/dev/null | head -20
```

复制完整输出发送给我 —— 我会告诉你具体需要修复哪里。 🦞
