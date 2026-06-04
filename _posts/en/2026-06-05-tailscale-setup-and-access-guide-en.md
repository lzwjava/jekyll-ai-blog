---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tailscale Setup and Access Guide
translated: false
type: note
---

Here's the full picture:

## What we did

Installed Tailscale v1.98.4 on this machine (Ubuntu 24.04 Noble, 192.168.1.36) and authenticated it to your tailnet.

## Current state

  Machine name:  to
  Account:       lzwjava@
  Status:        Connected and running
  Service:       tailscaled.service (enabled, starts on boot)
  Version:       1.98.4

## What this gives you

1. ACCESS FROM ANYWHERE — As long as your other device (laptop, phone) also has Tailscale installed and logged into the same account, you can reach this machine from any network — coffee shop, airport, cellular, behind NAT, anywhere.

2. ENCRYPTED MESH — Tailscale creates a WireGuard tunnel directly between your devices. All traffic between them is end-to-end encrypted. No port forwarding needed, no VPN server to maintain.

3. SSH ACCESS — From anywhere:
     ssh lzw@<tailscale-ip-of-this-machine>

4. SERVICE ACCESS — Any service running on this machine (web servers, databases, Hermes, Jupyter, etc.) is reachable via the Tailscale IP from your other devices.

## What you still need to do (on your other devices)

  - Install Tailscale on your MacBook (192.168.1.49): https://tailscale.com/download/mac
  - Install on your phone if you want mobile access
  - Log in with the same account (lzwjava@)
  - Then you can reach this machine from those devices

## Useful commands

  tailscale status          — see connected devices and their IPs
  tailscale ping <hostname> — test connectivity
  tailscale ip              — show this machine's Tailscale IP
  sudo tailscale down       — disconnect
  sudo tailscale up         — reconnect

## Optional enhancements

  - MagicDNS: access machines by name instead of IP (enable in Tailscale admin console)
  - Exit node: route all traffic through this machine when on public WiFi
  - Subnet routes: expose your entire 192.168.1.0/24 LAN to remote devices
  - Tailscale SSH: built-in SSH with no key management needed
