---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tailscale Installation and Status
translated: false
type: note
---

Here's the summary with IPs redacted:

══════════════════════════════════════════════
  Tailscale Installation Summary
══════════════════════════════════════════════

WHAT WAS DONE

  1. Added Tailscale's official APT repo for Ubuntu Noble
     - GPG key: /usr/share/keyrings/tailscale-archive-keyring.gpg
     - Repo:    /etc/apt/sources.list.d/tailscale.list
  2. Installed tailscale v1.98.4 via apt
  3. Enabled and started tailscaled.service (auto-starts on boot)
  4. Authenticated with your lzwjava@ account

THIS MACHINE
  Hostname:   xx
  Status:     connected, logged in as lzwjava@

YOUR TAILSCALE NETWORK (4 devices)
  ┌──────────────────────┬────────┬─────────┐
  │ Device               │ OS     │ Status  │
  ├──────────────────────┼────────┼─────────┤
  │ xx (this machine)    │ Linux  │ active  │
  │ to                   │ Linux  │ active  │
  │ lzw-mac              │ macOS  │ offline │
  │ iphone-14-pro-max    │ iOS    │ offline │
  └──────────────────────┴────────┴─────────┘

  "to" has a direct WireGuard connection to this machine.

USEFUL COMMANDS
  tailscale status          — show all devices and their status
  tailscale ping <device>   — test connectivity to another device
  tailscale ip              — show this machine's Tailscale IP
  tailscale up              — reconnect if disconnected
  tailscale down            — disconnect from the network
  tailscale set --operator=$USER  — allow non-root usage
  tailscale exit-node list  — list available exit nodes
  tailscale up --exit-node=<ip>  — route all traffic through another device

WHAT YOU CAN DO NOW

- Reach any device on your tailnet by Tailscale IP or hostname
- Use "to" as an exit node / proxy if it's configured for it
- Access services on your Mac or phone when they come online
- All traffic between devices is encrypted WireGuard tunnel

NOTE: tailscale commands require root currently. Run this to fix:
  sudo tailscale set --operator=$USER
