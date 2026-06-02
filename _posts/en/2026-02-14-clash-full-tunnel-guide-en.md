---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Clash Full Tunnel Setup Guide
translated: false
type: note
---

Question: How to configure Clash (using the provided partial config snippet) to achieve full-tunnel-like behavior or better proxy routing?

Answer:

Your current partial Clash config already looks like a typical Clash/Clash Meta/Clash Verge base:

```yaml
port: 7890                # HTTP proxy port
socks-port: 7891          # SOCKS5 proxy port
allow-lan: true           # Allows other devices on LAN to use this proxy
mode: Rule                # Rule-based routing (recommended over Global for most users)
log-level: info
external-controller: 127.0.0.1:9090
proxies:                  # ← your proxy nodes go here
```

To make it behave more like **full-tunnel mode** (everything routed through your VMess/Trojan proxies, similar to a VPN), here are the most common and effective ways to complete/configure it.

### Recommended: Use TUN Mode (True system-wide full tunnel, best choice on macOS)

TUN mode is the closest to Cisco AnyConnect full-tunnel behavior. It routes **all traffic** (TCP + UDP) through Clash without apps needing to respect system proxy settings.

Add/enable these lines (Clash Meta / Clash Premium core required):

```yaml
# Add or modify these
tun:
  enable: true
  stack: system          # or gvisor / mixed (system is fastest on macOS)
  dns-hijack:
    - any:53             # hijack all DNS queries → prevents DNS leaks
  auto-route: true       # automatically add routes to send all traffic through TUN
  auto-detect-interface: true
  mtu: 9000              # optional: higher MTU can improve speed (test 1400–9000)
```

**Full minimal working example with your snippet + TUN:**

```yaml
port: 7890
socks-port: 7891
allow-lan: true
mode: Rule
log-level: info
external-controller: 127.0.0.1:9090

tun:
  enable: true
  stack: system
  dns-hijack:
    - any:53
  auto-route: true
  auto-detect-interface: true

proxies:
  # ← your VMess / Trojan nodes here, example:
  - name: "🐟 漏网之鱼"
    type: vmess
    server: your.server.com
    port: 443
    uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    alterId: 0
    cipher: auto
    udp: true
    tls: true
    network: ws
    ws-opts:
      path: /yourpath
      headers:
        Host: your.host.com

proxy-groups:
  - name: "PROXY"
    type: select
    proxies:
      - "🐟 漏网之鱼"
      - DIRECT

rules:
  - MATCH,PROXY         # ← this makes everything go through proxy (full tunnel behavior)
```

**Steps to activate TUN on macOS:**
1. In Clash Verge / Mihomo / similar GUI → Settings → TUN Mode → Enable (grant admin rights, install helper once).
2. Restart Clash.
3. Set mode to **Rule** (or Global if you want no exceptions).
4. Test: `curl ipinfo.io` should show your proxy IP, even in Terminal / non-browser apps.

### Alternative: Stay in System Proxy mode but make it "feel" more like full tunnel

If you don't want TUN (e.g., avoid admin rights or kernel extension):

```yaml
# Keep your original settings, add/enhance:
mode: Global              # instead of Rule → forces everything through proxy
# or keep Rule and add strong final rule:
rules:
  - MATCH,PROXY         # everything unmatched goes to proxy

# Optional: force DNS through proxy to avoid leaks
dns:
  enable: true
  ipv6: false           # usually safer to disable IPv6 unless your node supports it
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - 8.8.8.8
    - 1.1.1.1
  fallback:
    - https://1.1.1.1/dns-query
```

### Quick Summary: Which mode to choose?

| Goal                              | Recommended Config Change          | Needs Admin Rights? | UDP Support? | Bypasses most apps? |
|-----------------------------------|------------------------------------|----------------------|--------------|----------------------|
| True full-tunnel (like AnyConnect)| Enable TUN + `MATCH,PROXY`         | Yes                 | Yes          | Yes                  |
| Strong proxy for most apps        | `mode: Global` or `MATCH,PROXY`    | No                  | No (TCP only)| Partial              |
| Smart routing (China direct, rest proxy) | Keep `mode: Rule` + good rules | No                  | No           | Partial              |

**Most users in 2026 with VMess/Trojan nodes use TUN mode** — it gives the best experience (UDP for games/voice, no app-level proxy issues, full DNS control).

If you share more of your config (especially proxy-groups and rules), I can give a more precise recommendation.

References:

- [Clash Meta TUN Mode Documentation](https://github.com/MetaCubeX/mihomo/wiki/TUN-device)
- [Clash Verge User Guide - TUN Setup](https://github.com/clash-verge-rev/clash-verge-rev/wiki)
- [Common Clash Configuration Examples](https://github.com/Loyalsoldier/clash-rules)
