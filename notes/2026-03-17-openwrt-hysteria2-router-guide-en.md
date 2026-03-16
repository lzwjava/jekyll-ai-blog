---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenWrt Hysteria2 Router Setup Guide
translated: false
type: note
---

Question:
What is the best approach to set up a home router in China that uses a Hysteria2 server (located in Los Angeles) as the entry point to access the global internet, given previous difficulties with a Linux laptop gateway setup and considering switching to an OpenWrt router?

Answer:

Your current experiment using an old laptop with Linux Mint as a gateway **is technically correct but operationally complex**. The issues you encountered (DHCP, DNS interception, routing loops, firewall forwarding) illustrate why **general-purpose Linux machines are harder to maintain as home routers**.

From a system design perspective, you essentially built this architecture:

```
iPad
  ↓ USB LAN
Linux Laptop (dnsmasq + NAT + Clash + TUN)
  ↓
WAN
  ↓
Hysteria2 Server (Los Angeles)
  ↓
Global Internet
```

The design works, but it introduces several operational difficulties:

* Linux firewall rules (UFW / iptables / nftables)
* DNS hijacking and fake-IP handling
* Routing loops between LAN and WAN
* DHCP configuration
* Device-specific connectivity issues (iPad caching DNS)

These are **router problems**, not application problems. A dedicated router OS like OpenWrt is built specifically to handle them.

Therefore the most stable architecture for your goal is:

```
Home Devices (iPad / Phone / Laptop)
        ↓ WiFi / LAN
OpenWrt Router
        ↓
Hysteria2 Client (sing-box / PassWall2)
        ↓
Hysteria2 Server (Los Angeles)
        ↓
Global Internet
```

This architecture has several advantages.

---

# 1. Why OpenWrt Is Usually the Better Solution

A router operating system such as **OpenWrt** already includes:

* DHCP server (dnsmasq)
* DNS forwarding
* NAT
* firewall zone management
* LAN/WAN routing

Instead of manually configuring all of those pieces on Linux, OpenWrt exposes them through **LuCI web UI**.

Key benefits:

### Stability

Routers run for months without maintenance.

### Simpler networking

OpenWrt automatically handles:

* LAN → WAN forwarding
* DHCP leases
* DNS propagation

### Easier proxy integration

Plugins like **PassWall2** or **OpenClash** integrate proxy routing rules.

---

# 2. Hysteria2 Support in OpenWrt

Hysteria2 is typically implemented via **sing-box**, which is supported by several OpenWrt plugins.

Common solutions:

| Plugin              | Engine     | Hysteria2 Support | Notes                |
| ------------------- | ---------- | ----------------- | -------------------- |
| PassWall2           | sing-box   | Yes               | Very common in China |
| OpenClash           | Clash Meta | Yes               | Powerful rule system |
| sing-box standalone | sing-box   | Yes               | Manual configuration |

Among these, the most straightforward approach is:

**PassWall2 + sing-box**

because it has direct GUI configuration for Hysteria2 nodes.

---

# 3. Why Your Laptop Gateway Was Difficult

Your debugging summary shows the exact typical problems:

### Problem 1: DHCP failure

```
iPad → APIPA 169.254.x.x
```

Cause: firewall blocking DHCP ports.

Routers normally manage DHCP automatically.

---

### Problem 2: DNS bypass

Your iPad used:

```
8.8.8.8
```

instead of:

```
Clash DNS
```

This breaks proxy routing.

Routers normally enforce DNS redirection.

---

### Problem 3: Routing loops

```
192.168.1.x network
```

looped between interfaces.

Routers implement proper **zone separation**:

```
LAN → WAN
WAN → blocked
```

---

### Problem 4: Complex firewall rules

You had to configure:

```
ufw default allow routed
NAT
forward rules
interface rules
```

OpenWrt handles these internally using **firewall zones**.

---

# 4. Hardware Considerations

Your **2013 Lenovo laptop** is powerful enough but inefficient:

| Device         | Power Usage |
| -------------- | ----------- |
| Laptop router  | ~20–40W     |
| OpenWrt router | ~5–10W      |

Running 24/7, the laptop wastes electricity.

---

# 5. Recommended Architecture

I would recommend this setup:

```
ISP Modem
   ↓
OpenWrt Router
   ↓
PassWall2 / sing-box
   ↓
Hysteria2 Server (Los Angeles)
   ↓
Internet
```

All devices connect via WiFi to the router.

No USB networking.

No manual DNS.

---

# 6. Typical OpenWrt Setup Steps

The configuration is roughly:

### Step 1

Install packages

```
luci-app-passwall2
sing-box
```

---

### Step 2

Add Hysteria2 server node

Parameters include:

```
server address
port
auth string
obfs
TLS
```

---

### Step 3

Enable transparent proxy

```
LAN → Proxy
China IP → Direct
Private IP → Direct
```

---

### Step 4

Enable DNS hijacking

```
53 → sing-box DNS
```

---

### Step 5

Enable routing rules

Example:

```
China IP → DIRECT
Apple domains → DIRECT
Global → Hysteria2
```

---

# 7. Role of AI Agents (OpenClaw)

Using an AI agent like **OpenClaw** can significantly help because OpenWrt configuration often involves:

* editing config files
* opkg installation
* firewall adjustments

An agent can automate tasks like:

```
install passwall
configure sing-box
add hysteria2 node
enable dns hijack
restart firewall
```

This removes much of the manual effort.

---

# 8. Final Recommendation

Given your situation, the **best path is**:

1. Use your **OpenWrt Xiaomi router**
2. Install **PassWall2**
3. Configure **Hysteria2 via sing-box**
4. Let the router handle DHCP + DNS + NAT

Avoid using the laptop router unless you specifically need:

* experimentation
* debugging
* high bandwidth testing

For daily home use, a router-based architecture is **far simpler and more stable**.

---

If you'd like, I can also explain:

* the **best OpenWrt proxy stack in 2026 (PassWall2 vs OpenClash vs sing-box)**
* the **ideal rule configuration for China networks**
* how to build a **very reliable Hysteria2 home gateway architecture**.