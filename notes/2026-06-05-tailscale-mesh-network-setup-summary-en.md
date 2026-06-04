---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tailscale Mesh Network Setup Summary
translated: false
type: note
---

```
══════════════════════════════════════════════════════════════
  Tailscale Setup — Full Summary
══════════════════════════════════════════════════════════════

WHAT WE BUILT
  A secure, encrypted mesh network between your MacBook Air
  and Ubuntu workstation using Tailscale (WireGuard). You can
  now SSH and access services on the workstation from anywhere
  — home LAN, coffee shop, airport, cellular — no port
  forwarding or VPN server needed.

MACHINES ON YOUR TAILNET
  Account:  lzwjava@

  1. lzw-mac  (MacBook Air M2, macOS)
     Role:    Daily driver
     Tailscale IP: 100.x.x.x

  2. to       (Ubuntu 24.04, RTX 4070)
     Role:    GPU/ML workstation
     Uptime:  45 days
     Tailscale IP: 100.x.x.x

CONNECTIVITY
  Ping:         ~8ms (direct LAN path via WireGuard)
  Tunnel:       End-to-end encrypted, peer-to-peer mesh
  SSH:          Public key auth, no password required
  NAT traversal: Automatic — works from any network

WHAT WE DID (step by step)

  1. Workstation (to)
     - Installed Tailscale v1.98.4
     - Enabled tailscaled.service (auto-start on boot)
     - Authenticated to lzwjava@ tailnet

  2. MacBook Air (lzw-mac)
     - Installed Tailscale GUI app from App Store (v1.98.5)
     - Installed Homebrew CLI (v1.96.4) — caused version
       mismatch warning on every command
     - Authenticated to same tailnet
     - Fixed version mismatch:
       • Uninstalled old Homebrew CLI (v1.96.4)
       • Created wrapper script at /opt/homebrew/bin/tailscale
         that delegates to the GUI app's binary (v1.98.5)
       • Both client and server now report v1.98.5
       • No more warnings

  3. Connectivity verified
     - tailscale ping: 8ms, direct LAN
     - SSH: public key auth working
     - Host key added to ~/.ssh/known_hosts

HOW THE CLI WORKS NOW
  /opt/homebrew/bin/tailscale
    ↓ (wrapper script, forwards all args)
  /Applications/Tailscale.app/Contents/MacOS/Tailscale
    ↓ (talks to)
  tailscaled (managed by GUI app's system extension, no sudo)

  The GUI app handles the daemon lifecycle — starting
  tailscaled on login, reconnecting after sleep, and
  managing the system extension. No sudo, no manual
  service management.

USEFUL COMMANDS
  tailscale status          — see connected devices
  tailscale ping <host>     — test connectivity
  tailscale ip              — show this machine's Tailscale IP
  tailscale down            — disconnect
  tailscale up              — reconnect
  ssh lzw@<workstation-ip> — SSH from anywhere

OPTIONAL ENHANCEMENTS (Tailscale admin console)
  MagicDNS      — access machines by hostname instead of IP
  Exit node     — route all traffic through workstation on
                  public WiFi
  Subnet routes — expose entire 192.168.1.0/24 LAN remotely
  Tailscale SSH — built-in SSH with no key management
══════════════════════════════════════════════════════════════
```
