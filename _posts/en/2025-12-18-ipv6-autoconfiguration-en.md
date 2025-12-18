---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: IPv6 Stateless Address Autoconfiguration Protocol
translated: false
type: note
---

Question: Which protocol is used for stateless address autoconfiguration in IPv6?  
A) DHCPv6  
B) SLAAC  
C) NAT66  
D) OSPFv3

Answer: 

The correct answer is **B) SLAAC**.

**Explanation**:  
Stateless Address Autoconfiguration (SLAAC) is the mechanism defined in IPv6 for hosts to automatically configure their own IPv6 addresses without requiring a stateful server. It uses Router Advertisement (RA) messages from routers, which include network prefix information, allowing hosts to generate their interface identifier (typically from the MAC address via EUI-64 or privacy extensions) and form a complete address. SLAAC is described in RFC 4862.

- **A) DHCPv6**: Incorrect. DHCPv6 is a stateful protocol that provides addresses and other configuration from a server (similar to DHCP in IPv4), but it is not stateless.
- **C) NAT66**: Incorrect. NAT66 is a form of Network Address Translation for IPv6, which is rarely used due to IPv6's large address space.
- **D) OSPFv3**: Incorrect. OSPFv3 is a routing protocol for IPv6, not related to address configuration.

SLAAC provides a simple, serverless way for devices to obtain addresses, making it the standard for stateless autoconfiguration in IPv6.

References:  
- [RFC 4862: IPv6 Stateless Address Autoconfiguration](https://tools.ietf.org/html/rfc4862)  
- [RFC 8415: DHCPv6](https://tools.ietf.org/html/rfc8415) (for contrast with stateful configuration)