---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Common Ethernet Broadcast Frame Scenarios
translated: false
type: note
---

Here are the most common real-world scenarios where an Ethernet **broadcast frame** (destination MAC = **FFFF.FFFF.FFFF**) is sent, along with **which device** actually puts that frame on the wire:

| Scenario                          | What kind of broadcast frame is sent                  | Which device sends the frame                  | Why it is sent (trigger)                                                                 |
|-----------------------------------|--------------------------------------------------------|-----------------------------------------------|-------------------------------------------------------------------------------------------|
| **ARP Request**                   | Ethernet dst=MAC FFFF.FFFF.FFFF + EtherType 0x0806    | The host that needs to resolve an IP address | A host wants to reach another IP on the same subnet but doesn’t know its MAC yet → sends ARP request to the whole L2 segment |
| **DHCP Discover / DHCP Request**  | Ethernet dst=MAC FFFF.FFFF.FFFF + UDP src port 68 → dst port 67 | The client (PC, phone, etc.)                  | Client has no IP yet (or is renewing) and is looking for a DHCP server                     |
| **IPv6 Router Solicitation (RS)** | Ethernet dst=MAC 33:33:00:00:00:02 (all-routers multicast), but Neighbor Solicitation (DAD or lookup) can be to 33:33:ff:xx:xx:xx; classic RS is multicast, not broadcast | The IPv6 host                                 | Host just came up and wants to discover routers or do Duplicate Address Detection         |
| **NetBIOS/WINS name resolution**  | Ethernet dst=MAC FFFF.FFFF.FFFF                        | Windows machines (legacy)                     | Old Windows networking trying to resolve NetBIOS names                                    |
| **Wake-on-LAN (magic packet)**    | Ethernet dst=MAC FFFF.FFFF.FFFF (or directed broadcast)| Another host on the same segment              | To wake up a sleeping machine                                                             |
| **Legacy IPX/SPX, AppleTalk, etc.**| Ethernet dst=MAC FFFF.FFFF.FFFF                       | Devices using those old protocols             | Service discovery in non-IP protocols                                                     |

### Most frequent cases you will see in a modern network (99% of broadcast frames)

1. **ARP requests** → sent by **any host or router** that needs to learn a MAC for a local IP
   → Example: PC wants to ping 192.168.1.50 → sends ARP “Who has 192.168.1.50?” with dst MAC FFFF.FFFF.FFFF

2. **DHCP Discover/Request** → sent by **clients** (laptops, phones, IoT devices, VMs, etc.) when they boot or renew
   → The very first packet a device sends when it has no IP is almost always a DHCP Discover broadcast.

### Who never sends true Ethernet broadcasts in normal operation?

- Layer-3 switches/routers (they forward them, but originate very few)
- Properly configured modern servers (they usually have static IPs, so no DHCP broadcasts, and they cache ARP entries)

### Summary

A broadcast frame (dst MAC = FFFF.FFFF.FFFF) is sent whenever a device on the local segment needs to reach **“everyone”** on Layer 2 because it does not yet know the specific unicast MAC of the target, or the protocol itself is designed as broadcast (old NetBIOS, etc.).

Most common senders today:

- Any PC/laptop/phone when it boots (DHCP)
- Any device that needs to resolve an IP → MAC mapping (ARP)
