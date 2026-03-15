---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix iPad DNS Proxy Loop Issue
translated: false
type: note
---

**Question:** Based on the detailed debug logs, what is the exact root cause of the iPad connectivity failure, and how do I fix it?

**Answer:**

## Root Cause: Confirmed — Hysteria2 Proxy Server DNS Loop

The logs reveal the issue with precision. Here is the exact failure chain:

```
iPad → Clash TUN → tries to connect to Hysteria2 server
  → Clash DNS resolves Hysteria2 domain → returns 198.18.0.28 (FAKE IP!)
  → Clash tries to route 198.18.0.28 → TUN intercepts it again
  → sends BACK to Clash → infinite loop → connection hangs/fails
```

This is a classic **"chicken-and-egg" DNS problem** in fake-IP mode: Clash needs to contact the proxy server to forward traffic, but its own DNS returns a fake-IP for the proxy server's domain, causing Clash to try to proxy the connection to its own proxy server — indefinitely.

---

## The Fix: Three Parts

### Fix 1 — `proxy-server-nameserver` (Most Important)

This is the proper Clash Meta/Mihomo solution. Add a dedicated DNS resolver specifically for proxy server domains that bypasses fake-IP:

```yaml
dns:
  enable: true
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16

  default-nameserver:
    - 223.5.5.5
    - 119.29.29.29

  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query

  # ↓↓↓ THIS IS THE KEY FIX ↓↓↓
  # Use real DNS (not fake-IP) to resolve YOUR proxy server's hostname
  proxy-server-nameserver:
    - https://doh.pub/dns-query
    - 223.5.5.5
```

`proxy-server-nameserver` tells Clash: "use these DNS servers to resolve proxy node hostnames, and return their **real IPs**, not fake IPs." This breaks the loop.

---

### Fix 2 — Add Hysteria2 Server Domain to `fake-ip-filter`

As a belt-and-suspenders measure, also explicitly exclude your Hysteria2 server's domain from fake-IP:

```yaml
dns:
  fake-ip-filter:
    - '*.lan'
    - 'localhost.ptlogin2.qq.com'
    - 'your-hysteria2-server.example.com'   # ← ADD YOUR ACTUAL SERVER DOMAIN HERE
```

This forces Clash to return the **real IP** for your proxy server domain even in fake-IP mode.

---

### Fix 3 — Add a DIRECT Rule for the Hysteria2 Server's Real IP

Once you know the real IP of your Hysteria2 server (get it with `dig your-hysteria2-domain @223.5.5.5`), add it as a DIRECT rule **before** the MATCH rule:

```yaml
rules:
  - IP-CIDR,192.168.201.0/24,DIRECT
  - IP-CIDR,192.168.1.0/24,DIRECT
  - IP-CIDR,<YOUR_HYSTERIA2_SERVER_REAL_IP>/32,DIRECT  # ← ADD THIS
  # ... other rules ...
  - MATCH,Hysteria2
```

This ensures that even if DNS somehow returns the real IP, traffic to your proxy server goes DIRECT (not back through itself).

---

## How to Apply the Fix

```bash
# 1. Edit your Clash config
sudo nano /etc/clash/config.yaml
# (or wherever your config lives — check with: ps aux | grep clash)

# 2. Add proxy-server-nameserver and fake-ip-filter as shown above

# 3. Restart Clash
sudo systemctl restart clash
# or
pkill clash && clash -d /etc/clash &

# 4. Verify the proxy server now resolves to a REAL IP (not 198.18.x.x)
dig your-hysteria2-domain @192.168.201.1
# ✅ Should return a real public IP now, NOT 198.18.x.x

# 5. Test from laptop
curl https://api.ipify.org
# Should return your proxy's exit IP
```

---

## Summary Diagnosis Table

| Symptom Observed | What It Means |
|---|---|
| iPad traffic reaches TUN (`tcpdump` on Meta confirmed) | ✅ TUN interception working |
| Only UDP in Clash logs, TCP silently dropped | ✅ Clash receiving TCP but failing to establish upstream |
| Hysteria2 resolves to `198.18.0.28` | ❌ **Root cause** — proxy server gets fake-IP |
| Proxy test from laptop also times out | ✅ Confirms it's a Clash-level upstream issue, not routing |
| Direct bypass NAT also failed | Because Clash intercepts all traffic including the bypass attempt via TUN |

The `proxy-server-nameserver` fix is standard for exactly this scenario and is documented in Clash Meta/Mihomo specifically to solve the "proxy server domain gets fake-IP" problem.

- [Clash Meta DNS config (proxy-server-nameserver)](https://merlinkodo.github.io/Clash-Rev-Doc/config/dns/)
- [Clash fake-IP explanation](https://en.clash.wiki/configuration/dns.html)