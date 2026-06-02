---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: IP Forwarding Versus Port Forwarding
translated: false
type: note
---

Question: Does IP forwarding in a router mean forwarding an external/public IP address to a computer in its LAN so that the computer can be directly accessed from the internet?

Answer:

Not exactly—there's an important distinction between **IP forwarding** (also called IP routing) and **port forwarding** (or NAT destination mapping).

| Feature                  | IP Forwarding (Routing)                          | Port Forwarding / Destination NAT                |
|--------------------------|--------------------------------------------------|--------------------------------------------------|
| What it does             | Allows the router to forward packets between different networks (e.g., from WAN to LAN and vice versa) based on destination IP. | Changes the destination IP (and usually port) of incoming packets so they reach a specific internal device. |
| Does the internal device get a real public IP? | Only if you assign it a public IP directly on the device or use 1:1 NAT / IP passthrough. In normal home setups, no. | No. The internal device still has a private IP (192.168.x.x, 10.x.x.x, etc.). Only specific ports are redirected. |
| Typical use case         | Enabling routing so devices behind the router can reach the internet (and sometimes be reached if rules allow). | Exposing services (web server, game server, RDP, etc.) on a private device to the internet without giving it a public IP. |
| Common name in home routers | “IP forwarding” or just “routing” is usually always on when NAT is active. | Called “Port forwarding”, “Virtual servers”, “NAT rules”, etc. |

### Summary

- **IP forwarding alone** does **not** give a computer in your LAN a real external/public IP in most home/SOHO setups. It simply allows the router to route packets between interfaces.
- To make a computer accessible from the internet, you normally need **port forwarding** (destination NAT) or a **1:1 NAT / DMZ / IP passthrough** configuration that actually maps a public IP to the internal device.
- Some routers/ISPs offer a true “IP passthrough” or “bridge” mode where one LAN device gets the real public IP directly; in that case IP forwarding is still happening, but NAT is bypassed for that device.

So in short:
Plain IP forwarding = routing packets.
Making a LAN computer reachable from outside = usually port forwarding or 1:1 NAT, not just “IP forwarding.”

References:

- [Wikipedia - Network Address Translation](https://en.wikipedia.org/wiki/Network_address_translation)
- [Wikipedia - Port Forwarding](https://en.wikipedia.org/wiki/Port_forwarding)
- [Cisco - Understanding IP Routing](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13748-24.html)
