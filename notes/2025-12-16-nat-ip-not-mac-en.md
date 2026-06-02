---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: NAT Translates IP Addresses Not MAC
translated: false
type: note
---

Question: Is Network Address Translation used to translate IP addresses to MAC addresses, and vice versa?

Answer:

No, that's not correct.

**Network Address Translation (NAT)** is a technique used in networking to modify IP addresses (and often ports) in packet headers as they pass through a router or firewall. Its primary purposes are:

- Allowing multiple devices on a private network (using private IP addresses) to share a single public IP address for internet access.
- Conserving public IPv4 addresses.
- Providing a layer of security by hiding internal IP addresses.

NAT operates at the **network layer (Layer 3)** of the OSI model and only deals with **IP addresses** (and ports in cases like Port Address Translation or PAT/NAT overload). It does **not** involve MAC addresses at all.

The process you're describing—translating between **IP addresses** and **MAC addresses**—is handled by the **Address Resolution Protocol (ARP)**, which operates at the **data link layer (Layer 2)**. ARP resolves IPv4 addresses to MAC addresses within a local network segment, and Reverse ARP (RARP) or similar mechanisms can do the opposite (though RARP is largely obsolete).

In summary:

- NAT: IP ↔ IP (and ports)
- ARP: IP → MAC (on local networks)

These are distinct protocols for different layers and purposes.

References:

- [Network address translation - Wikipedia](https://en.wikipedia.org/wiki/Network_address_translation)
- [What Is Network Address Translation (NAT)? - Cisco](https://www.cisco.com/site/us/en/learn/topics/networking/what-is-network-address-translation-nat.html)
- [Does NAT change the source MAC address? - Server Fault](https://serverfault.com/questions/145876/does-nat-change-the-source-mac-address)
- [Does NAT Map to the MAC Address, or to the Local IP? - Super User](https://superuser.com/questions/651143/does-nat-map-to-the-mac-address-or-to-the-local-ip)
