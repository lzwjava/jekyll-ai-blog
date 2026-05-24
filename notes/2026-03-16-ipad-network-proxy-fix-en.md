---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing iPad Network and Proxy Issues
translated: false
type: note
---

**Summary of iPad Connectivity Issues & Fixes:**

## **1. Initial Problem: DHCP Not Working**
- iPad got `169.254.x.x` (APIPA) instead of `192.168.201.x`
- **Cause:** UFW firewall blocking DHCP ports 67/68
- **Fix:** `sudo ufw allow in on enx00e04c362f89 to any port 67,68 proto udp`

## **2. Second Problem: iPad Connected but No Internet**
- iPad got IP `192.168.201.136` via DHCP ✓
- Traffic reaching Clash (`192.168.201.136 --> gateway.icloud.com` in logs) ✓
- **Cause A:** UFW blocking FORWARD traffic between interfaces
- **Fix A:** `sudo ufw default allow routed` + interface routing rules
- **Cause B:** DNS bypass - iPad using `8.8.8.8` not Clash DNS (`192.168.201.1`)
- **Fix B:** Updated dnsmasq to push Clash DNS via DHCP option 6

## **3. Critical Insight: Routing Loop Prevention**
- **Problem:** iPad traffic for laptop's WAN network (`192.168.1.0/24`) could loop:
iPad → Clash TUN → `192.168.1.x` → back to WAN interface → loop
- **Solution:** Explicit `IP-CIDR,192.168.1.0/24,DIRECT` rule in Clash config
- Also added `IP-CIDR,192.168.201.0/24,DIRECT` for USB LAN

## **4. DNS Architecture Fix**
**Before:** iPad → `8.8.8.8` (bypassing Clash) → No fake-IP, proxy broken
**After:** iPad → `192.168.201.1` (Clash DNS) → fake-IP → TUN intercept → proxy

## **5. Split Routing Configuration**
Updated Clash rules:
- Local subnets (`192.168.1.0/24`, `192.168.201.0/24`) → DIRECT
- Apple/iCloud services → DIRECT (for iPad functionality)
- Chinese sites → DIRECT
- Everything else → Hysteria2 proxy

## **Current Status:**
- ✅ DHCP working (iPad gets `192.168.201.136`)
- ✅ Firewall allows forwarding
- ✅ NAT masquerade active
- ✅ Clash running with split routing
- ✅ DNS pointing to Clash (`192.168.201.1`)
- ✅ Loop prevention rules in place

**Remaining step:** iPad needs to renew DHCP lease to get new DNS settings, or set DNS manually to `192.168.201.1`.

**Test commands for iPad:**
```bash
nslookup google.com 192.168.201.1 # Should return fake IP (198.18.0.x)
curl https://api.ipify.org # Should show 69.63.0.0 (US IP)
curl baidu.com # Should work (DIRECT)
```

The architecture is now correct. Any remaining issues are likely DNS-related (iPad caching old `8.8.8.8` DNS) or Hysteria2 proxy connectivity.
