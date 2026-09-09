---
audio: false
generated: true
image: false
lang: en
layout: post
title: "EtherType: 16-bit Protocol Identifier"
translated: false
type: note
---

**Question:** What is EtherType?

**Answer:**

EtherType is a **two-byte (16-bit) field** in an Ethernet frame header that identifies which **upper-layer protocol** is encapsulated in the frame's payload — essentially telling the receiving network stack *how to interpret the data* that follows.

**Where it sits in an Ethernet frame:**

| Destination MAC | Source MAC | **EtherType** | Payload | FCS |
|---|---|---|---|---|
| 6 bytes | 6 bytes | **2 bytes** | 46–1500 bytes | 4 bytes |

**Dual role — EtherType vs. Length:**

In modern Ethernet, this same 2-byte field can serve two different purposes depending on its value:

- **≤ 0x05DC (1500)** → indicates the **length** of the payload (IEEE 802.3 framing)
- **≥ 0x0600 (1536)** → indicates the **EtherType** / protocol identifier (Ethernet II framing)

**Who assigns EtherType values?**

EtherType values are assigned by the **IEEE Registration Authority**.

**Common EtherType values:**

| EtherType | Protocol |
| ----------- | ---------- |
| `0x0800` | IPv4 |
| `0x0806` | ARP |
| `0x86DD` | IPv6 |
| `0x8100` | VLAN tag (IEEE 802.1Q) |
| `0x8847` | MPLS unicast |
| `0x88CC` | LLDP |

**How it works in practice:**

When a NIC receives an Ethernet frame, it reads the EtherType field and hands the payload off to the correct protocol handler — e.g., if EtherType is `0x0800`, the payload is passed up to the IP stack.

EtherTypes are 16-bit identifiers appearing as the initial two octets after the MAC destination and source addresses (or after a tag), which, when considered as an unsigned integer, are equal to or larger than 0x0600.

**References:**

- [EtherType – Wikipedia](https://en.wikipedia.org/wiki/EtherType)
- [RFC 7042 – IANA Considerations for IEEE 802 Parameters](https://datatracker.ietf.org/doc/rfc7042/)
- [EtherType – Networx Security Glossary](https://www.networxsecurity.org/members-area/glossary/e/ethertype.html)
