---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: First-Hop Redundancy Protocol Goal
translated: false
type: note
---

Question: What is the main goal of First-Hop Redundancy Protocols (FHRP)?

Answer:

**B) Provide default gateway redundancy**

First-Hop Redundancy Protocols (FHRP) such as HSRP (Hot Standby Router Protocol), VRRP (Virtual Router Redundancy Protocol), and GLBP (Gateway Load Balancing Protocol) are designed to eliminate the single point of failure caused by having only one active default gateway (router) for hosts on a LAN segment. They achieve this by allowing multiple physical routers to share a virtual IP address and virtual MAC address. One router acts as the active/primary gateway while others remain in standby, automatically taking over if the active router fails, ensuring continuous Layer 3 connectivity for end devices without requiring manual reconfiguration.

- **A** is incorrect as a primary goal (though GLBP does offer some load-balancing capability, it is still fundamentally an FHRP for redundancy).
- **C** is unrelated—FHRPs do not provide encryption.
- **D** is incorrect; FHRPs actually reduce ARP broadcasts by having hosts send ARP requests to a single virtual MAC.

References:
- [Cisco - First Hop Redundancy Protocols Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp_fhrp/configuration/xe-16/fhrp-xe-16-book/fhrp-hsrp.html)
- [RFC 5798 - Virtual Router Redundancy Protocol (VRRP) Version 3](https://datatracker.ietf.org/doc/html/rfc5798)
