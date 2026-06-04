---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tailscale Deployment and Usage Overview
translated: false
type: note
---

```
══════════════════════════════════════════
  Tailscale Setup Summary
══════════════════════════════════════════

Account:        lzwjava@

Machine 1 — lzw-mac (this MacBook Air M2)
  OS:           macOS
  Tailscale:    v1.96.4 (Homebrew CLI)
  Role:         Daily driver

Machine 2 — to (Ubuntu workstation)
  OS:           Ubuntu 24.04 Noble
  Tailscale:    v1.98.4
  Role:         GPU/ML workstation (RTX 4070)
  Uptime:       45 days
  Service:      tailscaled.service (enabled, starts on boot)

Connectivity
  Ping:         10ms (direct LAN, WireGuard)
  Tunnel:       End-to-end encrypted, peer-to-peer
  SSH:          Public key auth, no password
  NAT:          Automatic traversal — works from any network

What you can do now
  • SSH to the workstation from anywhere:
      ssh lzw@<workstation-tailscale-ip>
  • Access any service on the workstation (Jupyter, web
    servers, databases) via its Tailscale IP
  • No port forwarding, no VPN server, no firewall changes
  • Works from coffee shops, airports, cellular, behind NAT

Optional enhancements (from Tailscale admin console)
  • MagicDNS — access machines by hostname instead of IP
  • Exit node — route all traffic through the workstation
    when on public WiFi
  • Subnet routes — expose your entire LAN to remote devices
  • Tailscale SSH — built-in SSH with no key management

Version mismatch note
  Client (1.96.4) != server (1.98.5). Functionally fine,
  but consider updating: brew upgrade tailscale
══════════════════════════════════════════
```
