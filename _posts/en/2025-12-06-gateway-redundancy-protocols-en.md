---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Gateway Redundancy Protocols Explained
translated: false
type: note
---

Question: What are First-Hop Redundancy Protocols (FHRP) in networking?

Answer:

First-Hop Redundancy Protocols (FHRP) are a family of networking protocols designed to provide gateway (router) redundancy for hosts on a LAN segment. In a typical network, end devices (PCs, servers, etc.) are configured with a single default gateway IP address. If that physical router fails, all hosts lose connectivity to other networks, even if another router is available on the same subnet.

FHRPs solve this single point of failure by allowing multiple physical routers to **share a virtual IP address** and **virtual MAC address** that act as the default gateway for hosts. Only one router (the active/primary/master) forwards traffic at a time, while the others (standby/backup/slave) remain ready to take over instantly if the active one fails.

### Key Benefits

- High availability – sub-second failover in most cases
- No need to change host default gateway configuration
- Transparent to end devices (they always point to the same virtual IP)
- Load balancing possible in some implementations

### Common FHRP Protocols

| Protocol       | Developer   | Key Features                                                                 | Virtual IP/MAC Mechanism                          | Load Balancing Support |
|----------------|-------------|------------------------------------------------------------------------------|---------------------------------------------------|-------------------------|
| HSRP           | Cisco       | Hot Standby Router Protocol (proprietary, but widely supported)             | Virtual IP + Virtual MAC (01-00-5E-00-01-xx)     | Limited (MHSRP)        |
| VRRP           | IETF (RFC 5798) | Open standard, very similar to HSRP                                        | Virtual IP (can be the real IP of a router) + Virtual MAC (00-00-5E-00-01-xx) | No (VRRPv3 + some vendor extensions allow it) |
| GLBP           | Cisco       | Gateway Load Balancing Protocol (proprietary)                              | Virtual IP + Multiple virtual MACs (AVF)          | Yes – active load balancing across multiple routers |

### How They Work (General Principle)

1. Routers participating in the FHRP form a group and share a **virtual IP address** (the default gateway seen by hosts).
2. They elect one router as **active/master** and another as **standby/backup**.
3. The active router owns the virtual IP and responds to ARP requests with a **virtual MAC address**.
4. Routers exchange periodic hello/keepalive messages (usually multicast).
5. If the active router stops sending hellos, the standby takes over the virtual IP and MAC almost instantly (typically <1–3 seconds).
6. Hosts continue sending traffic to the same gateway IP/MAC with no reconfiguration needed.

### Summary Table of Main Differences

| Feature              | HSRP                  | VRRP                     | GLBP                     |
|----------------------|-----------------------|--------------------------|--------------------------|
| Standard             | Cisco proprietary     | Open standard (IETF)     | Cisco proprietary        |
| Preemption           | Yes (configurable)    | Yes (configurable)       | Yes                      |
| Timers               | 3 sec hello, 10 sec hold | 1 sec hello (default)   | 3 sec hello, 10 sec hold |
| Load balancing       | Only with Multiple HSRP groups | Generally no (some vendor tricks) | Native (AVF/AVG roles)   |
| Virtual MAC format   | 0000.0c07.acXX        | 0000.5e00.01XX           | 0007.b4XX.XXXX           |
| Authentication       | Plain text/MD5        | MD5/IPsec                | MD5                      |

FHRPs are fundamental in any enterprise network that requires high availability at the access or distribution layer. Modern alternatives or complements include using routing protocols (OSPF/BGP) with equal-cost paths or EVPN/VXLAN in data-center fabrics, but classic FHRPs remain widely deployed in traditional campus and branch designs.
