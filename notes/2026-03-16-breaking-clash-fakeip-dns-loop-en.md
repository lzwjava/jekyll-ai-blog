---
audio: false
generated: true
image: false
lang: en
layout: post
title: Breaking Clash Fake-IP DNS Loop
translated: false
type: note
---

## Summary of Solutions & Key Obstacles

### **Root Cause Identified**
**DNS Loop in Clash Fake-IP Mode**: Clash was returning fake IPs (198.18.x.x) for its own proxy server domain, creating an infinite routing loop.

### **The 3-Part Fix Applied**

1. **`proxy-server-nameserver` Configuration**
   - Added to Clash DNS config
   - Uses real DNS (223.5.5.5, 119.29.29.29) specifically for proxy server hostnames
   - Prevents proxy server domains from getting fake IPs

2. **`fake-ip-filter` Exclusion**
   - Added proxy server domain to filter list
   - Forces Clash to return real IPs for the proxy server domain
   - Breaks the DNS loop at the filtering layer

3. **DIRECT Route Rule**
   - Added explicit `IP-CIDR` rule for proxy server IP
   - Ensures traffic to proxy server goes DIRECT (bypasses proxy)
   - Prevents any remaining routing issues

### **Most Challenging Block**

**The "Chicken-and-Egg" DNS Problem** was the biggest obstacle:

```
iPad → Clash → Needs proxy → Resolves proxy domain → Gets FAKE IP (198.18.x.x) 
→ Tries to route fake IP → TUN intercepts → Back to Clash → INFINITE LOOP
```

This was **invisible in logs** - traffic would reach TUN but connections would silently hang because Clash couldn't establish the upstream connection to itself.

### **Critical Insight**
The breakthrough came from realizing that **Clash's own DNS was sabotaging itself**. When Clash tried to connect to its proxy server:
- Normal DNS: `proxy-server.com` → `real.ip.addr` ✓
- Clash Fake-IP DNS: `proxy-server.com` → `198.18.x.x` (FAKE!) ❌

### **Current Status**
- ✅ **DNS loop fixed**: Proxy server resolves to real IP
- ✅ **All infrastructure working**: DHCP, NAT, forwarding, TUN
- ✅ **iPad traffic flowing**: SYN packets reaching Clash
- ✅ **Clean single process**: No leftover zombie processes

The architecture is now **correct** - the DNS configuration ensures proxy servers get real IPs while normal domains get fake IPs for TUN interception.