---
audio: false
generated: true
image: false
lang: en
layout: post
title: iOS Dual VPN Proxy Setup Guide
translated: false
type: note
---

**Question:** How to configure Tailscale and Shadowsocks on iOS simultaneously, given iOS VPN limitations and China's network environment?

**Answer:**

iOS restricts to **one active VPN at a time**, so you need a routing strategy. Here are practical solutions ranked by reliability:

## 1. **Shadowsocks in Proxy Mode (Recommended)**

The cleanest approach: run Shadowsocks as a **SOCKS5/HTTP proxy** (not VPN mode), then Tailscale as the VPN.

**iOS setup:**
- Install **Shadowrocket** (paid, most flexible) or **Quantumult X** (more powerful)
- Configure your Shadowsocks server as a proxy rule (SOCKS5), not as VPN
- Enable Tailscale VPN independently
- In Shadowrocket, set:
  ```
  [Proxy]
  ProxyName = SOCKS5, <SS_SERVER_IP>, <SS_PORT>, chacha20-poly1305, <PASSWORD>

  [Rule]
  # Route CN traffic through Shadowsocks
  GEOIP,CN,ProxyName
  FINAL,DIRECT
  ```

This works because proxy rules operate at app-level, not system VPN. Tailscale handles VPN tunneling, Shadowrocket handles proxy routing for specific domains/regions.

---

## 2. **Route Tailscale Traffic, Proxy Everything Else**

If you need both features to work globally:

```bash
# On your Mac/Linux gateway (running both services):
# Configure Shadowsocks to listen on 0.0.0.0:1080
# Configure Tailscale normally

# On iOS:
# - Connect to Tailscale VPN
# - Point apps/browsers to Shadowsocks gateway via Tailscale IP
```

**iOS config in Shadowrocket:**
```
[Proxy]
Gateway = <TAILSCALE_IP_OF_SS_GATEWAY>, 1080

[Rule]
# Anything not on Tailscale network uses Shadowsocks proxy
GEOIP,CN,Gateway
FINAL,DIRECT
```

---

## 3. **Selective VPN with Shadowsocks Primary**

If Shadowsocks is more critical (which it likely is in China):

- **Primary:** Shadowsocks as VPN in Shadowrocket
- **Secondary:** Tailscale access via **Shadowsocks-routed HTTP proxy** → Tailscale control server

This requires configuring Tailscale to use a SOCKS5 proxy:
```bash
# Tailscale CLI doesn't directly support proxy, but you can:
# 1. SSH into Tailscale peer through Shadowsocks proxy
# 2. Or use ProxyChains on macOS/Linux side
```

---

## 4. **Hardware Gateway (Best for Stability)**

If you have consistent VPN requirements, run both on your Ubuntu machine:

```bash
# Install ss-server (or use sslocal for client mode)
apt install shadowsocks-libev

# Start Shadowsocks
ss-server -c /etc/shadowsocks-libev/config.json -u

# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Now iOS connects:
# 1. Tailscale VPN to your Ubuntu machine
# 2. Shadowsocks traffic routed through same machine via proxy
```

iOS Shadowrocket config:
```
[Proxy]
ShadowsocksGW = SOCKS5, 100.x.x.x (Tailscale IP), 1080

[Rule]
GEOIP,CN,ShadowsocksGW
FINAL,Tailscale
```

---

## Why This Works

- **Proxy ≠ VPN**: iOS allows multiple proxies, only one VPN
- **Shadowsocks as proxy** handles traffic interception at app level
- **Tailscale VPN** handles secure tunnel to your machines
- No conflict because they operate on different layers (Layer 7 proxy vs Layer 3 VPN)

---

## iOS App Recommendations

| App | Proxy | VPN | Cost | Notes |
|-----|-------|-----|------|-------|
| **Shadowrocket** | ✓ | ✓ | $3-5 | Most flexible, best CN support |
| **Quantumult X** | ✓ | ✓ | $8 | More powerful rule engine |
| **Surge** | ✓ | ✓ | $10 | Overkill unless you need logging |
| **Tailscale iOS** | — | ✓ | Free | Just for Tailscale |

Use **Shadowrocket for routing**, **Tailscale app for VPN independently**.

---

**Key point:** Stop thinking "two VPNs" — think "one VPN + one proxy". Shadowsocks excels as a proxy layer, Tailscale as a VPN layer. They're designed for different jobs.
