---
audio: false
generated: true
image: false
lang: en
layout: post
title: Switch Classification by Layer
translated: false
type: note
---

Question: What is the classification of switches based on the protocol layers they handle? (Fill in the blank: Layer 2 switches and _____.)

Answer: **三层交换机 (Layer 3 Switches)**

Switches are classified by the OSI model layer at which they operate:

- **Layer 2 Switch (二层交换机):** Operates at the Data Link Layer. It uses **MAC addresses** to forward frames within the same network segment (LAN). It cannot route traffic between different subnets.

- **Layer 3 Switch (三层交换机):** Operates at both the Data Link Layer and the **Network Layer**. It uses **IP addresses** in addition to MAC addresses, enabling it to perform **inter-VLAN routing** and forward packets between different subnets — combining the functions of a traditional switch and a router.

| Feature | Layer 2 Switch | Layer 3 Switch |
| --- | --- | --- |
| OSI Layer | Layer 2 (Data Link) | Layer 2 + Layer 3 (Network) |
| Address Used | MAC Address | MAC + IP Address |
| Routing Capability | ✗ | ✓ |
| Inter-VLAN Routing | ✗ | ✓ |
| Speed | Very fast | Fast (hardware-based routing) |

> In some contexts, **Layer 4 switches** (四层交换机) are also mentioned, which can additionally inspect transport-layer information (TCP/UDP ports) for more advanced traffic management.

---

References:

- [OSI Model and Network Switches - Cisco](https://www.cisco.com/c/en/us/solutions/enterprise-networks/what-is-a-network-switch.html)
- [Layer 3 Switch vs Router - NetworkLessons](https://networklessons.com/switching/layer-3-switch)
