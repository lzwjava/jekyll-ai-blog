---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPv6 Address Types Explained Simply
translated: false
type: note
---

Question: What are the three types of IPv6 addresses, including unicast, multicast, and anycast?

Answer: 

IPv6 addresses are categorized into three main types:

1. **Unicast addresses** - Identify a single network interface. Packets sent to a unicast address are delivered to the specific interface associated with that address.

2. **Multicast addresses** - Identify a group of interfaces. Packets sent to a multicast address are delivered to all interfaces in the group (one-to-many communication).

3. **Anycast addresses** - Identify the nearest interface among a group of interfaces. Packets sent to an anycast address are delivered to the closest interface (based on routing metrics), enabling efficient service discovery and load distribution.

The blank in the question should be filled with **unicast address** (单播地址). 

Note: Unlike IPv4, IPv6 does not use broadcast addresses; multicast addresses fulfill that functionality instead.

References:  

- [IPv6 Addressing Architecture - RFC 4291](https://datatracker.ietf.org/doc/html/rfc4291)
- [Cisco - IPv6 Address Types](https://www.cisco.com/c/en/us/support/docs/ip/ipv6/29199-ipv6-faq-29199.html)