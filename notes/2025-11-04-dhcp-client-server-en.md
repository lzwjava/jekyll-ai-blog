---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: DHCP Client and Server Roles
translated: false
type: note
---

No, that's a common mix-up, but DHCP doesn't need to "run" the same thing on both the client and router—it's a client-server protocol with distinct roles for each side. Let me break it down simply.

### Quick DHCP Overview

DHCP (Dynamic Host Configuration Protocol) automates assigning IP addresses and other network settings (like subnet mask, gateway, DNS) to devices on a network. It eliminates manual configuration.

### Roles in a Typical Setup

- **Router (or DHCP Server)**: Runs the **DHCP server** software. This is the "boss" that hands out IP addresses from a pool it manages. Most home/SOHO routers (e.g., from TP-Link, Netgear) have this built-in and enabled by default.
- **Client (e.g., your laptop, phone, PC)**: Runs a **DHCP client** (built into the OS, like `dhclient` on Linux or Windows' automatic IP setup). This requests an IP from the server but doesn't serve IPs to others.

Both sides are essential for the handshake, but they're not running identical "DHCP" processes—one serves, one requests.

### How It Works (Basic Flow)

1. **Client broadcasts "DISCOVER"**: New device joins the network and yells, "Hey, anyone got an IP for me?"
2. **Server (router) offers "OFFER"**: "Sure, here's an available IP and settings."
3. **Client requests "REQUEST"**: "I'll take that one, please."
4. **Server acknowledges "ACK"**: "Done—use it."

If the router's DHCP server is off, clients might need static IPs or another server (e.g., on a Pi-hole or enterprise setup).

### Common Scenarios

| Setup | DHCP Server Location | Client Behavior |
| ------- | ---------------------- | ----------------- |
| **Home Network** | Router (enabled) | Auto-configures everything |
| **No Router DHCP** | Manual/static IPs or external server | Client falls back to APIPA (169.254.x.x) if no response |
| **Enterprise** | Dedicated DHCP server (not router) | Same client request process |

If you're troubleshooting a specific issue (e.g., "My device isn't getting an IP"), share more details—I can help debug! For deeper reading, check out the official RFC: [RFC 2131: Dynamic Host Configuration Protocol](https://datatracker.ietf.org/doc/html/rfc2131).
