---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tailscale DERP Relay Slowdown Fix
translated: false
type: note
---

## Tailscale SSH Slowness — Full Diagnosis

### Network Topology

```
Mac (<IP_ADDRESS>)              →  (<IP_ADDRESS>) to
Parents' home, Guangzhou             Your home, Zengcheng
<IP_ADDRESS> (Wi-Fi)                 <IP_ADDRESS> (ethernet)
Public IP: <IP_ADDRESS>              Public IP: <IP_ADDRESS>
Router: TL-WR886N (UPnP ✓)          Router: <IP_ADDRESS> (OpenWrt/LuCI, UPnP ✗)
```

### Root Cause

Tailscale was using **DERP relay** instead of direct connection:

```
Mac → DERP(sin) Singapore → to     ~500ms RTT → 5-6s SSH
Mac → DERP(lax) Los Angeles → to   ~350ms RTT → 5-6s SSH
```

Both machines are behind NAT, but a direct path IS possible because:

- `to` has **cone NAT** (`MappingVariesByDestIP: false`) — STUN discovers a stable endpoint
- Mac's parents' router has **UPnP** — Tailscale can open a port

Tailscale wasn't discovering this direct path on its own — it settled on DERP before completing peer probing.

### Fix Applied

Ran `tailscale ping --until-direct` to force Tailscale to keep probing until it found the direct path:

```
Before:  via DERP(sin/lax)   343-721ms per packet   SSH 5-6s
After:   via direct <IP_ADDRESS>:<PORT>   76ms        SSH 1.9s
```

Current status:

```
<IP_ADDRESS>   to   active; direct <IP_ADDRESS>:<PORT>
```

### Why It Wasn't Connecting Directly

| Factor | Mac (parents' home) | to (your home) |
|--------|-------------------|----------------|
| NAT type | UPnP available | Cone NAT (stable port) |
| UPnP | ✓ (TL-WR886N) | ✗ (no UPnP on home router) |
| IPv6 | ✗ | ✗ (disabled but no global addr) |
| STUN endpoint | Discovered | Stable mapped port |
| Inbound reachable | Yes (via UPnP) | No (ICMP blocked, no port forward) |

The direct path works because `to`'s cone NAT keeps its port mapped consistently, and Mac can send UDP to it. Tailscale's discovery timing was giving up before finding this.

### SSH Config Notes

Your SSH config has `lzw-to` with `ProxyCommand none` — correct. The catch-all `Host !192.168.*.*` routes through SOCKS5 proxy (`localhost:7891` → hysteria2 → LA). This doesn't affect Tailscale traffic (the daemon uses its own tunnel), but prefer `ssh lzw-to` over `ssh lzw@<IP_ADDRESS>` to be explicit.

### Recommended Permanent Fixes

1. **Forward UDP 41641 on home router** (LuCI → `<IP_ADDRESS>`) — makes `to` always reachable inbound, direct connection establishes immediately without DERP fallback.

2. **Periodic re-probe on Mac** — if you don't want to touch the router:

   ```bash
   */10 * * * * tailscale ping -c 1 --until-direct <TAILSCALE_IP> > /dev/null 2>&1
   ```

3. **Enable IPv6 on home router** — if China Telecom provides a public IPv6 prefix, Tailscale can NAT-traverse directly without STUN/UPnP.

**Option 1 is best** — one-time config, permanent fix.
